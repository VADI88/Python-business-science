# Library
import warnings

import pandas as pd

from helper.logger import Log
from transformer.bike_order_transformer import BikeOrderTransformer
from transformer.forecasting import Forecaster
from transformer.data_access import DataAccess

from my_pandas_extension.timeseries_func import summarize_by_time  # isort: skip
from helper.utils import prepare_data  # isort: skip

warnings.filterwarnings(
    "ignore", message="'force_all_finite'", category=FutureWarning
)

db_access = DataAccess()

log = Log(
    log_dir="logs/update_database", log_name="update_database.log"
).get_logger()


bike_order_line_df = BikeOrderTransformer().transform_data()  # type: ignore

bike_order_line_df["order_date"] = pd.to_datetime(
    bike_order_line_df["order_date"]
)


# 1.0 SUMMARIZE AND FORECAST


# 1.1 Total Revenue

log.info("Forecast 1/4: Forecasting Total Revenue...\n")

total_revenue_m_df = bike_order_line_df.summarize_by_time(
    date_column="order_date",
    value_column=["total_price"],
    rules="MS",
    time_format="period",
)

forecast_df = Forecaster(data=total_revenue_m_df, h=12, sp=12).forecast()

forecast_df = forecast_df.assign(id="Total Revenue").prepare_data(
    id_column="id", date_column="order_date"
)

log.info("Forecast 1/4: Forecasting Total Revenue Complete\n")


# 1.2 Revenue by Category 1

log.info("Forecast 2/4: Forecasting Category 1...\n")

revenue_by_category_1_m_df = bike_order_line_df.summarize_by_time(
    date_column="order_date",
    value_column=["total_price"],
    groups=["category_1"],
    rules="MS",
    time_format="period",
)


forecast_by_cat1_df = Forecaster(
    data=revenue_by_category_1_m_df, h=12, sp=12
).forecast()

forecast_by_cat1_df = forecast_by_cat1_df.prepare_data(
    id_column="category_1", date_column="order_date"
)


log.info("Forecast 2/4: Forecasting Total Revenue Complete\n")

# 1.3 Revenue by Category 2

log.info("Forecast 3/4: Forecasting Category 1...\n")


revenue_by_category_2_m_df = bike_order_line_df.summarize_by_time(
    date_column="order_date",
    value_column=["total_price"],
    groups=["category_2"],
    rules="MS",
    time_format="period",
)


forecast_by_cat2_df = Forecaster(
    data=revenue_by_category_2_m_df, h=12, sp=12
).forecast()

forecast_by_cat2_df = forecast_by_cat2_df.prepare_data(
    id_column="category_2", date_column="order_date"
)

log.info("Forecast 3/4: Forecasting Total Revenue Complete\n")

# 1.4 Revenue by Customer

log.info("Forecast 4/4: Forecasting Revenue by Customer...\n")


revenue_by_bikeshop_Q_df = bike_order_line_df.summarize_by_time(
    date_column="order_date",
    value_column=["total_price"],
    groups=["bikeshop_name"],
    rules="Q",
    time_format="period",
)
forecast_by_bikeshop_df = Forecaster(
    data=revenue_by_bikeshop_Q_df, h=4, sp=3
).forecast()


forecast_by_bikeshop_df = forecast_by_bikeshop_df.prepare_data(
    id_column="bikeshop_name", date_column="order_date"
).assign(id=lambda x: "Bikeshop: " + x["id"])

log.info("Forecast 4/4: Forecasting Total Revenue by Customer Complete\n")


# 2.0 UPDATE DATABASE

log.info("updating database")


all_forecasts_df = pd.concat(
    [
        forecast_df,
        forecast_by_cat1_df,
        forecast_by_cat2_df,
        forecast_by_bikeshop_df,
    ],
    axis=0,
)

all_forecasts_  # Library
import warnings

import pandas as pd

