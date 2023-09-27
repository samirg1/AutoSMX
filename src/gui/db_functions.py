import os
import sqlite3
from contextlib import contextmanager
from typing import Generator

from design.Item import Item
from design.Job import Job

_BASE_FILE = rf"C:\Users\{os.getenv('USERNAME')}\AppData\Local\SMXMobile"


@contextmanager
def _get_connection(filename: str) -> Generator[sqlite3.Connection, None, None]:
    connection = sqlite3.connect(rf"{_BASE_FILE}\{filename}.sdb")
    yield connection
    connection.close()


def get_item(item_number: str) -> Item | None:
    with _get_connection("SCMTests") as connection:
        fields = connection.execute(
            """
            SELECT logical_name, description, model, manufacturer, serial_no_, room, last_update
            FROM 'devicem1_PS'
            WHERE logical_name == ?
            """,
            (item_number,),
        ).fetchone()

    if fields is None:
        return None

    return Item(*fields)


def get_job(job_number: str) -> Job | None:
    if not job_number.startswith("PM"):
        job_number = f"PM{job_number}"

    with _get_connection("SCMLookup") as connection:
        fields = connection.execute(
            """
            SELECT company, location, dept, number
            FROM 'probsummarym1'
            WHERE number == ?
            """,
            (job_number,),
        ).fetchone()

    if fields is None:
        return None

    return Job(*fields)
