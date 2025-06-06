# SQL DATABASES (Module 2): Working with SQLAlchemy ----
from gc import collect

# IMPORTS ----
# %%
import pandas as pd
import numpy as np
from path import Path
from typing import List, Dict, Literal, Optional
import sqlalchemy as sql
import janitor  # type: ignore
import os

SELECTED_COLUMN_TO_KEEP: List[str] = [
    "order_id",
    "order_line",
    "order_date",
    "model",
    "quantity",
    "price",
    "total_price",
    "bikeshop_name",
    "location",
    "category_1",
    "category_2",
    "frame_material",
    "city",
    "state",
]


class BikeOrderTransformer:

    def __init__(self, conn_string: str):
        """

        Args:
            conn_string (str): SQLITE connection string.

        """
        self.engine = sql.create_engine(conn_string)

    def collect_data(self, table_name: str) -> pd.DataFrame:
        query = f"SELECT * FROM {table_name}"
        with self.engine.connect() as conn:
            df = pd.read_sql(sql=query, con=conn)
        return df

    def transform_data(self) -> pd.DataFrame:
        # Collect raw tables
        bikes_df = self.collect_data("bikes")
        order_lines_df = self.collect_data("order_lines")
        bike_shop_df = self.collect_data("bike_shops")

        # Transform: Join, Clean, Derive
        bike_order_line_joined_df: pd.DataFrame = order_lines_df.merge(
            bikes_df, how="left", left_on="product_id", right_on="bike_id"
        ).merge(bike_shop_df, how="left", left_on="customer_id", right_on="bikeshop_id")

        bike_order_cleaned_df = (
            bike_order_line_joined_df.deconcatenate_column(  # type: ignore
                "description",
                sep=" - ",
                new_column_names=["category_1", "category_2", "frame_material"],
            )
            .deconcatenate_column(
                "location",
                sep=", ",
                new_column_names=["city", "state"],
                preserve_position=False,
            )
            .assign(total_price=lambda x: x["price"] * x["quantity"])
            .select(SELECTED_COLUMN_TO_KEEP)
        )

        return bike_order_cleaned_df

    @staticmethod
    def save_data(
        df: pd.DataFrame,
        path: Path,
        file_name: str,
        file_type: Literal["csv", "xlsx", "pkl"] = "csv",
    ):

        if not os.path.exists(path):
            os.mkdir(path=path)

        file_path = path / file_name

        if file_type == "csv":
            df.to_csv(file_path, index=False)
        elif file_type == "xlsx":
            df.to_excel(file_path, index=False)
        elif file_type == "pkl":
            df.to_pickle(file_path)
        else:
            raise ValueError(f"Unsupported file type: {file_type}")
        print(f"Saved to: {path}")
