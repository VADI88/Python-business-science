# Pandas Core (Module 3): Data Structures ----

# IMPORTS

from path import Path

from transformer.bike_order_transformer import BikeOrderTransformer


bike_order_line_df = BikeOrderTransformer().transform_data()

type(bike_order_line_df)  # <class 'pandas.core.frame.DataFrame'>

type(bike_order_line_df).mro()

# Attributes
bike_order_line_df.shape
bike_order_line_df.columns


# Methods

bike_order_line_df.query("model =='Jekyll Carbon 2'")

# Pandas core structure

type(bike_order_line_df["order_date"])  # <class 'pandas.core.series.Series'>


type(bike_order_line_df["order_date"].values)  # <class 'numpy.ndarray'>


# 2.0
