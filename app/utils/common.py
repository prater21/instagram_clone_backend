import datetime
from fastapi import (
    HTTPException,
)
from app.utils.logger import log_error


def get_cur_datetime(type="datetime"):
    if type == "date":
        return datetime.date.today()

    cur_datetime = datetime.datetime.now()

    return cur_datetime


def raise_error(url, method, status_code, message):

    log_error(url, method, status_code, message)

    raise HTTPException(status_code=status_code, detail=message)
