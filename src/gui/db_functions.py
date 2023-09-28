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


def get_items(item_number: str) -> list[Item]:
    with _get_connection("SCMTests") as connection:
        item_fields = connection.execute(
            """
            SELECT logical_name, description, model, manufacturer, serial_no_, room, last_update
            FROM 'devicem1_PS'
            WHERE logical_name LIKE ?
            """,
            (item_number + "%",),
        ).fetchall()

    return [Item(*fields) for fields in item_fields]


def get_jobs(job_number: str) -> list[Job]:
    with _get_connection("SCMLookup") as connection:
        job_fields = connection.execute(
            """
            SELECT company, location, dept, number
            FROM 'probsummarym1'
            WHERE number LIKE ? OR number LIKE ?
            """,
            (f"PM{job_number}%", f"{job_number}%"),
        ).fetchall()

    return [Job(*fields) for fields in job_fields]

