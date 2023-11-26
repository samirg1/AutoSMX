from datetime import datetime

from utils.constants import SYSMODTIME_FORMAT


def convert_stringed_date(date_string: str | None) -> datetime | None:
    if date_string is None:
        return None
    return datetime.strptime(date_string + "000", SYSMODTIME_FORMAT)
