import sqlite3
from contextlib import contextmanager
from typing import Generator, Literal

from utils.constants import BASE_FILE, DatabaseFilenames


@contextmanager
def get_connection(filename: DatabaseFilenames, *, mode: Literal["ro", "rw"] = "ro") -> Generator[sqlite3.Connection, None, None]:
    connection = sqlite3.connect(rf"file:{BASE_FILE}\{filename}.sdb?mode={mode}", uri=True)
    yield connection
    connection.close()
