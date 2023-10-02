import os
from contextlib import contextmanager
from typing import Generator, Literal
import sqlite3


_BASE_FILE = rf"C:\Users\{os.getenv('USERNAME')}\AppData\Local\SMXMobile"


@contextmanager
def get_connection(filename: str, mode: Literal["ro", "rw"] = "ro") -> Generator[sqlite3.Connection, None, None]:
    connection = sqlite3.connect(rf"file:{_BASE_FILE}\{filename}.sdb?mode={mode}", uri=True)
    yield connection
    connection.close()
