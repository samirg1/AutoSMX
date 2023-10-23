from datetime import datetime


def convert_stringed_date(date_string: str | None) -> datetime | None:
    """Converts date from 2023-10-05 15:12:23.260 format to datetime object"""
    if date_string is None:
        return None
    return datetime.strptime(date_string[:-4], r"%Y-%m-%d %H:%M:%S")
