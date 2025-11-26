from typing import Literal

import pandas as pd
import sqlalchemy as sql
from path import Path
from sqlalchemy.sql.sqltypes import Numeric
from sqlalchemy.types import String

from my_pandas_extension.plot_forecast import plot_forecast
from transformer.bike_order_transformer import BikeOrderTransformer
from transformer.forecasting import Forecaster

database_folder_path = Path("data/database")

conn_string = f"sqlite:///{database_folder_path}/bikes_order_database.sqlite"

bike_order_line_df: pd.DataFrame = BikeOrderTransformer(
    conn_string
).transform_data()

bike_order_line_df["order_date"] = pd.to_datetime(
    bike_order_line_df["order_date"]
)

bike_sales_m_df = bike_order_line_df.summarize_by_time(
    date_column="order_date",
    value_column=["total_price"],
    rules="MS",
    groups=["category_2"],
    time_format="period",
    wide_format=True,
    na_value=0,
)  # type: ignore

arima_forecast_df = Forecaster(data=bike_sales_m_df, h=12, sp=3).forecast()

g = plot_forecast(
    arima_forecast_df,
    id_column="category_2",
    date_column="order_date",
    facet_ncol=3,
)
g.show()


# Preparing the data to update the Databases


def prepare_forecast_data_for_update(
    data: pd.DataFrame,
    id_column: str,
    date_column: str,
) -> pd.DataFrame:
    data = data.rename(columns={id_column: "id", date_column: "date"})

    return data


def write_forecast_to_db(
    data: pd.DataFrame,
    id_column: str,
    date_column: str,
    conn_string: str = conn_string,
    table_name: str = "forecast",
    if_exists: Literal["fail", "replace", "append"] = "fail",
    **kwargs,
):
    # Prepare forecast
    df = prepare_forecast_data_for_update(data, id_column, date_column)

    df["date"] = df["date"].dt.to_timestamp()

    print(df.head())
    sql_dtypes = {
        "id": String(),
        "date": String(),
        "value": Numeric(),
        "prediction": Numeric(),
        "ci_lo": Numeric(),
        "ci_hi": Numeric(),
    }

    engine = sql.create_engine(conn_string)
    with engine.connect() as conn:
        df.to_sql(
            name=table_name,
            con=conn,
            if_exists=if_exists,
            dtype=sql_dtypes,
            index=False,
            **kwargs,
        )

    return
