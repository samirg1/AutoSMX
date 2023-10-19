import os
from contextlib import contextmanager
from typing import Generator, Literal
from enum import Enum
import sqlite3


BASE_FILE = rf"C:\Users\{os.getenv('USERNAME')}\AppData\Local\SMXMobile"

class DatabaseFilenames(Enum):
    TESTS = "SCMTests"
    LOOKUP = "SCMLookup"
    SETTINGS = "Settings"


@contextmanager
def get_connection(filename: DatabaseFilenames, *, mode: Literal["ro", "rw"] = "ro") -> Generator[sqlite3.Connection, None, None]:
    connection = sqlite3.connect(rf"file:{BASE_FILE}\{filename.value}.sdb?mode={mode}", uri=True)
    yield connection
    connection.close()
