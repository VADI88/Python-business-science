# IMPORTS

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from mizani.formatters import currency_format
from path import Path
from plotnine import (
    aes,
    coord_flip,
    facet_wrap,
    geom_col,
    ggplot,
    theme_minimal,
)

from transformer.bike_order_transformer import BikeOrderTransformer


raw_folder_path = Path("data/data_raw")


bike_order_line_df = BikeOrderTransformer().transform_data()

pd.set_option("display.max_columns", None)
pd.set_option("display.expand_frame_repr", False)
pd.set_option("max_colwidth", 2)

# 1.0 SELECTING COLUMNS
# SELECT BY COLUMNS

bike_order_line_df[
    ["order_date", "order_id", "order_line", "total_price"]
]  # ORder based on input criteria

# SELECT BY POSITION


bike_order_line_df.iloc[:, 0:3]

bike_order_line_df.iloc[:, -3:]

# Using filter

(bike_order_line_df.filter(regex="(^model)|(^cat)|(price$)", axis=1))

# Rearranging columns
# To make `model` first
# use pyjanitor packages

column_list = bike_order_line_df.columns.tolist()
column_list.remove("model")

bike_order_line_df[["model", *column_list]]

# Selecting Dtypes, Concat and drop


object_df = bike_order_line_df.select_dtypes(include="object")

numeric_df = bike_order_line_df.select_dtypes(include=int)

pd.concat([object_df, numeric_df], axis=1)

# 1.0 Arranging the data

bike_order_line_df.sort_values(by=["total_price"])  # ascending

bike_order_line_df.sort_values(
    by=["total_price"], ascending=False
)  # descending

(
    bike_order_line_df.filter(
        regex="(date$)|(^cat)|(price$)", axis=1
    ).sort_values(by=["order_date", "total_price"], ascending=[True, False])
)

# 2.0 SELECTING ROWS
# Non-query method
bike_order_line_df.order_date = pd.to_datetime(bike_order_line_df.order_date)

bike_order_line_df[bike_order_line_df.order_date.dt.year >= 2015]

bike_order_line_df[bike_order_line_df.model.str.contains("Carbon")]

# Query Methods
price_threshold_1 = 9000
price_threshold_2 = 1000

(
    bike_order_line_df.query(
        "price >= @price_threshold_1  | price <= @price_threshold_2 "
    )
)

# isin methods

bike_order_line_df[
    bike_order_line_df.category_2.isin(["Triathalon", "Over Mountain"])
]

bike_order_line_df[
    ~bike_order_line_df.category_2.isin(["Triathalon", "Over Mountain"])
]

# iloc

bike_order_line_df.iloc[0:5, [1, 3, 5]]

bike_order_line_df.iloc[0:5, :]

# n-largest / n-smallest

bike_order_line_df.nlargest(columns="total_price", n=20)

bike_order_line_df.nsmallest(columns="total_price", n=20)

# sample

bike_order_line_df.sample(frac=1.5, replace=True)

# 3.0 Mutating / Assign

# Method 1 : Series Notations
bike_order_copy = bike_order_line_df.copy()

bike_order_copy["frame_material_category_2"] = (
    bike_order_copy["frame_material"] + "_" + bike_order_line_df["category_2"]
)

(bike_order_copy.filter(regex="(^frame_material)|(^cat)", axis=1))

del bike_order_copy

# Method 2 : Assign

(
    bike_order_line_df.assign(
        frame_material_lower=lambda x: x["frame_material"].str.lower()
    ).filter(regex="(^frame_material)|(^cat)", axis=1)
)

# use case
(
    bike_order_line_df[["model", "price"]]
    .drop_duplicates()
    .assign(price=lambda x: np.log(x["price"]))
    .set_index("model")
    .plot(kind="hist")
)
plt.show()

# Searching for values

