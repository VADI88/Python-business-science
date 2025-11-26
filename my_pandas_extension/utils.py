import pandas as pd
import pandas_flavor as pf  # type: ignore
from pydantic import ConfigDict, validate_call
from functools import wraps
from typing import Any, Callable, List, Literal, ParamSpec, TypeVar
import janitor  # type: ignore


@pf.register_dataframe_method
@validate_call(config=ConfigDict(arbitrary_types_allowed=True))
def prepare_data(data: pd.DataFrame, id_column: str, date_column: str):
    if data is None:
        raise ValueError("No data available to prepare.")

    data = data.rename(columns={id_column: "id", date_column: "date"})

    data = data.reorder_columns(["id", "date"])

    return data


P = ParamSpec("P")
R = TypeVar("R")


def with_db_connection(func: Callable[P, R]) -> Callable[P, R]:
    """Injects `conn` argument into the wrapped method."""

    @wraps(func)
    def wrapper(self, *args: P.args, **kwargs: P.kwargs) -> R:
        with self.engine.connect() as conn:
            return func(self, conn, *args, **kwargs)

    return wrapper  # type: ignore
