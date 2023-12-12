import psutil

from utils.constants import SYNC_EXECUTABLE_NAME


def is_sync_running() -> bool:
    return SYNC_EXECUTABLE_NAME in (p.name() for p in psutil.process_iter())
