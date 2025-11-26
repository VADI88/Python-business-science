# Imports

import mizani.formatters as fl
import mizani.labels as ml
import numpy as np
import pandas as pd
from path import Path
from plotnine import (
    aes,
    coord_flip,
    element_rect,
    element_text,
    expand_limits,
    facet_wrap,
    geom_boxplot,
    geom_col,
    geom_density,
    geom_histogram,
    geom_jitter,
    geom_label,
    geom_line,
    geom_point,
    geom_smooth,
    geom_text,
    geom_violin,
    ggplot,
    labs,
    scale_color_cmap_d,
    scale_x_datetime,
    scale_y_continuous,
    theme,
    theme_light,
    theme_minimal,
    theme_tufte,
)
from plydata.cat_tools import cat_reorder

from transformer.bike_order_transformer import BikeOrderTransformer

database_folder_path = Path("data/database")

conn_string = f"sqlite:///{database_folder_path}/bikes_order_database.sqlite"

bike_order_line_df = BikeOrderTransformer(conn_string).transform_data()

bike_order_line_df["order_date"] = pd.to_datetime(
    bike_order_line_df["order_date"]
)

# 1.0 Scatter Plots ----
# - Great for Continuous vs Continuous

# Goal: Explain relationship between order line value
#  and quantity of bikes sold

quantity_total_price_by_order_df = (
    bike_order_line_df.select("order_id", "quantity", "total_price")
    .groupby("order_id")
    .sum()
    .reset_index()
)

p = (
    ggplot(
        data=quantity_total_price_by_order_df,
        mapping=aes(x="quantity", y="total_price"),
    )
    + geom_point(alpha=0.8)
    + geom_smooth(method="lm")
    + theme_light()
)
p.show()

# 2.0 Line Plot ----
# - Great for time series

# Goal: Describe revenue by Month, expose cyclic nature

# Step 1: Data Manipulation


bike_sales_m_df = bike_order_line_df.summarize_by_time(
    date_column="order_date",
    value_column=["total_price"],
    rules="MS",
    time_format="timestamp",
).reset_index()

# Step 2: Plot

p = (
    ggplot(data=bike_sales_m_df, mapping=aes(x="order_date", y="total_price"))
    + geom_line(alpha=0.7)
    + geom_smooth(method="lm", se=False)
    + geom_smooth(method="loess", se=False, span=0.2, color="dodgerblue")
    + theme_light()
)
p.show()

# 3.0 Bar / Column Plots ----
# - Great for categories

# Goal: Sales by Descriptive Category

# Step 1: Data Manipulation
bike_sales_by_cat2_df = (
    bike_order_line_df.groupby("category_2", as_index=False)
    .agg(revenue=("total_price", np.sum))
    .sort_values("revenue", ascending=False)
    .assign(
        category_2=lambda x: cat_reorder(
            x["category_2"], x["revenue"], ascending=True
        )
    )
)

# Aside: Categorical Data (pd.Categorical)
# - Used frequently in plotting to designate order of categorical data


# Step 2: Plot

p = (
    ggplot(data=bike_sales_by_cat2_df, mapping=aes("category_2", "revenue"))
    + geom_col(fill="#2c3e50", color="white")
    + coord_flip()
    + theme_light()
)

p.show()

# 4.0 Histogram / Density Plots ----
# - Great for inspecting the distribution of a variable

# Goal: Unit price of bicycles

# Histogram ----

# Step 1: Data Manipulation

unit_price_by_models_df = bike_order_line_df.select(
    "model", "frame_material", "price"
).drop_duplicates()  # type: ignore

# Step 2: Visualize
p = (
    ggplot(
        data=unit_price_by_models_df,
        mapping=aes("price", fill="frame_material"),
    )
    + geom_histogram(bins=25, color="white")
    + facet_wrap("frame_material", ncol=1)
    + theme_tufte()
)

p.show()

# Density ----

p = (
    ggplot(
        data=unit_price_by_models_df,
        mapping=aes("price", fill="frame_material"),
    )
    + geom_density(color="white")
    + facet_wrap("frame_material", ncol=1)
    + theme_tufte()
)

