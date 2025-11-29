from typing import List

from path import Path
from sqlalchemy.types import Numeric, String

database_folder_path = Path("data/database")
CONN_STRING = f"sqlite:///{database_folder_path}/bikes_order_database.sqlite"

SQL_DTYPES = {
    "id": String(),
    "date": String(),
    "value": Numeric(),
    "prediction": Numeric(),
    "ci_lo": Numeric(),
    "ci_hi": Numeric(),
}


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
