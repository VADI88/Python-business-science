# Module 2 (Pandas Import): Importing Files

# %%
import pandas as pd
from path import Path


# 1.0 FILES ----
wrangled_folder_path = Path("data/data_wrangled")

bike_order_cleaned_df = pd.read_pickle(
    wrangled_folder_path / "bike_order_line_cleaned.pkl"
)

# Similarly we can import csv and excel. But we need to modify the datatypes. Read the notes for more info on
# difference among these
