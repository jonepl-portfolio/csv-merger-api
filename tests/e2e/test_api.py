"""Test suite for api.py"""

import pytest
from werkzeug.datastructures import FileStorage

from app.api import app as flask_app


@pytest.fixture()
def client():
    flask_app.testing = True
    with flask_app.test_client() as client:
        yield client


def test_root(client):
    """Test the root endpoint ('/') for a 'hello world' message."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json == {"message": "Welcome to the CSV Merger API"}


def test_health(client):
    """Test the '/fruits' endpoint for the correct list of fruits."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json == {"message": "Healthy"}


def test_csvs_e2e(client, tmpdir):
    # Define input data
    files_to_upload = {
        "group_name": [
            FileStorage(
                stream=open("tests/e2e/test_data/test1.csv", "rb"),
                filename="test_file1.csv",
            ),
            FileStorage(
                stream=open("tests/e2e/test_data/test2.csv", "rb"),
                filename="test_file2.csv",
            ),
        ]
    }

    # Call the API endpoint
    response = client.post(
        "/csvs", content_type="multipart/form-data", data=files_to_upload
    )

    # Assertions
    assert response.status_code == 200
    # You can add more assertions to check the response content and file download, if necessary
