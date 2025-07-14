# IMPORTS
import pandas as pd
from transformer.bike_order_transformer import BikeOrderTransformer
from path import Path
import numpy as np
from pydantic import validate_call, StrictFloat, ConfigDict, Field, ValidationError
from pandas import Series
from typing import Literal, Annotated

database_folder_path = Path("data/database")

raw_folder_path = Path("data/data_raw")

conn_string = f"sqlite:///{database_folder_path}/bikes_order_database.sqlite"

bike_order_line_df = BikeOrderTransformer(conn_string).transform_data()

# 1.0 EXAMINING FUNCTIONS ----

# Pandas Series Function
# ?pd.Series.max
# ?np.max

bike_order_line_df["total_price"].max()


# Pandas Data Frame Function
# ?pd.DataFrame.aggregate


# 2.0 OUTLIER DETECTION FUNCTION ----
# - Works with a Pandas Series


@validate_call(config=ConfigDict(arbitrary_types_allowed=True))
def detect_outliers(
    x: pd.Series,
    iqr_multiplier: Annotated[StrictFloat, Field(strict=True, gt=0)] = 1.5,
    how: Literal["both", "upper", "lower"] = "both",
) -> Series:
    """
    Detect outliers using the IQR (Inter Quartile Range) Methods.

    Args:
        x (Pandas Series) : Series
        iqr_multiplier(Float) : A multiplier used to modify the sensitivity. Must be positive. Defaults values = 1.5
        how (Literal[str] ):
            one of "both", "upper" , "lower". Default to "both"
            - "both" : flags both upper limit and lower limit
            - "upper" : flags only upper limit
            - "lower" : flags only lower limit

    Returns:
        Series of True or False

    """
    # IQR Method
    q75 = np.quantile(x, 0.75)
    q25 = np.quantile(x, 0.25)
    iqr = q75 - q25

    lower_limit = q25 - iqr_multiplier * iqr
    upper_limit = q75 + iqr_multiplier * iqr
    if how == "both":
        outliers = (x <= lower_limit) | (x >= upper_limit)
    elif how == "upper":
        outliers = x >= upper_limit
    else:
        outliers = x <= lower_limit

    return outliers
