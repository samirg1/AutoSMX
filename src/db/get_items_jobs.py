from design.Item import Item
from design.Job import Job
from db.get_connection import get_connection

def get_items(item_number: str) -> list[Item]:
    with get_connection("SCMTests") as connection:
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
    with get_connection("SCMLookup") as connection:
        job_fields = connection.execute(
            """
            SELECT company, location, dept, number
            FROM 'probsummarym1'
            WHERE number LIKE ? OR number LIKE ?
            """,
            (f"PM{job_number}%", f"{job_number}%"),
        ).fetchall()

    return [Job(*fields) for fields in job_fields]
