from typeguard import check_type

from db.get_connection import get_connection
from design.Problem import Problem
from utils.constants import DatabaseFilenames


def get_problems(problem_number: str) -> list[Problem]:
    with get_connection(DatabaseFilenames.LOOKUP) as connection:
        problem_fields = check_type(
            connection.execute(
                """
                SELECT company, location, dept, number, customer_no_
                FROM probsummarym1
                WHERE number LIKE ? OR number LIKE ?;
                """,
                (f"PM{problem_number}%", f"{problem_number}%"),
            ).fetchall(),
            list[tuple[str, str, str | None, str, str]],
        )

    return [Problem(*fields) for fields in problem_fields]
