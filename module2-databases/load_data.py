# SQL DATABASES (Module 2): Working with SQLAlchemy ----
from operator import index

# %%
import pandas as pd
from path import Path
import sqlalchemy as sql
import os
import janitor  # type: ignore

# Creating Database folder

# %%
database_folder_path = Path("data/database")
raw_folder_path = Path("data/data_raw")

if not os.path.exists(database_folder_path):
    os.mkdir(database_folder_path)

# CREATING A DATABASE ----

# Instantiate a database

# %%
engine = sql.create_engine(
    f"sqlite:///{database_folder_path}/bikes_order_database.sqlite"
)

conn = engine.connect()

# Read Excel Files
# %%

bikes_df = pd.read_excel(raw_folder_path / "bikes.xlsx").clean_names()  # type: ignore

bike_shop_df = pd.read_excel(
    raw_folder_path / "bikeshops.xlsx"
).clean_names()  # type: ignore

order_lines_df = pd.read_excel(
    io=raw_folder_path / "orderlines.xlsx", converters={"order.date": str}
).clean_names()  # type: ignore

# Create tables


bikes_df.to_sql("bikes", con=conn, index=False, if_exists="replace")

bike_shop_df.to_sql("bike_shops", con=conn, index=False, if_exists="replace")

order_lines_df.drop("unnamed_0", axis=1).to_sql(
    "order_lines", con=conn, index=False, if_exists="replace"
)
