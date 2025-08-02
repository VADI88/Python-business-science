# Imports

import pandas as pd
import numpy as np
from path import Path
from my_pandas_extension.timeseries_func import summarize_by_time
from transformer.bike_order_transformer import BikeOrderTransformer
from plotnine import *
from transformer.forecasting import Forecaster
import mizani.labels as ml
import mizani.formatters as fl

database_folder_path = Path("data/database")

conn_string = f"sqlite:///{database_folder_path}/bikes_order_database.sqlite"

bike_order_line_df = BikeOrderTransformer(conn_string).transform_data()

bike_order_line_df["order_date"] = pd.to_datetime(bike_order_line_df["order_date"])

# Step 1 : Data summarization
bike_sales_y_df = bike_order_line_df.summarize_by_time(
    date_column="order_date",
    value_column=["total_price"],
    rules="YS",
    time_format="timestamp",
).reset_index()

# Step 2 : Ploting

p = (
    ggplot(data=bike_sales_y_df, mapping=aes(x="order_date", y="total_price"))
    + geom_col(fill="#2c3e50")
    + geom_smooth(method="lm", se=False, color="dodgerblue")
    + expand_limits(y=20e6)
    + scale_y_continuous(labels=fl.label_dollar(scale=1e-6, suffix="M"))  # type: ignore
    + scale_x_datetime(date_labels="%Y")
    + labs(title="Revenue by year", x="", y="Revenue")
    + theme_light()
)

p.show()

p.save(Path("module7") / "bike_sales_y.png")
type(p)
