from __future__ import annotations

from typing import Literal

import pandas as pd
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy import create_engine, inspect
from sqlalchemy.engine import Engine

from settings import CONN_STRING, SQL_DTYPES
from my_pandas_extension.utils import with_db_connection, prepare_data


class DataAccess(BaseModel):
    """
    Data Access class for writing and reading forecast-related data.
    """

    engine: Engine = Field(default_factory=lambda: create_engine(CONN_STRING))

    model_config = ConfigDict(arbitrary_types_allowed=True)

    # ----------------------------------------------------------------
    # Validation (performed only ON-DEMAND during write)
    # ----------------------------------------------------------------
    def _validate_dataframe(self, df: pd.DataFrame) -> None:
        required = {
            self.id_column,
            self.date_column,
            "value",
            "prediction",
            "ci_lo",
            "ci_hi",
        }
        df_cols = set(df.columns)

        missing = required - df_cols
        extra = df_cols - required

        if missing or extra:
            raise ValueError(
                f"DataFrame must contain columns: {sorted(required)}\n"
                f"Missing: {sorted(missing)}\n"
                f"Extra: {sorted(extra)}"
            )

    def table_exists(self, table_name) -> bool:
        inspector = inspect(self.engine)
        return table_name in inspector.get_table_names()

    @with_db_connection
    def write_data_to_db(
        self,
        conn,
        data: pd.DataFrame | None,  # optional until writing
        id_column: str,
        date_column: str,
        table_name: str = "forecast",
        *,
        prepare: bool = False,
        if_exists: Literal["fail", "replace", "append"] = "fail",
        **kwargs,
    ) -> None:
        if data is None:
            raise ValueError("No data provided for writing.")

        df = data.copy()

        # optional preprocessing step
        if prepare:
            df = prepare_data(
                data=df, id_column=id_column, date_column=date_column
            )  # type: ignore

        # validate dataframe ONLY at write time
        self._validate_dataframe(df)

        # write to database
        df.to_sql(
            name=table_name,
            con=conn,
            if_exists=if_exists,
            dtype=SQL_DTYPES,
            index=False,
            **kwargs,
        )

    @with_db_connection
    def read_data_from_db(
        self,
        conn,
        table_name: str | None = None,
        query: str | None = None,
        **kwargs,
    ) -> pd.DataFrame:
        # Ensure table exists before reading
        if not self.table_exists(table_name):
            raise ValueError(
                f"Table '{table_name}' does not exist in the database."
            )

        # Default query: select all
        if query is None:
            query = f"SELECT * FROM {table_name}"  # type: ignore

        return pd.read_sql(query, con=conn, **kwargs)