(
    bike_order_line_df.assign(
        is_super_six=lambda x: x["model"].str.contains("supersix", case=False)
    ).query("is_super_six==True")
)

# Creating binning

pd.cut(bike_order_line_df["price"], bins=3, labels=["high", "medium", "low"])

(
    bike_order_line_df[["model", "price"]]
    .drop_duplicates()
    .assign(
        price_group=lambda x: pd.qcut(
            x["price"], q=3, labels=["high", "medium", "low"]
        )
    )
    .pivot(index="model", columns="price_group", values="price")
)

# 4.0 Grouping
# 4.1 Aggregating (No Grouping)

(
    bike_order_line_df.select_dtypes(exclude="object")
    .drop("order_date", axis=1)
    .sum()
)

# Summary functions

bike_order_line_df["model"].value_counts()

bike_order_line_df.nunique()

bike_order_line_df.isna().sum()  # Provides summary for missing varaibles

(
    bike_order_line_df.select_dtypes(exclude="object")
    .drop("order_date", axis=1)
    .std()
)

# 4.2 Aggregating with grouping

(
    bike_order_line_df.groupby(["state", "city"], as_index=False).agg(
        dict(quantity=np.sum, total_price=[np.sum, np.mean])
    )
)

# 4.2.1 Get the sum and median by groups

summary_df_1 = (
    bike_order_line_df[["category_1", "category_2", "total_price"]]
    .groupby(["category_1", "category_2"])
    .agg(
        total_price=("total_price", "sum"),
        median_price=("total_price", "median"),
    )
    .reset_index()
)

# 4.2.2 Get the  sum of quantity and price by groups

summary_df_2 = (
    bike_order_line_df[["category_1", "category_2", "total_price", "quantity"]]
    .groupby(["category_1", "category_2"])
    .agg(
        total_price=("total_price", "sum"), total_quantity=("quantity", "sum")
    )
    .reset_index()
)


# 4.2.3 Group by and transform

summary_df_3 = (
    bike_order_line_df[["category_2", "order_date", "total_price", "quantity"]]
    .groupby(
        [pd.Grouper(key="order_date", freq="1W"), "category_2"], as_index=False
    )
    .agg("sum")
)

(
    summary_df_3.set_index("order_date")
    .groupby(["category_2"])
    .apply(
        lambda x: (x.total_price - x.total_price.mean())
        / (x.total_price.std())
    )
    .reset_index()
    .pivot(index="order_date", columns="category_2", values="total_price")
)  # .plot


(
    summary_df_3.set_index(["order_date", "category_2"])
    .groupby(level="category_2")
    .transform(lambda x: (x - x.mean()) / (x.std()))
    .reset_index()
)


#

# 4.4 Groupby + Filter

(summary_df_3.groupby("category_2").tail(5))


(summary_df_3.groupby("category_2").apply(lambda x: x.iloc[10:20]))


# 5.0 Renaming
# 5.1 direct


# 6.0 Reshaping
# Data - Aggregating total price by category 1 and bikeshop name

bike_revenue_df = (
    bike_order_line_df[["bikeshop_name", "category_1", "total_price"]]
    .groupby(["bikeshop_name", "category_1"])
    .sum()
    .reset_index()
    .sort_values(by=["total_price"], ascending=False)
    .rename(columns=lambda x: x.replace("_", " ").title())
)


# Pivot
bike_revenue_wider_df = (
    bike_revenue_df.pivot(
        index=["Bikeshop Name"], columns=["Category 1"], values=["Total Price"]
    )
    .reset_index()
    .set_axis(["Bikeshop name", "Mountain", "Road"], axis=1)
)

bike_revenue_wider_df.sort_values(by=["Mountain"]).plot(
    x="Bikeshop name", y=["Mountain", "Road"], kind="barh"
)
plt.show()


usd = currency_format(prefix="$", big_mark=",", precision=0)


