import datetime


def interval_to_timedelta(interval: str) -> datetime.timedelta:
    """ Parse the interval string into a timedelta object. """

    if interval.endswith('d'):
        return datetime.timedelta(days=int(interval[:-1]))
    elif interval.endswith('h'):
        return datetime.timedelta(hours=int(interval[:-1]))
    elif interval.endswith('m'):
        return datetime.timedelta(minutes=int(interval[:-1]))

    raise ValueError("Invalid interval format")

