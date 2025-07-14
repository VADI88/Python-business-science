# IMPORTS

from typing import Literal, Optional, List, Any

import numpy as np
import pandas as pd
from path import Path
from pydantic import validate_call, ConfigDict

from transformer.bike_order_transformer import BikeOrderTransformer

database_folder_path = Path("data/database")

raw_folder_path = Path("data/data_raw")

conn_string = f"sqlite:///{database_folder_path}/bikes_order_database.sqlite"

bike_order_line_df = BikeOrderTransformer(conn_string).transform_data()
bike_order_line_df["order_date"] = pd.to_datetime(bike_order_line_df["order_date"])

bike_order_line_df[["category_2", "order_date", "total_price"]].groupby(
    ["category_2", pd.Grouper(key="order_date", freq="MS")]
).aggregate(np.sum).unstack("category_2").reset_index().assign(
    order_date=lambda x: x["order_date"].dt.to_period()
).set_index(
    "order_date"
)


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

    Returns:

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


summarize_by_time(
    data=bike_order_line_df,
    date_column="order_date",
    groups=["category_1", "category_2"],
    rules="MS",
    value_column=["total_price", "price"],
)
