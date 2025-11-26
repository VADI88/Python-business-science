# Module 4 (Time Series): Profiling Data ----


import datetime

import matplotlib.pyplot as plt
import numpy as np

# IMPORTS
import pandas as pd
from path import Path

from transformer.bike_order_transformer import BikeOrderTransformer

database_folder_path = Path("data/database")


bike_order_line_df = BikeOrderTransformer().transform_data()

# 1.0 Date basics

# Conversion
type("2025-01-23")

pd.to_datetime("2025-01-23")  #  Timestamp('2025-01-23 00:00:00')

pd.to_datetime("2025-01-23").to_period(
    freq="W"
)  # Period('2025-01-20/2025-01-26', 'W-SUN')

# accessing elements

bike_order_line_df.order_date = pd.to_datetime(bike_order_line_df.order_date)
# bike_order_line_df.order_date.dt.month - returns numeric values 1-12
# bike_order_line_df['order_date'].dt.month_name() returns labels for months
#
#
#
# bike_order_line_df['order_date'].dt.day  returns numeric values 1-30/31
# bike_order_line_df['order_date'].dt.day_name()  returns numeric Monday to Friday

# date maths
today = datetime.date.today()

today + pd.Timedelta(days=1)

today + pd.Timedelta(minutes=30)

today + pd.DateOffset(years=1)

# Duration
one_from_today = today + pd.Timedelta(weeks=52)

(one_from_today - today) / pd.Timedelta(days=1)

# Date Sequences

pd.date_range(start=pd.to_datetime("2011-01"), periods=10, freq="2D")

pd.date_range(start=pd.to_datetime("2011-01"), periods=10, freq="1W")

# 2.0 Period

# Convert to timestamp
# collapase the datetime to period based on frequecny arg
bike_order_line_df["order_date"].dt.to_period(freq="D")  #  Daily
bike_order_line_df["order_date"].dt.to_period(freq="W")  #  Weekly
bike_order_line_df["order_date"].dt.to_period(freq="M")  #  Monthly
bike_order_line_df["order_date"].dt.to_period(freq="Y")  #  Year
bike_order_line_df["order_date"].dt.to_period(freq="Q")  #  Quaterly

# Get the frequency

# bike_order_line_df["order_date"].dt.to_period(freq="Q").dt.freq

# Sampling

bike_order_m_df = (
    bike_order_line_df[["order_date", "total_price"]]
    .set_index("order_date")
    .resample("MS", kind="timestamp")
    .sum()
)

bike_order_cat2_m_df = (
    bike_order_line_df[["order_date", "category_2", "total_price"]]
    .groupby(["category_2", "order_date"])
    .agg(np.sum)
    .unstack("category_2")
    .resample("M", kind="period")
    .agg(np.sum)
)

# bike_order_line_df[['order_date', 'category_2', 'total_price']]\
#  .groupby(['category_2', pd.Grouper(key = 'order_date',freq='M')])\
# .agg(np.sum)\
# .unstack('category_2')\
# .reset_index()\
# .assign(order_date = lambda x:x['order_date'].dt.to_period('M'))\
# .set_index('order_date')

# Measuring change

# single (No Group)

bike_order_m_df.assign(
    total_price_lag_1=lambda x: x["total_price"].shift(1)
).assign(diff=lambda x: x["total_price"] - x["total_price_lag_1"]).plot(
    y="diff"
)

# Same same but different

bike_order_m_df.apply(lambda x: (x - x.shift(1)) / (x.shift(1))).plot()
plt.show()
# Multiple Groups

bike_order_cat2_m_df.apply(lambda x: (x - x.shift(1)) / (x.shift(1))).plot()

plt.show()

# Difference from first timestamp


bike_order_m_df.apply(lambda x: (x - x[0]) / (x[0])).plot()
plt.show()

# Difference from multiple first timestamp


bike_order_cat2_m_df.apply(lambda x: (x - x[0]) / (x[0])).plot()

plt.show()


# Cumulative Cal.
bike_order_m_df.reset_index().groupby(
    pd.Grouper(key="order_date", freq="YS")
).total_price.sum().cumsum().reset_index().assign(
    order_date=lambda x: x["order_date"].dt.to_period("Y")
).plot(kind="bar", y="total_price", x="order_date")


bike_order_cat2_m_df.resample("Y").sum().cumsum().plot(
    kind="bar", stacked=True
)


# MOving calculations
# single
bike_order_m_df.assign(
    total_price_roll3=lambda x: x["total_price"]
    .rolling(window=3, center=True, min_periods=1)
    .mean()
).plot()


bike_order_cat2_m_df.apply(
    lambda x: x.rolling(window=3, center=True, min_periods=1).mean()
).plot()


bike_order_cat2_m_df.rolling(
    window=3, center=True, min_periods=1
).mean().plot()
