import pytest
from unittest import mock
from werkzeug.datastructures import FileStorage

from app.api import app
from tests.unit.mocks.shared_mocks import file1, file2


@pytest.fixture
def client():
    app.testing = True
    with app.test_client() as client:
        yield client


@pytest.fixture
def mock_file_service():
    with mock.patch("app.api.FileService") as mock_FileService:
        yield mock_FileService.return_value


# Define a fixture for mocking CsvMerger
@pytest.fixture
def mock_csv_merger():
    with mock.patch("app.api.CsvMerger") as mock_CsvMerger:
        yield mock_CsvMerger.return_value


@pytest.fixture
def mock_send_file():
    with mock.patch("flask.send_file") as mock_send_file:
        yield mock_send_file


def test_hello_world(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.get_json() == {"message": "Welcome to the CSV Merger API"}


def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.get_json() == {"message": "Healthy"}


@mock.patch("app.api.send_file")
@mock.patch("app.api.InputSanitizerService")
def test_csvs(
    mock_sanitizer, mock_send_file, client, mock_file_service, mock_csv_merger
):
    mock_sanitizer.sanitize_group_name.return_value = "group_name"
    mock_csv_merger.get_merged_csvs.return_value = "merged.csv"
    mock_file_service.add_file_details.return_value = None
    mock_file_service.get_consolidated_filepath.return_value = "consolidated.csv"
    files_to_upload = {"group_name": [file1, file2]}

    response = client.post(
        "/csvs", content_type="multipart/form-data", data=files_to_upload
    )

    assert response.status_code == 200
    # Check if the mock methods were called with the expected arguments
    actual_files = mock_csv_merger.merge_csvs.call_args[0][0]
    expected_files = files_to_upload["group_name"]
    assert_files_match(actual_files, expected_files)
    mock_csv_merger.get_merged_csvs.assert_called_with("group_name")
    mock_file_service.add_file_details.assert_called_with("merged.csv", "group_name")
    mock_file_service.get_consolidated_filepath.assert_called_once()
    mock_send_file.assert_called_with("consolidated.csv", as_attachment=True)


def test_csvs_shouldReturn400WhenNoFilesPassed(client):
    response = client.post("/csvs", content_type="multipart/form-data", data={})

    assert response.status_code == 400


def assert_files_match(actual_files, expected_files):
    assert isinstance(
        actual_files, list
    ), f"Expected a list, but got: {type(actual_files)}"
    for i in range(len(actual_files)):
        assert isinstance(
            actual_files[i], FileStorage
        ), f"Expected FileStorage, but got: {type(actual_files[i])}"
        assert actual_files[i].filename == expected_files[i].filename
