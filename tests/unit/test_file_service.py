import os
import pytest
from unittest import mock
import zipfile

from app.services.file_service import FileService
from app.constants.shared_consts import (
    FileExtensions,
    FileTypes,
    CONSOLIDATED_ZIP_PATH,
    APPLICATION_ROOT,
)
from tests.unit.mocks.file_service_mocks import fd1, fd2, fd3


@pytest.fixture
def service() -> FileService:
    return FileService()


def test_should_create(service: FileService):
    assert service.file_details == []
    assert service.consolidated_path is None


def test_add_file_details_shouldAddNewFileDetails(service: FileService):
    service.file_details = [fd1, fd2]

    service.add_file_details(fd3.path, fd3.name)

    assert len(service.file_details) == 3
    assert service.file_details[2].name == fd3.name
    assert service.file_details[2].path == fd3.path


def test_get_consolidated_filepath_shouldReturnSinglePathWhenOnlyOneExists(
    service: FileService,
):
    service.file_details = [fd1]

    actual = service.get_consolidated_filepath()

    assert actual == fd1.path


@mock.patch("app.services.file_service.zipfile.ZipFile")
def test_get_consolidated_filepath_shouldZipAllFilesWhenMoreThanOneExists(
    mock_zipfile: mock.MagicMock, service: FileService
):
    mock_zipMe: mock.MagicMock = mock_zipfile.return_value.__enter__.return_value
    service.file_details = [
        mock.MagicMock(path="path_to_file1.csv"),
        mock.MagicMock(path="path_to_file2.csv"),
    ]
    expected_temp_filepath = os.path.join(APPLICATION_ROOT, CONSOLIDATED_ZIP_PATH)
    expected_calls = [
        mock.call.write("path_to_file1.csv", compress_type=zipfile.ZIP_DEFLATED),
        mock.call.write("path_to_file2.csv", compress_type=zipfile.ZIP_DEFLATED),
    ]

    actual = service.get_consolidated_filepath()

    assert actual == expected_temp_filepath
    mock_zipfile.assert_called_with(expected_temp_filepath, "w")
    mock_zipMe.write.assert_has_calls(expected_calls)


def test_get_filename_shouldReturnCsvFileWhenOnlyOneFileAdded(service: FileService):
    service.file_details = [fd1]
    expected = fd1.name + FileExtensions.CSV.value

    actual = service.get_filename()

    assert actual == expected


def test_get_filename_shouldReturnZipFileWhenMultipleFilesAdded(service: FileService):
    service.file_details = [fd1, fd2]

    actual = service.get_filename()

    assert actual == "consolidated-csvs.zip"


def test_get_get_file_type_shouldReturnCsvWhenOnlyOneFileAdded(service: FileService):
    service.file_details = [fd1]
    expected = FileTypes.CSV.value

    actual = service.get_file_type()

    assert actual == expected


def test_get_get_file_type_shouldReturnZipFileWhenMultipleFilesAdded(
    service: FileService,
):
    service.file_details = [fd1, fd2]
    expected = FileTypes.ZIP.value

    actual = service.get_file_type()

    assert actual == expected


def test_get_filepaths_shouldReturnFilepathToAllAddedFiles(service: FileService):
    service.file_details = [fd1, fd2, fd3]
    expected = [fd1.path, fd2.path, fd3.path]

    actual = service.get_filepaths()

    assert actual == expected
