from typing import Literal, Optional, List, Any

import numpy as np
import pandas as pd
from pydantic import validate_call, StrictFloat, ConfigDict, Field, ValidationError
from typing import Literal, Annotated
import pandas_flavor as pf  # type: ignore


@pf.register_dataframe_method
@validate_call(config=ConfigDict(arbitrary_types_allowed=True))
def summarize_by_time(
    data: pd.DataFrame,
    value_column: List[str],
    date_column: Optional[str] = None,
    groups: Optional[Any] = None,
    rules: Literal["D", "MS", "YS"] = "D",
    agg_func=np.sum,
    time_format: Literal["timestamp", "period"] = "timestamp",
    na_value: int = 0,
    *args,
    **kwargs,
) -> pd.DataFrame:
    """

    Args:
        data (pd.DataFrame):
        date_column (str):
        value_column (List[str]):
        groups (Optional[Any]):
        rules (Literal[str]):
        agg_func ():
        time_format ():
        na_value ():
        *args ():
        **kwargs ():

    Returns: pd.DataFrame

    """
    group_by_column: List = []

    if date_column:
        datecolumn = pd.Grouper(key=date_column, freq=rules)
        group_by_column.insert(0, datecolumn)

    if groups:
        for grp in groups:
            group_by_column.append(grp)

    if group_by_column:
        data = data.groupby(group_by_column)

    data = data[value_column].agg(func=agg_func, *args, **kwargs)

    if groups:
        data = data.unstack(groups)  # type: ignore

    if time_format == "period":
        data.index = data.index.to_period()

    data = data.fillna(value=na_value)

    return data


@pf.register_dataframe_method
@validate_call(config=ConfigDict(arbitrary_types_allowed=True))
def detect_outliers(
    x: pd.Series,
    iqr_multiplier: Annotated[StrictFloat, Field(strict=True, gt=0)] = 1.5,
    how: Literal["both", "upper", "lower"] = "both",
) -> pd.Series:
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
