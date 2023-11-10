from datetime import datetime

from utils.constants import SYSMODTIME_FORMAT


def get_sysmodtime(date: datetime) -> str:
    return date.strftime(SYSMODTIME_FORMAT)[:-3]