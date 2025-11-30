# IMPORTS

import glob
import pathlib
from tqdm import tqdm
from settings import make_nbconvert_config

from nbconvert.preprocessors import TagRemovePreprocessor
from nbconvert.exporters import HTMLExporter, PDFExporter
from nbconvert.writers import FilesWriter


config = make_nbconvert_config()

# get the files

files = glob.glob("reports/output/sales_report*.ipynb")

config.PDFExporter.preprocessors = [TagRemovePreprocessor()]

# Iterate through files ----

for file in tqdm(files):
    file_path = pathlib.Path(file)
    file_name = file_path.stem
    file_dir = file_path.parents[0]

    (body, resources) = HTMLExporter(config=config).from_filename(file_path)
    file_dir_html = str(file_dir) + "_html"
    config.FilesWriter.build_directory = str(file_dir_html)
    fw = FilesWriter(config=c)
    fw.write(body, resources, notebook_name=file_name)
