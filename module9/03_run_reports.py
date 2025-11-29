from pydantic import BaseModel, ConfigDict, Field, model_validator
import pandas as pd
from path import Path
from typing import Literal
import papermill as pm  # type: ignore


class RunReport(BaseModel):
    data: pd.DataFrame
    report_info: Literal[
        "Total Revenue", "Category 1", "Category 2", "Bikeshop"
    ]
    title: str
    template_path: Path = Field(
        default=Path("module9/template/jupyter_report_template.ipynb")
    )
    output_path: str

    def model_post_init(self, __context) -> None:
        if self.title is None:
            self.title = f"Sales Forecast : {self.report_info}"

        if self.output_path is None:
            self.output_path = Path(
                f'module9/reports/sales_report_{self.report_info.lower().replace("", "_")}.ipynb"'
            )

    @model_validator(mode="after")
    def validate_fields(self):
        if self.data.empty:
            raise ValueError("Input 'data' must not be empty.")

        if self.data.shape[1] == 0:
            raise ValueError("Input 'data' must have at least one column.")

        if self.data.shape[0] == 0:
            raise ValueError("Input 'data' must have at least one row.")

        return self

    config = ConfigDict(arbitrary_types_allowed=True)

    def _prepare_ids(self) -> list:
        return_ids = self.data[
            self.data["id"].str.startswith(self.report_info)
        ]["id"].unique()

        return list(return_ids)

    def build_param(self):
        params = {
            "ids": list(self._prepare_ids()),
            "data": self.data.to_json(),
            "title": self.title,
        }
        return params

    def execute(self) -> None:
        params = self.build_param()

        pm.execute_notebook(
                input_path=self.template_path,
                output_path=self.output_path,
                parameters=params,
                report_mode=True,
        )

        pass