from helper.logger import Log
from transformer.bike_order_transformer import BikeOrderTransformer
from transformer.forecasting import Forecaster
from transformer.data_access import DataAccess

from my_pandas_extension.timeseries_func import summarize_by_time  # isort: skip
from helper.utils import prepare_data  # isort: skip

warnings.filterwarnings(
    "ignore", message="'force_all_finite'", category=FutureWarning
)

db_access = DataAccess()

log = Log(
    log_dir="logs/update_database", log_name="update_database.log"
).get_logger()


bike_order_line_df = BikeOrderTransformer().transform_data()  # type: ignore

bike_order_line_df["order_date"] = pd.to_datetime(
    bike_order_line_df["order_date"]
)


# 1.0 SUMMARIZE AND FORECAST


# 1.1 Total Revenue

log.info("Forecast 1/4: Forecasting Total Revenue...\n")

total_revenue_m_df = bike_order_line_df.summarize_by_time(
    date_column="order_date",
    value_column=["total_price"],
    rules="MS",
    time_format="period",
)

forecast_df = Forecaster(data=total_revenue_m_df, h=12, sp=12).forecast()

forecast_df = forecast_df.assign(id="Total Revenue").prepare_data(
    id_column="id", date_column="order_date"
)

log.info("Forecast 1/4: Forecasting Total Revenue Complete\n")


# 1.2 Revenue by Category 1

log.info("Forecast 2/4: Forecasting Category 1...\n")

revenue_by_category_1_m_df = bike_order_line_df.summarize_by_time(
    date_column="order_date",
    value_column=["total_price"],
    groups=["category_1"],
    rules="MS",
    time_format="period",
)


forecast_by_cat1_df = Forecaster(
    data=revenue_by_category_1_m_df, h=12, sp=12
).forecast()

forecast_by_cat1_df = forecast_by_cat1_df.prepare_data(
    id_column="category_1", date_column="order_date"
)


log.info("Forecast 2/4: Forecasting Total Revenue Complete\n")

# 1.3 Revenue by Category 2

log.info("Forecast 3/4: Forecasting Category 1...\n")


revenue_by_category_2_m_df = bike_order_line_df.summarize_by_time(
    date_column="order_date",
    value_column=["total_price"],
    groups=["category_2"],
    rules="MS",
    time_format="period",
)


forecast_by_cat2_df = Forecaster(
    data=revenue_by_category_2_m_df, h=12, sp=12
).forecast()

forecast_by_cat2_df = forecast_by_cat2_df.prepare_data(
    id_column="category_2", date_column="order_date"
)

log.info("Forecast 3/4: Forecasting Total Revenue Complete\n")

# 1.4 Revenue by Customer

log.info("Forecast 4/4: Forecasting Revenue by Customer...\n")


revenue_by_bikeshop_Q_df = bike_order_line_df.summarize_by_time(
    date_column="order_date",
    value_column=["total_price"],
    groups=["bikeshop_name"],
    rules="Q",
    time_format="period",
)
forecast_by_bikeshop_df = Forecaster(
    data=revenue_by_bikeshop_Q_df, h=4, sp=3
).forecast()


forecast_by_bikeshop_df = forecast_by_bikeshop_df.prepare_data(
    id_column="bikeshop_name", date_column="order_date"
).assign(id=lambda x: "Bikeshop: " + x["id"])

log.info("Forecast 4/4: Forecasting Total Revenue by Customer Complete\n")


# 2.0 UPDATE DATABASE

log.info("updating database")


all_forecasts_df = pd.concat(
    [
        forecast_df,
        forecast_by_cat1_df,
        forecast_by_cat2_df,
        forecast_by_bikeshop_df,
    ],
    axis=0,
)

all_forecasts_df

# 2.1 Writing database

db_access.write_data_to_db(
    data=all_forecasts_df,
    table_name="forecast",
    if_exists="replace",
    id_column="id",
    date_column="date",
)
