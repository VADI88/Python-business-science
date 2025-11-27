# Library
import pandas as pd
from my_pandas_extension.plot_forecast import plot_forecast
from my_pandas_extension.timeseries_func import summarize_by_time
from my_pandas_extension.utils import prepare_data
from transformer.bike_order_transformer import BikeOrderTransformer
from transformer.data_access import DataAccess
from transformer.forecasting import Forecaster

bike_order_line_df: pd.DataFrame = BikeOrderTransformer().transform_data()  # type: ignore

bike_order_line_df["order_date"] = pd.to_datetime(
    bike_order_line_df["order_date"]
)

# Total Revenue

total_revenue_m_df = bike_order_line_df.summarize_by_time(
    date_column="order_date",
    value_column=["total_price"],
    rules="MS",
    time_format="period",
)

forecast_df = Forecaster(data=total_revenue_m_df, h=12, sp=3).forecast()

forecast_df = forecast_df.assign(id="Total Revenue").prepare_data(
    id_column="id", date_column="order_date"
)

g = plot_forecast(forecast_df, id_column="id", date_column="date")
g.show()


# Revenue by Category 1
revenue_by_category_1_m_df = bike_order_line_df.summarize_by_time(
    date_column="order_date",
    value_column=["total_price"],
    groups=["category_1"],
    rules="MS",
    time_format="period",
)

forecast_by_cat1_df = Forecaster(
    data=revenue_by_category_1_m_df, h=12, sp=3
).forecast()


forecast_by_cat1_df = forecast_by_cat1_df.prepare_data(
    id_column="category_1", date_column="order_date"
)

g = plot_forecast(forecast_by_cat1_df, id_column="id", date_column="date")
g.show()


# Revenue by Category 1
revenue_by_category_2_m_df = bike_order_line_df.summarize_by_time(
    date_column="order_date",
    value_column=["total_price"],
    groups=["category_2"],
    rules="MS",
    time_format="period",
)

forecast_by_cat2_df = Forecaster(
    data=revenue_by_category_2_m_df, h=12, sp=3
).forecast()


forecast_by_cat2_df = forecast_by_cat2_df.prepare_data(
    id_column="category_2", date_column="order_date"
)

g = plot_forecast(forecast_by_cat2_df, id_column="id", date_column="date",facet_ncol=3)
g.show()

all_forecast_df = pd.concat([forecast_df,forecast_by_cat1_df,forecast_by_cat2_df],ignore_index=True)


db_access = DataAccess.write_data_to_db(data=all_forecast_df
                                          ,table_name="forecast",if_exists="replace",
                                          id_column = 'id',date_column = 'date'
                                          )
