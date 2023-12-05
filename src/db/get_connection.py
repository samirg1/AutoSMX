import sqlite3
from contextlib import contextmanager
from typing import Generator, Literal

from utils.constants import BASE_PATH, DatabaseFilenames


@contextmanager
def get_connection(filename: DatabaseFilenames, *, mode: Literal["ro", "rw"] = "ro") -> Generator[sqlite3.Connection, None, None]:
    path = (BASE_PATH / filename).with_suffix(".sdb").as_uri()
    connection = sqlite3.connect(rf"{path}?mode={mode}", uri=True)
    yield connection
    connection.close()
