from datetime import datetime


def convert_stringed_date(date_string: str) -> datetime:
    """Converts date from 023-10-05 15:12:23.260 format to datetime object"""
    return datetime.strptime(date_string[:-4], r"%Y-%m-%d %H:%M:%S")
