import datetime
from .const import ERROR_CODE_MESSAGE
from ..schemas import FailResponse


def get_cur_datetime(type="datetime"):
    if type == "date":
        return datetime.date.today()

    cur_datetime = datetime.datetime.now()

    return cur_datetime


def printError(url, msg):
    print("------------------------error------------------------")
    print(f"url = {url}")
    print(msg)


def getError(url, code, msg=""):
    message = ERROR_CODE_MESSAGE[code]
    if msg:
        message = msg
    ret = FailResponse(code=code, message=message)
    printError(url, message)
    return ret
