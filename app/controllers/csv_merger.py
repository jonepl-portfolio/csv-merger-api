import os
import pandas as pd
from typing import List
from werkzeug.datastructures import FileStorage

from logger.logger_factory import LoggerFactory
from services.dataframe_service import DataframeService
from constants.shared_consts import TEMP_PATH, FileExtensions

logger = LoggerFactory.get_logger(__name__)


class CsvMerger:
    def __init__(self) -> None:
        self.df = pd.DataFrame()

    def merge_csvs(self, storages: List[FileStorage]) -> None:
        for storage in storages:
            next_df = DataframeService.convert_to_dataframe(storage)
            self.df = DataframeService.merge_dataframes(self.df, next_df)

    def get_merged_csvs(self, group_name: str):
        r"""
        Converts dataframe into csv
        """
        csv = self.df.to_csv(index=False)

        if not os.path.exists(TEMP_PATH):
            os.makedirs(TEMP_PATH)

        filename = f"{group_name}{FileExtensions.CSV.value}"
        reportPath = os.path.join(TEMP_PATH, filename)

        try:
            file = open(reportPath, "w")
            file.write(csv)
        except Exception as e:
            errMsg = f"Error occurred when opening/writing file. Exceptions {e}"
            logger.critical(errMsg)
            raise Exception(errMsg)
        finally:
            if not file.closed:
                file.close()

        return reportPath
