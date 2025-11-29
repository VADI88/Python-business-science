# Core package
import pandas as pd
import numpy as np
import papermill as pm  # type: ignore
from path import Path

from transformer.data_access import DataAccess

# COLLECT DATA
db_access = DataAccess()

all_forecasts_df = db_access.read_data_from_db(table_name="forecast")  # type: ignore

# 2.0 Setup


reports_directory = Path("module9/reports")

if not reports_directory.exists():
    print(
        "Creating reports directory at {}".format(reports_directory.absolute())
    )
    reports_directory.mkdir()


def prepare_data_for_automation(data, columns_value):
    return_ids = data[data["id"].str.startswith(columns_value)]["id"].unique()

    return return_ids


# 3.0 MAKE JUPYTER TEMPLATE
# - Convert Analysis to a Papermill Template
# - Parameterize key variables:
#   - ids
#   - title
#   - data: Note that data will be passed as json


ids_set = ["Total Revenue", "Category 1", "Category 2", "Bikeshop"]

template_path = Path("module9/template/jupyter_report_template.ipynb")

output_path = "module9/reports/sales_report_{}.ipynb"

for i, id_value in enumerate(ids_set):
    params = {
        "ids": list(prepare_data_for_automation(all_forecasts_df, id_value)),
        "data": all_forecasts_df.to_json(),
        "title": f"Sales Forecast: {id_value}",
    }

    pm.execute_notebook(
        input_path=template_path,
        output_path=Path(
            output_path.format(id_value.lower().replace(" ", "_"))
        ),
        parameters=params,
        report_mode=True,
    )
