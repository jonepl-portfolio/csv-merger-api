import os
import pytest
import shutil
import zipfile

from app.services.file_service import FileService
from app.constants.shared_consts import TEMP_PATH, CONSOLIDATED_CSV_ZIP, FileTypes


# Fixture for setup and teardown of test environment
@pytest.fixture
def setup_files():
    # Create a temporary directory for the test files
    os.makedirs(TEMP_PATH, exist_ok=True)

    # Create temporary files for testing
    file1_path = os.path.join(TEMP_PATH, "file1.csv")
    file2_path = os.path.join(TEMP_PATH, "file2.csv")
    file3_path = os.path.join(TEMP_PATH, "file3.csv")

    with open(file1_path, "w") as file1:
        file1.write("col1,col2\n1,2\n")
    with open(file2_path, "w") as file2:
        file2.write("col1,col2\n3,4\n")
    with open(file3_path, "w") as file3:
        file3.write("col1,col2\n5,6\n")

    # Provide file paths to the test function
    yield file1_path, file2_path, file3_path

    # Cleanup: remove the test directory and its contents
    shutil.rmtree(TEMP_PATH)


# Integration test for FileService.get_consolidated_filepath
def test_get_consolidated_filepath(setup_files):
    file1_path, file2_path, _ = setup_files
    service = FileService()

    # Add two files to the service
    service.add_file_details(file1_path, "file1")
    service.add_file_details(file2_path, "file2")

    # Get the consolidated filepath
    consolidated_filepath = service.get_consolidated_filepath()

    # Assert that the consolidated path is the expected ZIP file path
    expected_zip_path = os.path.join(TEMP_PATH, CONSOLIDATED_CSV_ZIP)
    assert consolidated_filepath == expected_zip_path

    # Verify that the ZIP file was created
    assert os.path.exists(consolidated_filepath)

    # Check the content of the ZIP file
    with zipfile.ZipFile(consolidated_filepath, "r") as zip_file:
        zip_content = zip_file.namelist()
        assert normalize_path(os.path.join(TEMP_PATH, "file1.csv")) in zip_content
        assert normalize_path(os.path.join(TEMP_PATH, "file2.csv")) in zip_content


# Integration test for FileService.get_filename
def test_get_filename(setup_files):
    file1_path, file2_path, _ = setup_files
    service = FileService()

    # Test with one file added
    service.add_file_details(file1_path, "file1")
    filename = service.get_filename()
    assert filename == "file1.csv"

    # Test with multiple files added
    service.add_file_details(file2_path, "file2")
    filename = service.get_filename()
    assert filename == "consolidated-csvs.zip"


# Integration test for FileService.get_file_type
def test_get_file_type(setup_files):
    file1_path, file2_path, _ = setup_files
    service = FileService()

    # Test with one file added
    service.add_file_details(file1_path, "file1")
    file_type = service.get_file_type()
    assert file_type == FileTypes.CSV.value

    # Test with multiple files added
    service.add_file_details(file2_path, "file2")
    file_type = service.get_file_type()
    assert file_type == FileTypes.ZIP.value


# Integration test for FileService.get_filepaths
def test_get_filepaths(setup_files):
    file1_path, file2_path, file3_path = setup_files
    service = FileService()

    # Add files to the service
    service.add_file_details(file1_path, "file1")
    service.add_file_details(file2_path, "file2")
    service.add_file_details(file3_path, "file3")

    # Get the file paths from the service
    filepaths = service.get_filepaths()

    # Assert that the filepaths match the added files
    expected_filepaths = [file1_path, file2_path, file3_path]
    assert filepaths == expected_filepaths


def normalize_path(path: str):
    if path.startswith("/"):
        path = path[1:]
    return path
