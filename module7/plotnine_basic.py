# Imports

import mizani.formatters as fl
import pandas as pd
from path import Path
from plotnine import (
    aes,
    expand_limits,
    geom_col,
    geom_smooth,
    ggplot,
    labs,
    scale_x_datetime,
    scale_y_continuous,
    theme_light,
)

from transformer.bike_order_transformer import BikeOrderTransformer

bike_order_line_df = BikeOrderTransformer().transform_data()

bike_order_line_df["order_date"] = pd.to_datetime(
    bike_order_line_df["order_date"]
)

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