p.show()

# 5.0 Box Plot / Violin Plot ----
# - Great for comparing distributions

# Goal: Unit price of model, segmenting by category 2

# Step 1: Data Manipulation
unit_price_by_cat2_df = (
    bike_order_line_df.select("model", "category_2", "price")
    .drop_duplicates()
    .assign(
        category_2=lambda x: cat_reorder(
            x["category_2"], x["price"], fun=np.median, ascending=True
        )
    )
)

# Step 2: Visualize

# Box Plot
p = (
    ggplot(data=unit_price_by_cat2_df, mapping=aes(y="price", x="category_2"))
    + geom_boxplot()
    + coord_flip()
    + theme_tufte()
)

p.show()

# Violin Plot & Jitter Plot

p = (
    ggplot(data=unit_price_by_cat2_df, mapping=aes(y="price", x="category_2"))
    + geom_violin()
    + geom_jitter()
    + coord_flip()
    + theme_tufte()
)

p.show()

# 6.0 Adding Text & Label Geometries----

# Goal: Exposing sales over time, highlighting outlier

# Data Manipulation


bike_sales_y_df = (
    bike_order_line_df.summarize_by_time(
        date_column="order_date",
        value_column=["total_price"],
        rules="YS",
        time_format="timestamp",
    )
    .reset_index()
    .assign(
        total_price_text=lambda x: fl.label_dollar(big_mark=",", precision=0)(
            x["total_price"]
        )
    )
)

# Adding text to bar chart


p = (
    ggplot(data=bike_sales_y_df, mapping=aes("order_date", "total_price"))
    + geom_col(fill="#2c3e50", color="white")
    + geom_smooth(method="lm", se=False)
    + geom_text(
        aes(label="total_price_text"),
        va="top",
        nudge_y=-2e-5,
        size=8,
        color="white",
        ha="center",
    )
    + geom_label(
        label="Major Demand",
        data=bike_sales_y_df[bike_sales_y_df.order_date.dt.year == 2013],
        nudge_y=1e6,
        color="red",
    )
    + expand_limits(y=[0, 20e6])
    + scale_x_datetime(date_labels="%Y")
    + scale_y_continuous(labels=ml.label_dollar(precision=0))
    + theme_light()
)

p.show()

# Filtering labels to highlight a point


# 7.0 Facets, Scales, Themes, and Labs ----
# - Facets: Used for visualizing groups with subplots
# - Scales: Used for transforming x/y axis and colors/fills
# - Theme: Used to adjust attributes of the plot
# - Labs: Used to adjust title, x/y axis labels

# Goal: Monthly Sales by Categories


bike_sales_cat2_m_df = bike_order_line_df.summarize_by_time(
    date_column="order_date",
    value_column=["total_price"],
    wide_format=False,
    groups=["category_2"],
    rules="MS",
    time_format="timestamp",
).reset_index()

# Step 1: Format Data
p = (
    ggplot(
        data=bike_sales_cat2_m_df,
        mapping=aes(x="order_date", y="total_price", color="category_2"),
    )
    + geom_line(color="#2c3e50")
    + geom_smooth(method="lm", se=False, color="dodgerblue")
    + facet_wrap("category_2", ncol=3, scales="free_y")
    + scale_x_datetime(date_breaks="2 years", date_labels="%Y")
    + scale_y_continuous(labels=ml.label_dollar(precision=0))
    + scale_color_cmap_d()
    + theme_minimal()
    + theme(
        strip_background=element_rect(fill="#2c3e50"),
        strip_text=element_text(color="white"),
        legend_position="none",
        figure_size=(16, 8),
        subplots_adjust={"wspace": 0.25},
        # legend_background= element_rect(fill = "white")
    )
    + labs(
        x="Order Year month",
        y="Revenue",
        title="Revenue by Month and Category2",
        fill="Category 2",
    )
)

p.show()
p.save("sales_by_m_cat2.png")

# Step 2: Visualize
