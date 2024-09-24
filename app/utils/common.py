import datetime


def get_cur_datetime(type="datetime"):
    if type == "date":
        return datetime.date.today()

    cur_datetime = datetime.datetime.now()

    return cur_datetime
