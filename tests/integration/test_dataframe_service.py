import os
import pandas as pd
import pytest
from werkzeug.datastructures import FileStorage

from app.services.dataframe_service import DataframeService as Service

# Define paths for the CSV files used in the tests
TEST_DATA_DIR = "tests/integration/data/"
CSV_FILE_1 = os.path.join(TEST_DATA_DIR, "data1.csv")
CSV_FILE_2 = os.path.join(TEST_DATA_DIR, "data2.csv")


# Create a fixture for setting up test data
@pytest.fixture
def setup_test_data():
    # Ensure the test data directory exists
    os.makedirs(TEST_DATA_DIR, exist_ok=True)

    # Create CSV files for the tests
    data1 = {"col1": [1, 2], "col2": [3, 4]}
    data2 = {"col1": [3, 4], "col2": [5, 6]}

    df1 = pd.DataFrame(data1)
    df2 = pd.DataFrame(data2)

    df1.to_csv(CSV_FILE_1, index=False)
    df2.to_csv(CSV_FILE_2, index=False)

    # Yield the paths of the created CSV files
    yield CSV_FILE_1, CSV_FILE_2

    # Clean up by removing the created files and directory
    os.remove(CSV_FILE_1)
    os.remove(CSV_FILE_2)
    os.rmdir(TEST_DATA_DIR)


# Integration test for DataframeService.convert_to_dataframe
def test_convert_to_dataframe_integration(setup_test_data):
    csv_file_1, _ = setup_test_data
    # Create a FileStorage object to simulate file uploads
    with open(csv_file_1, "rb") as f:
        storage = FileStorage(f)
        df = Service.convert_to_dataframe(storage)

        # Create expected DataFrame from the CSV file
        expected_df = pd.read_csv(csv_file_1)

        # Compare the DataFrame created by convert_to_dataframe with the expected DataFrame
        assert df.equals(expected_df)


# Integration test for DataframeService.merge_dataframes
def test_merge_dataframes_integration(setup_test_data):
    csv_file_1, csv_file_2 = setup_test_data

    # Read the CSV files into DataFrames
    df1 = pd.read_csv(csv_file_1)
    df2 = pd.read_csv(csv_file_2)

    # Merge the DataFrames using the service
    merged_df = Service.merge_dataframes(df1, df2)

    # Create the expected merged DataFrame
    expected_df = pd.concat([df1, df2], ignore_index=True).drop_duplicates(keep="last")

    # Compare the merged DataFrame with the expected merged DataFrame
    merged_df = merged_df.reset_index(drop=True)
    expected_df = expected_df.reset_index(drop=True)
