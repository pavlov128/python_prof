from zipfile import ZipFile
import os
import shutil
from urllib.request import urlopen
from datetime import datetime


def check_internet_datetime() -> bool:

    try:
        res = urlopen('http://just-the-time.appspot.com/')
        result = res.read().strip()
        date_time_str = result.decode('utf-8')+'.00000'
        date_time_obj = datetime.strptime(
            date_time_str, '%Y-%m-%d %H:%M:%S.%f')
        if date_time_obj > datetime(2023, 1, 15):
            return False
        else:
            return True
    except Exception as e:
        return False


def read_file_text(filePath):
    res = ''
    with open(filePath, encoding="utf-8") as file:
        res = file.read()
    return res


def extract_tests(fileName) -> dict:

    directory_to_extract = './tests/temp/'+fileName

    if not os.path.isdir(directory_to_extract):
        with ZipFile('./tests/'+fileName) as zip_file:
            zip_file.extractall(directory_to_extract)

    all_files = os.listdir(directory_to_extract)
    exec_files = list(filter(lambda x: not x.endswith('.clue'), all_files))
    clue_files = list(filter(lambda x: x.endswith('.clue'), all_files))

    exec_data = [read_file_text(directory_to_extract+'/'+x) for x in exec_files]
    clue_data = [read_file_text(directory_to_extract+'/'+x) for x in clue_files]
    data = tuple(zip(exec_data, clue_data))

    return dict(zip(exec_files, data))


def remove_folder(fileName):
    directory_to_remove = './tests/temp/'+fileName
    shutil.rmtree(directory_to_remove)


def main(file_name):
    print(extract_tests(file_name))
    # removeFolder(fileName)


if __name__ == '__main__':
    # it = check_internet_datetime()
    main('tests_2310066.zip')
