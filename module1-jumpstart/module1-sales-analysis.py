# JUMPSTART (Module 1): First Sales Analysis with Python


# 1.0 Load Libraries

# %%
# Core Python Data Analysis
import pandas as pd
import numpy as np
import janitor  # type: ignore

# Plotting
import matplotlib.pyplot as plt
from plotnine import (
    ggplot,
    aes,
    geom_col,
    geom_line,
    geom_smooth,
    facet_wrap,
    scale_y_continuous,
    scale_x_datetime,
    labs,
    theme,
    theme_minimal,
    theme_matplotlib,
    expand_limits,
element_text
)

from mizani.breaks import date_breaks
from mizani.formatters import date_format, currency_format

# Misc

from path import Path
from os import mkdir
from rich import pretty

pretty.install()

# %%

# 2.0 Importing Data Files

raw_folder_path = Path("data/data_raw")
wrangled_folder_path = Path("data/data_wrangled")

# %%

bikes_df = pd.read_excel(raw_folder_path / "bikes.xlsx").clean_names()  # type: ignore

bike_shop_df = pd.read_excel(
    raw_folder_path / "bikeshops.xlsx"
).clean_names()  # type: ignore

order_lines_df = pd.read_excel(
    io=raw_folder_path / "orderlines.xlsx", converters={"order.date": str}
).clean_names()  # type: ignore

# %%
# 3.0 Examining the data


top_bikes_series = bikes_df["description"].value_counts().nlargest(5)

top_bikes_series.plot(kind="barh").invert_yaxis()
plt.show()


# %%
# 4.0 Joining the data

bike_order_line_joined_df = (
    order_lines_df.drop("unnamed_0", axis=1)
    .merge(right=bikes_df, how="left", left_on="product_id", right_on="bike_id")
    .merge(
        right=bike_shop_df, how="left", left_on="customer_id", right_on="bikeshop_id"
    )
)


# 5.0 Wrangling the data

# * Splitting the description columns into category_1, category_2 and frame_material

# %%

bike_order_line_cleaned_df = (
    bike_order_line_joined_df.deconcatenate_column(
        "description",
        sep=" - ",
        new_column_names=["category_1", "category_2", "frame_material"],
    )
    .deconcatenate_column(
        "location",
        sep=", ",
        new_column_names=["city", "state"],
        preserve_position=False,
    )
    .assign(total_price=lambda x: x["price"] * x["quantity"])
)

selected_columns_to_keep = [
    "order_id",
    "order_line",
    "order_date",
    # "customer_id",
    # "product_id",
    # "bike_id",
    "model",
    # "description",
    # "bikeshop_id",
    "quantity",
    "price",
    "total_price",
    "bikeshop_name",
    "location",
    "category_1",
    "category_2",
    "frame_material",
    "city",
    "state",
]

bike_order_line_cleaned_df = bike_order_line_cleaned_df.select_columns(
    selected_columns_to_keep
)


# Save the cleaned data to folder

mkdir(wrangled_folder_path)

bike_order_line_cleaned_df.to_pickle(
    wrangled_folder_path / "bike_order_line_cleaned.pkl"
)


# 6.0 Visualizing a Time Series
# %%

bike_order_line_cleaned_df = pd.read_pickle(
    wrangled_folder_path / "bike_order_line_cleaned.pkl"
)



bike_order_line_cleaned_df["order_date"] = pd.to_datetime(
    bike_order_line_cleaned_df["order_date"]
)


# 6.1 Total Sales by Month ----
# Calculating the sales per month using resample.

sales_by_month_df = (
    bike_order_line_cleaned_df.select("order_date", "total_price")
    .set_index("order_date")
    .resample(rule="MS")
    .aggregate(np.sum)
    .reset_index()
)

# %%

usd_fmt = currency_format(prefix="$", big_mark=",",)

sales_by_month_plot = (
    ggplot(data=sales_by_month_df, mapping=aes(x="order_date", y="total_price"))
    + geom_line()
    + geom_smooth(method="loess", se=False, color="blue", span=0.3)
    + scale_y_continuous(labels=usd_fmt)  # type: ignore
    + labs(title="Revenue by month", x="", y="Revenue in USD$")
    + theme_matplotlib()
    + expand_limits(y=0)
)

sales_by_month_plot.draw(True)


# 6.2 Sales by Year and Category 2 ----

# %%
sales_by_month_cat2_df = (
    bike_order_line_cleaned_df.select("order_date", "category_2", "total_price")
    .set_index("order_date")
    .groupby("category_2")
    .resample(rule="W")
    .agg(func={"total_price": "sum"})
    .reset_index()
)


# %%
(
    sales_by_month_cat2_df.pivot_wider(
        index="order_date",
        names_from="category_2",
        values_from="total_price",
        reset_index=False,
    )
    .fillna(0)
    .clean_names(case_type="snake")
)

# %%

sales_by_month_cat2_plot = (
    ggplot(
        data=sales_by_month_cat2_df,
        mapping=aes(x="order_date", y="total_price"),
    )
    + geom_line(color="#2c3e50")
    + geom_smooth(method="lm", se=False, color="blue")
    + scale_y_continuous(labels = usd_fmt) # type: ignore
    + scale_x_datetime(breaks = date_breaks("2 years"),labels = date_format("%Y-%m")) # type: ignore
    + facet_wrap("category_2", ncol=3, scales="free_y")
    + labs(title="Revenue by week", x="", y="Revenue in USD$")
    + theme(
        subplots_adjust = {'w_space': 0.3},
        axis_text_y= element_text(size = 6),
        axis_text_x= element_text(size = 6 ,angle=45))

)


sales_by_month_cat2_plot.draw(True)
