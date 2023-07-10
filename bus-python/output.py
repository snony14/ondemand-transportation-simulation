import datetime


def get_formatted_time(timedelta: int):
    return str(datetime.timedelta(seconds=timedelta))


