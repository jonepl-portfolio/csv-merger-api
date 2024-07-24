from app.services.file_service import FileDetails

MOCK_FILENAME_1 = "mock1.csv"
MOCK_FILENAME_2 = "mock2.csv"
MOCK_FILENAME_3 = "mock3.csv"
MOCK_FILEPATH_1 = "./app/path1/file1.csv"
MOCK_FILEPATH_2 = "./app/path2/file2.csv"
MOCK_FILEPATH_3 = "./app/path3/file3.csv"

fd1 = FileDetails(MOCK_FILENAME_1, MOCK_FILEPATH_1)
fd2 = FileDetails(MOCK_FILENAME_2, MOCK_FILEPATH_2)
fd3 = FileDetails(MOCK_FILENAME_3, MOCK_FILEPATH_3)
