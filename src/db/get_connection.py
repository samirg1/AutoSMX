import os
import sqlite3
from contextlib import contextmanager
from enum import StrEnum
from typing import Generator, Literal

BASE_FILE = rf"C:\Users\{os.getenv('USERNAME')}\AppData\Local\SMXMobile"


class DatabaseFilenames(StrEnum):
    TESTS = "SCMTests"
    LOOKUP = "SCMLookup"
    SETTINGS = "Settings"


@contextmanager
def get_connection(filename: DatabaseFilenames, *, mode: Literal["ro", "rw"] = "ro") -> Generator[sqlite3.Connection, None, None]:
    connection = sqlite3.connect(rf"file:{BASE_FILE}\{filename}.sdb?mode={mode}", uri=True)
    yield connection
    connection.close()
