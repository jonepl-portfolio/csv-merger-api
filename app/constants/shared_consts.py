import os
from enum import Enum

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__)).split("app/")[0]
APPLICATION_ROOT = os.path.join(PROJECT_ROOT, "app")
TEMP_DIR = "uploaded"
CONSOLIDATED_CSV_ZIP = "consolidated-csvs.zip"

CONSOLIDATED_ZIP_PATH = os.path.join(TEMP_DIR, CONSOLIDATED_CSV_ZIP)
TEMP_PATH = os.path.join(APPLICATION_ROOT, TEMP_DIR)


class FileTypes(Enum):
    CSV = "csv"
    ZIP = "zip"


class FileExtensions(Enum):
    CSV = ".csv"
    ZIP = ".zip"
