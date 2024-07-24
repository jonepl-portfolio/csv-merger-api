import os
import zipfile
from typing import List

from logger.logger_factory import LoggerFactory
from constants.shared_consts import (
    TEMP_PATH,
    CONSOLIDATED_CSV_ZIP,
    FileExtensions,
    FileTypes,
)

logger = LoggerFactory.get_logger(__name__)


class FileDetails:
    name: str
    path: str
    consolidated_path: str

    def __init__(self, filename, filepath) -> None:
        self.name = filename
        self.path = filepath


class FileService:
    file_details: List[FileDetails]
    consolidated_path: str

    def __init__(self) -> None:
        self.file_details = []
        self.consolidated_path = None

    def add_file_details(self, filepath: str, file_group_name):
        """Append file details and to FileService

        params:
            - filepath (str): existing filepath
            - file_group_name (str): name for the group of files being added
        """
        self.file_details.append(FileDetails(file_group_name, filepath))
        logger.info(f"Added file details: {file_group_name}, {filepath}")

    def get_consolidated_filepath(self) -> str:
        """Returns consolidated filepath from saved file_details"""
        if len(self.file_details) == 1:
            logger.debug("Single file detail found, returning the single file path")
            return self.file_details[0].path
        else:
            zip_path: str = os.path.join(TEMP_PATH, CONSOLIDATED_CSV_ZIP)
            try:
                with zipfile.ZipFile(zip_path, "w") as zipMe:
                    for file in self.file_details:
                        zipMe.write(file.path, compress_type=zipfile.ZIP_DEFLATED)
                logger.info(f"Consolidated files into zip: {zip_path}")
            except Exception as e:
                logger.error(f"Error occurred while creating zip file: {str(e)}")
                raise
            return zip_path

    def get_filename(self):
        """Returns the appropriate filename based on file details."""
        if len(self.file_details) == 1:
            filename = self.file_details[0].name + FileExtensions.CSV.value
            logger.debug(f"Single file detail found, returning filename: {filename}")
            return filename
        else:
            logger.debug(
                "Multiple file details found, returning consolidated zip filename"
            )
            return CONSOLIDATED_CSV_ZIP

    def get_file_type(self):
        """Returns the appropriate file type based on file details."""
        if len(self.file_details) == 1:
            file_type = FileTypes.CSV.value
            logger.debug(f"Single file detail found, returning file type: {file_type}")
            return file_type
        else:
            file_type = FileTypes.ZIP.value
            logger.debug("Multiple file details found, returning file type: ZIP")
            return file_type

    def get_filepaths(self):
        """Returns a list of file paths from saved file details."""
        filepaths = [file.path for file in self.file_details]
        logger.debug(f"Returning file paths: {filepaths}")
        return filepaths
