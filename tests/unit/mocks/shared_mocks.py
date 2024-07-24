from io import BytesIO
from werkzeug.datastructures import FileStorage

file_content1 = b"col1,col2\nval1_1,val1_2\nval2_1,val2_2"
file_content2 = b"col1,col2\nval3_1,val3_2\nval4_1,val4_2"

file1 = FileStorage(stream=BytesIO(file_content1), filename="test1.csv")
file2 = FileStorage(stream=BytesIO(file_content2), filename="test2.csv")

file3 = FileStorage(stream=BytesIO(file_content1), filename="test1.csv")
file4 = FileStorage(stream=BytesIO(file_content2), filename="test2.csv")
