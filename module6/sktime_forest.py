# IMPORTS
import pandas as pd
from path import Path
from sktime.forecasting.arima import AutoARIMA
from my_pandas_extension.timeseries_func import summarize_by_time
import numpy as np
from sktime.utils import plotting
from tqdm import tqdm
import warnings

warnings.filterwarnings("ignore")

from transformer.bike_order_transformer import BikeOrderTransformer

database_folder_path = Path("data/database")

raw_folder_path = Path("data/data_raw")

conn_string = f"sqlite:///{database_folder_path}/bikes_order_database.sqlite"

bike_order_line_df = BikeOrderTransformer(conn_string).transform_data()

bike_order_line_df["order_date"] = pd.to_datetime(bike_order_line_df["order_date"])

# 1.0 Data Summarization


# %%

bike_sales_m_df = bike_order_line_df.summarize_by_time(
    date_column="order_date",
    value_column=["total_price"],
    rules="MS",
    time_format="period",
)


bike_sales_cat2_m_df = bike_order_line_df.summarize_by_time(
    date_column="order_date",
    value_column=["total_price"],
    groups=["category_2"],
    rules="MS",
    time_format="period",
)


# 2.0 Auto Arima
# %%

y = bike_sales_m_df["total_price"]

forecaster = AutoARIMA(sp=12)  # seasonal period (monthly = 12

forecaster.fit(y)

forecaster.predict(
    fh=np.arange(1, 13),
)
forecaster.predict_quantiles(alpha=[0.275, 0.975])

coverage = 0.95
y_pred_ints = forecaster.predict_interval(coverage=coverage)
y_pred_ints

y_pred = forecaster.predict(
    fh=np.arange(1, 13),
)
y_pred_ints.index = y_pred.index
fig, ax = plotting.plot_series(
    y, y_pred, labels=["y", "y_pred"], pred_interval=y_pred_ints
)
# 3.0 Scaling

columns = bike_sales_cat2_m_df.columns

models_results_dict = dict()
for col in tqdm(columns):
    # Series extraction
    y = bike_sales_cat2_m_df[col]

    forecaster = AutoARIMA(sp=12, suppress_warnings=True)

    # predict

    forecaster.fit(y)

    h = 12

    predictions = forecaster.predict(fh=np.arange(1, h + 1))
    predictions_interval = forecaster.predict_interval(coverage=coverage)
    predictions_interval.index = predictions.index

    # Combine into single pandas dataframe

    predictions_return_Df = pd.concat([y, predictions, predictions_interval], axis=1)

    predictions_return_Df.columns = ["value", "prediction", "ci_lo", "ci_hi"]

    models_results_dict[col] = predictions_return_Df

models_results_df = pd.concat(models_results_dict, axis=0)
