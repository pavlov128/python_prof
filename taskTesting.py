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

def readFileText(filePath):
    res = ''
    with open(filePath) as file:
        res = file.read()

    return res

def extractTests(fileName) -> dict:
    
    directoryToExtractTo = './tests/temp/'+fileName
   
    if not os.path.isdir(directoryToExtractTo):
        with ZipFile('./tests/'+fileName) as zip_file:
            zip_file.extractall(directoryToExtractTo)

    all_files = os.listdir(directoryToExtractTo)
    exec_files = list(filter(lambda x: not x.endswith('.clue'), all_files))
    clue_files = list(filter(lambda x: x.endswith('.clue'), all_files))

    exec_data = [readFileText(directoryToExtractTo+'/'+x) for x in exec_files]
    clue_data = [readFileText(directoryToExtractTo+'/'+x) for x in clue_files]
    data = tuple(zip(exec_data, clue_data))

    return  dict(zip(exec_files, data))

def removeFolder(fileName):
    directoryToRemove = './tests/temp/'+fileName
    shutil.rmtree(directoryToRemove)


def main(fileName):
    print(extractTests(fileName))
    # removeFolder(fileName)


if __name__ == '__main__':
    fileName = 'tests_2310066.zip'
    it = check_internet_datetime()
    print(it)
    main(fileName)