bike_revenue_wider_df.sort_values(
    by=["Mountain"], ascending=False
).style.highlight_max().format(
    {"Mountain": lambda x: "$" + usd(x)[0], "Road": lambda x: "$" + usd(x)[0]}
).to_excel("bikeshop_name_revenue.xlsx", index=False)


bike_revenue_wider_df = pd.read_excel("bikeshop_name_revenue.xlsx")
bikeshop_revenue_long_df = pd.melt(
    bike_revenue_wider_df,
    value_vars=["Mountain", "Road"],
    value_name="Revenue",
    var_name="Category 1",
    id_vars="Bikeshop name",
)


bikeshop_order = (
    bikeshop_revenue_long_df.groupby(["Bikeshop name"])
    .sum()
    .sort_values(by="Revenue")
    .index.tolist()
)

## Converting the bikeshop name to category


bikeshop_revenue_long_df["Bikeshop name"] = pd.Categorical(
    bikeshop_revenue_long_df["Bikeshop name"], categories=bikeshop_order
)

plot = (
    ggplot(
        data=bikeshop_revenue_long_df,
        mapping=aes(x="Bikeshop name", y="Revenue", fill="Category 1"),
    )
    + geom_col()
    + coord_flip()
    + facet_wrap("Category 1")
    + theme_minimal()
)


plot.draw(True)


# pivot_table w
# Without columns

pd.pivot_table(
    bike_order_line_df,
    values=["total_price"],
    index="category_1",
    aggfunc=np.sum,
)


pd.pivot_table(
    bike_order_line_df,
    columns="frame_material",
    values=["total_price"],
    index="category_1",
    aggfunc=np.sum,
)


pd.pivot_table(
    bike_order_line_df,
    columns=None,
    values=["total_price"],
    index=["category_1", "frame_material"],
    aggfunc=np.sum,
)

sales_by_cat1_cat2_year_df = bike_order_line_df.assign(
    order_year=lambda x: x["order_date"].dt.year
).pivot_table(
    columns="order_year",
    index=["category_1", "category_2"],
    values=["total_price"],
    aggfunc=np.sum,
)

# unstack

(sales_by_cat1_cat2_year_df.unstack(fill_value=0, level="category_1"))

# melt
sales_by_cat1_cat2_year_df.stack(level="order_year").unstack(
    level=["category_1", "category_2"]
)


# 7.0 Joining

order_line_df = pd.read_excel(raw_folder_path / "orderlines.xlsx")
bike_df = pd.read_excel(raw_folder_path / "bikes.xlsx")


order_line_df = order_line_df.clean_names()
bike_df = bike_df.clean_names()
# merge


pd.merge(
    left=order_line_df,
    right=bike_df,
    left_on="product_id",
    right_on="bike_id",
    how="left",
)

# concat

# Rows
pd.concat([bike_order_line_df.head(n=10), bike_order_line_df.tail(n=10)])


# Columns

df_1 = bike_order_line_df.iloc[:, :5]
df_2 = bike_order_line_df.iloc[:, -5:]

pd.concat([df_1, df_2], axis=1)


# 8.0 SPlit the columns

df2 = (
    bike_order_line_df["order_date"]
    .astype(str)
    .str.split("-", expand=True)
    .set_axis(["order_year", "order_month", "order_day"], axis=1)
)

pd.concat([bike_order_line_df, df2], axis=1)


# 8.1 Combining the columns

df2["order_year"] + "-" + df2["order_month"] + "-" + df2["order_day"]

# 9.0 Apply

# 9.1 Summarize the data

sales_cat2_daily_df = (
    bike_order_line_df[["order_date", "category_2", "total_price"]]
    .set_index("order_date")
    .groupby("category_2")
    .resample("D")
    .agg(total_price=("total_price", "sum"))
)


sales_cat2_daily_df.apply(np.mean)


sales_cat2_daily_df.groupby("category_2").total_price.transform(np.mean)


# 10 pipe

# See the notes
