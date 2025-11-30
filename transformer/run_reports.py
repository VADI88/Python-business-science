from pydantic import BaseModel, ConfigDict, Field, model_validator
import pandas as pd
from path import Path
from typing import Literal
import papermill as pm  # type: ignore
from traitlets.config import Config
from settings import make_nbconvert_config
from nbconvert.writers import FilesWriter
from nbconvert.exporters import HTMLExporter, PDFExporter
from nbconvert.preprocessors import TagRemovePreprocessor
from helper.logger import Log

log = Log(
        log_dir="logs/run_reports", log_name="run_reports.log"
).get_logger()


class RunReport(BaseModel):
    data: pd.DataFrame
    report_info: Literal[
        "Total Revenue", "Category 1", "Category 2", "Bikeshop"
    ]
    title: str = None  # type: ignore
    template_path: Path = Field(
            default=Path("reports/template/jupyter_report_template.ipynb")
    )
    output_path: str = None  # type: ignore
    format: Literal["html", "pdf"] = "html"
    config: Config = make_nbconvert_config()
    file_name: str = None  # type: ignore
    file_dir_path: str = None  # type: ignore

    model_config = ConfigDict(arbitrary_types_allowed=True)

    def model_post_init(self, __context) -> None:
        if self.title is None:
            self.title = f"Sales Forecast : {self.report_info}"

        if self.output_path is None:
            self.output_path = Path(
                    f"reports/output/sales_report_{self.report_info.lower().replace(' ', '_')}.ipynb"
            )

        self.file_name = (
                f"sales_report_{self.report_info.lower().replace(' ', '_')}"
        )

        if self.format == "html":
            self.config.HTMLExporter.preprocessors = [TagRemovePreprocessor()]
            self.file_dir_path = Path("reports/report_Html/")

        else:
            self.config.HTMLExporter.preprocessors = [TagRemovePreprocessor()]
            self.file_dir_path = Path("reports/report_Pdf/")

    @model_validator(mode="after")
    def validate_fields(self):
        if self.data.empty:
            raise ValueError("Input 'data' must not be empty.")

        if self.data.shape[1] == 0:
            raise ValueError("Input 'data' must have at least one column.")

        if self.data.shape[0] == 0:
            raise ValueError("Input 'data' must have at least one row.")

        if self.format not in ["html", "pdf"]:
            raise ValueError("Input 'format' must be 'html' or 'pdf'.")

        return self

    def _prepare_ids(self) -> list:
        return_ids = self.data[
            self.data["id"].str.startswith(self.report_info)
        ]["id"].unique()

        return list(return_ids)

    def build_param(self):
        log.info("Build Parameters")

        params = {
                "ids"  : list(self._prepare_ids()),
                "data" : self.data.to_json(),
                "title": self.title,
        }
        return params

    def execute(self):
        log.info("Papermill is executing")
        params = self.build_param()

        pm.execute_notebook(
                input_path=self.template_path,
                output_path=self.output_path,
                parameters=params,
                report_mode=True,
        )

        return self

    def filewriter(self, body, resources):
        log.info(f"Files save to {self.file_dir_path} under {self.file_name}.{self.format}")

        self.config.FilesWriter.build_directory = str(self.file_dir_path)
        fw = FilesWriter(config=self.config)
        fw.write(body, resources, notebook_name=self.file_name)

        return self

    def convert(self) -> str:
        log.info(f"Converting IPYNB format to {self.format}")
        if self.format == "html":
            (body, resources) = HTMLExporter(config=self.config).from_filename(
                    self.output_path
            )
        else:
            (body, resources) = PDFExporter(config=self.config).from_filename(
                    self.output_path
            )

        self.filewriter(body, resources)

        return f"File Converted Successfully to {self.format} and saved to {self.file_dir_path}"  # type: ignore
