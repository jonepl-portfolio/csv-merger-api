import os
import pandas as pd

from logger.logger_factory import LoggerFactory

logger = LoggerFactory.get_logger(__name__)


class CsvService:

    @staticmethod
    def sanitize_csv(csv_path: str) -> pd.DataFrame:
        """Converts csv into Pandas Dataframe while removing metadata and blank rows

        params:
            csv_path (str): a file paths to csv files
        """
        if not os.path.exists(csv_path):
            errMsg = f"Unable to find file {csv_path}"
            logger.critical(errMsg)
            raise FileNotFoundError(errMsg)

        df = pd.read_csv(csv_path, skiprows=0, index_col=False)
        return df
