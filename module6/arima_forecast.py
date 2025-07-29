# IMPORTS
import warnings

import pandas as pd
from path import Path

warnings.simplefilter('always', FutureWarning)
warnings.warn("debug", FutureWarning, stacklevel=2)
from my_pandas_extension.timeseries_func import summarize_by_time

import numpy as np

from pydantic import (
    validate_call,
    StrictFloat,
    ConfigDict,
    Field,
    StrictInt,
)
from typing import Literal, Annotated
import pandas_flavor as pf  # type: ignore
from tqdm import tqdm

from sktime.forecasting.arima import AutoARIMA

from transformer.bike_order_transformer import BikeOrderTransformer

database_folder_path = Path("data/database")

conn_string = f"sqlite:///{database_folder_path}/bikes_order_database.sqlite"

bike_order_line_df = BikeOrderTransformer(conn_string).transform_data()

bike_order_line_df["order_date"] = pd.to_datetime(bike_order_line_df["order_date"])

bike_sales_m_df = bike_order_line_df.summarize_by_time(  # type: ignore
        date_column="order_date",
        value_column=["total_price"],
        rules="MS",
        time_format="period",
)
bike_sales_cat2_m_df = bike_order_line_df.summarize_by_time(  # type: ignore
        date_column="order_date",
        value_column=["total_price"],
        groups=["category_2"],
        rules="MS",
        time_format="period",
)


# Function Development


@validate_call(config=ConfigDict(arbitrary_types_allowed=True))
def arima_forcast(
        data: pd.DataFrame,
        h: Annotated[int, Field(strict=True, gt=0)],
        sp: Literal[3, 6, 12, 24],
        alpha: Annotated[StrictFloat, Field(strict=True, gt=0, lt=1)] = 0.95,
        suppress_warmings=True,
        *args,
        **kwargs,
):
    # CHECKS

    # HANDLE INPUTS

    models_results_dict = dict()

    # FOR LOOPS

    for col in tqdm(data.columns, mininterval=0):
        y = data[col]

        forecaster = AutoARIMA(
                sp=sp, suppress_warnings=suppress_warmings, *args, **kwargs
        )

        forecaster.fit(y)

        predictions = forecaster.predict(fh=np.arange(1, h + 1))
        predictions_interval = forecaster.predict_interval(coverage=alpha)
        predictions_interval.index = predictions.index

        predictions_return_df = pd.concat([y, predictions, predictions_interval], axis=1)

        predictions_return_df.columns = ["value", "prediction", "ci_lo", "ci_hi"]

        models_results_dict[col] = predictions_return_df

    models_results_df = pd.concat(models_results_dict, axis=0)

    models_results_df.index.names = [*data.columns.names, *data.index.names]

    # Cols to keep
    models_results_df = models_results_df.reset_index()

    col_to_keep = ~models_results_df.columns.str.startswith('level_')

    models_results_df = models_results_df.iloc[:, col_to_keep]

    return models_results_df


models_df = arima_forcast(data=bike_sales_cat2_m_df, h=12, sp=12)
