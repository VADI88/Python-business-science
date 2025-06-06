# Databases 

| Feature               | CSV (Comma Separated Values)      | Excel (XLSX)                    | Pickle (`.pkl`)                             |
| --------------------- | --------------------------------- | ------------------------------- | ------------------------------------------- |
| Format Type           | Plain text                        | Binary/ZIP-compressed XML       | Binary (Python-specific serialization)      |
| File Extension        | `.csv`                            | `.xls` / `.xlsx`                | `.pkl`                                      |
| Software Support      | Universal (text tools, R, Python) | Excel, R (via `readxl`), Python | Primarily Python (`pickle`, `joblib`)       |
| Data Structure        | Flat, table-like                  | Tabular + complex structures    | Arbitrary Python objects (dataframes, etc.) |
| Formulas & Formatting | Not supported                     | Fully supported                 | Not applicable                              |
| Size Efficiency       | Smaller                           | Larger (due to formatting)      | Very efficient (compressed binary)          |
| Multisheet Support    | Not supported                     | Supported                       | Not applicable                              |
| Compatibility         | Very high                         | Moderate                        | Low (Python-specific)                       |
| Ease of Use           | Simple                            | Rich features                   | Requires Python environment                 |
| Ideal For             | Data exchange                     | Reports, rich presentation      | Fast, efficient Python data persistence     |




## Automating the task 
- Created a class  `bike_order_transformer`
- Takes database_connection_string and returned the cleaned data that follows below defined steps\
  1.Merges the tables :`bikes`,`bike_shop`, `order_lines`.\
  2.Split the columns like `description` and `location`.\
  3.Calculates `total_price`.\
  4.Selects specific columns `"order_id", "order_line", "order_date", "model", "quantity", "price", "total_price",
    "bikeshop_name", "location", "category_1", "category_2", "frame_material", "city", "state"` to keep.
- We packaged around this class to reuse it.