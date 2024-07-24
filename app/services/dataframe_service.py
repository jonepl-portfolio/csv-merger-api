import pandas as pd
from werkzeug.datastructures import FileStorage

from logger.logger_factory import LoggerFactory

logger = LoggerFactory.get_logger(__name__)


class DataframeService:

    @staticmethod
    def convert_to_dataframe(storage: FileStorage) -> pd.DataFrame:
        """Converts csv into Pandas Dataframe while removing metadata and blank rows

        params:
            csv_path (str): a file paths to csv files
        """
        df: pd.DataFrame = pd.read_csv(storage.stream, skiprows=0, index_col=False)
        return df

    @staticmethod
    def merge_dataframes(old_df: pd.DataFrame, new_df: pd.DataFrame) -> pd.DataFrame:
        """Merges two Pandas Dataframes

        params:
            old_df (Dataframe): a Pandas dataframe
            new_df (Dataframe): a Pandas dataframe
        """
        dups = old_df.loc[old_df.duplicated()]
        newDups = new_df.loc[new_df.duplicated()]

        # Append new and old orders and remove duplicates
        merged_df = pd.concat([old_df, new_df], ignore_index=False).drop_duplicates(
            keep="last"
        )

        # Append individual duplicate records to the merge dataframe
        merged_df = pd.concat([merged_df, dups])
        merged_df = pd.concat([merged_df, newDups])

        return merged_df

    # @staticmethod
    # def is_dataframe_valid(df: pd.DataFrame, expected_headers: List[dict]):
    #     for header in expected_headers:
    #         found = [option for option in header["options"] if option in df.columns]
    #         if len(found) == 0:
    #             return False

    #     return True

    # @staticmethod
    # def convert_pandas_date_to_date_str(date: pd.Timestamp):
    #     dtStr = None
    #     if isinstance(date, pd.Timestamp):
    #         dt: datetime = date.to_pydatetime()
    #         dtStr = dt.strftime("%m/%d/%Y")
    #     else:
    #         err_msg = f"Invalid date: {date} passed. Can not convert to date string."
    #         logger.critical(err_msg)
    #         raise TypeError(err_msg)

    #     return dtStr

    # @staticmethod
    # def __sanitize_csv(csv_path: str) -> pd.DataFrame:
    #     """Converts csv into Pandas Dataframe while removing metadata and blank rows

    #     params:
    #         csv_path (str): a file paths to csv files
    #     """
    #     if not os.path.exists(csv_path):
    #         err_msg = f"Unable to find file {csv_path}"
    #         logger.critical(err_msg)
    #         raise FileNotFoundError(err_msg)

    #     df = pd.read_csv(csv_path, skiprows=0, index_col=False)
    #     return df
