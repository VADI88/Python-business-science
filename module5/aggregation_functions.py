# IMPORTS
from typing import Annotated, Literal

import numpy as np
import pandas as pd
from pandas import Series
from path import Path
from pydantic import ConfigDict, Field, StrictFloat, validate_call

from transformer.bike_order_transformer import BikeOrderTransformer

database_folder_path = Path("data/database")


bike_order_line_df = BikeOrderTransformer().transform_data()

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
