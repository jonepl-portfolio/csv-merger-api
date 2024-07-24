import pytest
from typing import List
from unittest import mock
from werkzeug.datastructures import FileStorage

from app.controllers.csv_merger import CsvMerger
from app.services.dataframe_service import DataframeService
from app.constants.shared_consts import TEMP_PATH, FileExtensions
from tests.unit.mocks.shared_mocks import file1, file2


@pytest.fixture
def csv_merger() -> CsvMerger:
    return CsvMerger()


def test_init_shouldCreate(csv_merger: CsvMerger):
    assert csv_merger.df.empty is True


@mock.patch("app.controllers.csv_merger.DataframeService")
def test_merge_csvs_shouldCreate(
    mock_dataframe_service: DataframeService, csv_merger: CsvMerger
):
    fileStorages: List[FileStorage] = [file1, file2]

    csv_merger.merge_csvs(fileStorages)

    expected_calls = [mock.call.write(file1), mock.call.write(file2)]
    mock_dataframe_service.convert_to_dataframe.assert_has_calls(expected_calls)
    mock_dataframe_service.merge_dataframes.assert_called_with(
        csv_merger.df, mock_dataframe_service.convert_to_dataframe.return_value
    )


@mock.patch("builtins.open")
@mock.patch("app.controllers.csv_merger.os")
def test_get_merged_csvs_shouldCreateCsvs(
    mock_os: DataframeService, mock_open, csv_merger: CsvMerger
):
    group_name = "group-name"
    csv_merger.df.to_csv = mock.MagicMock()
    mock_os.path.exists.return_value = False
    mock_open.return_value.closed = False

    actual = csv_merger.get_merged_csvs(group_name)

    mock_os.path.exists.assert_called_with(TEMP_PATH)
    mock_os.makedirs.assert_called_with(TEMP_PATH)
    mock_os.path.join.assert_called_with(
        TEMP_PATH, f"{group_name}{FileExtensions.CSV.value}"
    )
    mock_open.assert_called_with(mock_os.path.join.return_value, "w")
    mock_open.return_value.write.assert_called_with(csv_merger.df.to_csv.return_value)
    mock_open.return_value.close.assert_called()
    assert actual == mock_os.path.join.return_value


@mock.patch("app.controllers.csv_merger.logger")
@mock.patch("builtins.open")
@mock.patch("app.controllers.csv_merger.os")
def test_get_merged_csvs_shouldThrowExceptionIfUnableToOpenFile(
    mock_os: DataframeService, mock_open, mock_logger, csv_merger: CsvMerger
):
    group_name = "group-name"
    csv_merger.df.to_csv = mock.MagicMock()
    mock_os.path.exists.return_value = False
    mock_open.return_value.write = lambda: (_ for _ in ()).throw(
        Exception("An error occurred")
    )
    mock_open.return_value.closed = True

    expected_message_pattern = (
        r"Error occurred when opening/writing file. Exceptions .*"
    )
    with pytest.raises(Exception, match=expected_message_pattern):
        csv_merger.get_merged_csvs(group_name)
