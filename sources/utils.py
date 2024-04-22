from datetime import datetime


def llu_datetime(timestamp):
    return datetime.strptime(timestamp, "%m/%d/%Y %I:%M:%S %p")