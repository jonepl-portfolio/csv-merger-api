import pytest
import pandas as pd
from app.services.dataframe_service import DataframeService as Service
from tests.unit.mocks.dataframe_mocks import (
    MOCK_EMPTY_DATA,
    MOCK_DATAFRAME_DATA_1,
    MOCK_DATAFRAME_DATA_2,
    MOCK_DATAFRAME_DATA_3,
)


def test_convert_to_dataframe_should():
    pass


@pytest.mark.parametrize(
    "data1,data2,expected_data",
    [
        pytest.param(
            MOCK_EMPTY_DATA,
            MOCK_DATAFRAME_DATA_1,
            MOCK_DATAFRAME_DATA_1,
            id="Empty Old Dataframe",
        ),
        pytest.param(
            MOCK_DATAFRAME_DATA_1,
            MOCK_EMPTY_DATA,
            MOCK_DATAFRAME_DATA_1,
            id="Empty New Dataframe",
        ),
    ],
)
def test_merge_dataframes_shouldMergeEmptyAndFullDataframes(
    data1, data2, expected_data
):
    df1 = pd.DataFrame(data1)
    df2 = pd.DataFrame(data2)
    expected = pd.DataFrame(expected_data)

    actual = Service.merge_dataframes(df1, df2)

    assert actual.compare(expected).empty


def test_merge_dataframes_shouldMergeDataframesWithUniqueRows():
    expected_data = MOCK_DATAFRAME_DATA_1 + MOCK_DATAFRAME_DATA_2
    df1 = pd.DataFrame(MOCK_DATAFRAME_DATA_1)
    df2 = pd.DataFrame(MOCK_DATAFRAME_DATA_2)
    expected = pd.DataFrame(expected_data)

    actual = Service.merge_dataframes(df1, df2)

    assert actual.reset_index(drop=True).compare(expected.reset_index(drop=True)).empty


def test_merge_dataframes_shouldMergeDataframesWithoutDuplicatedRows():
    df1 = pd.DataFrame(MOCK_DATAFRAME_DATA_1)
    df2 = pd.DataFrame(MOCK_DATAFRAME_DATA_3)
    expected_data = (
        [MOCK_DATAFRAME_DATA_1[0]] + [MOCK_DATAFRAME_DATA_1[2]] + MOCK_DATAFRAME_DATA_3
    )
    expected = pd.DataFrame(expected_data)

    actual = Service.merge_dataframes(df1, df2)

    assert actual.reset_index(drop=True).compare(expected.reset_index(drop=True)).empty
