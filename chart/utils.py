import datetime


def round_timestamp(time_of_reading: datetime.datetime):
    return time_of_reading - datetime.timedelta(seconds=time_of_reading.second, microseconds=time_of_reading.microsecond)
