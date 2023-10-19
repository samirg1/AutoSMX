from db.get_connection import DatabaseFilenames, get_connection
from design.Item import Item
from design.Problem import Problem


def get_items(item_number: str) -> list[Item]:
    with get_connection(DatabaseFilenames.TESTS) as connection:
        item_fields = connection.execute(
            """
            SELECT logical_name, description, model, manufacturer, serial_no_, room, last_spt_date
            FROM 'devicem1_PS'
            WHERE logical_name LIKE ?;
            """,
            (item_number + "%",),
        ).fetchall()

    return [Item(*fields) for fields in item_fields]


def get_problems(problem_number: str) -> list[Problem]:
    with get_connection(DatabaseFilenames.LOOKUP) as connection:
        problem_fields = connection.execute(
            """
            SELECT company, location, dept, number, customer_no_
            FROM 'probsummarym1'
            WHERE number LIKE ? OR number LIKE ?;
            """,
            (f"PM{problem_number}%", f"{problem_number}%"),
        ).fetchall()

    return [Problem(*fields) for fields in problem_fields]
