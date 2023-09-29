import os
from contextlib import contextmanager
from typing import Generator
import sqlite3


_BASE_FILE = rf"C:\Users\{os.getenv('USERNAME')}\AppData\Local\SMXMobile"


@contextmanager
def get_connection(filename: str) -> Generator[sqlite3.Connection, None, None]:
    connection = sqlite3.connect(rf"{_BASE_FILE}\{filename}.sdb")
    yield connection
    connection.close()
