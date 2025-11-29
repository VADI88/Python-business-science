from typing import (
    Annotated,
    Hashable,
    List,
    Literal,
    Optional,
    Sequence,
    Union,
)

import numpy as np
import pandas as pd
import pandas_flavor as pf  # type: ignore
from pandas.core.groupby.generic import DataFrameGroupBy
from pydantic import ConfigDict, Field, StrictFloat, validate_call

GroupKeys = Sequence[Hashable]
ValueCols = Sequence[str]


@pf.register_dataframe_method
@validate_call(config=ConfigDict(arbitrary_types_allowed=True))
def summarize_by_time(
    data: pd.DataFrame,
    value_column: ValueCols,
    date_column: Optional[str] = None,
    wide_format: bool = True,
    groups: Optional[GroupKeys] = None,
    rules: Literal["D", "MS", "QE", "Q", "YS"] = "D",
    agg_func: Union[str, callable] = "sum",
    time_format: Literal["timestamp", "period"] = "timestamp",
    na_value: int = 0,
    *args,
    **kwargs,
) -> pd.DataFrame:
    """
    Summarize values grouped by time period and optional group keys.
    """

    group_by_column: List[Union[pd.Grouper, Hashable]] = []

    # Add time grouper
    if date_column is not None:
        group_by_column.append(pd.Grouper(key=date_column, freq=rules))

    # Add grouping columns
    if groups is not None:
        group_by_column.extend(groups)

    grouped: Union[pd.DataFrame, DataFrameGroupBy]

    # Apply grouping if needed
    if group_by_column:
        grouped = data.groupby(group_by_column)
    else:
        grouped = data

    # Aggregate
    aggregated = grouped[value_column].agg(agg_func, *args, **kwargs)

    # Unstack group levels
    if groups is not None:
        aggregated = aggregated.unstack(list(groups))

    # Convert to long format if required
    if not wide_format and groups is not None:
        aggregated = aggregated.stack(list(groups))

    # Change index to PeriodIndex if needed
    if time_format == "period" and wide_format:
        if isinstance(aggregated.index, pd.DatetimeIndex):
            aggregated.index = aggregated.index.to_period()

    # Fill NA values
    aggregated = aggregated.fillna(na_value)

    return pd.DataFrame(aggregated)


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
