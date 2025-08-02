# Imports

import pandas as pd
from path import Path
import matplotlib.pyplot as plt

from my_pandas_extension.timeseries_func import summarize_by_time
from transformer.bike_order_transformer import BikeOrderTransformer
from transformer.forecasting import Forecaster
from plotnine import *
import janitor
from plydata.cat_tools import cat_reorder

import numpy as np
import mizani.labels as ml
import mizani.formatters as fl

database_folder_path = Path("data/database")

conn_string = f"sqlite:///{database_folder_path}/bikes_order_database.sqlite"

bike_order_line_df = BikeOrderTransformer(conn_string).transform_data()

bike_order_line_df["order_date"] = pd.to_datetime(bike_order_line_df["order_date"])

bike_sales_m_df = bike_order_line_df.summarize_by_time(
    date_column="order_date",
    value_column=["total_price"],
    groups=["category_1"],
    rules="MS",
    time_format="period",
)

arima_forecast_df = Forecaster(data=bike_sales_m_df, h=12, sp=3).forecast()

# Workflow until now


# 1.0 FORECAST VISUALIZATION ----

# Step 1: Data preparation for Plot
df_prepared = (
    arima_forecast_df.melt(
        id_vars=["category_1", "order_date", "ci_lo", "ci_hi"],
        value_vars=["value", "prediction"],
        value_name=".value",
    )
    .rename(columns={".value": "value"})
    .assign(order_date=lambda x: x["order_date"].dt.to_timestamp())
)
# Step 2: Plotting

p = (
    ggplot(data=df_prepared, mapping=aes(x="order_date", y="value", color="variable"))
    + geom_ribbon(aes(ymin="ci_lo", ymax="ci_hi"), alpha=0.2, color=None)
    + geom_line()
    + facet_wrap("category_1", ncol=1, scales="free_y")
    + scale_x_datetime(date_labels="%Y", date_breaks="2 years")
    + scale_y_continuous(labels=ml.label_dollar(big_mark=",", precision=0))
    + scale_color_manual(values=["red", "#2c3e50"])
    + theme_minimal()
    + theme(figure_size=(15, 15), strip_background=element_rect(fill="#2c3e50"))
)

p.show()

# 2.0 PLOTTING AUTOMATION ----
# - Make plot_forecast()

# Function Development


# Testing

from my_pandas_extension.plot_forecast import plot_forecast

g = plot_forecast(arima_forecast_df, id_column="category_1", date_column="order_date")
g.show()
