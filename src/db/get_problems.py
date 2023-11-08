from db.get_connection import DatabaseFilenames, get_connection
from design.Problem import Problem
from utils.validate_type import validate_type


def get_problems(problem_number: str) -> list[Problem]:
    with get_connection(DatabaseFilenames.LOOKUP) as connection:
        problem_fields = validate_type(
            list[tuple[str, str, str | None, str, str]],
            connection.execute(
                """
                SELECT company, location, dept, number, customer_no_
                FROM probsummarym1
                WHERE number LIKE ? OR number LIKE ?;
                """,
                (f"PM{problem_number}%", f"{problem_number}%"),
            ).fetchall(),
        )

    return [Problem(*fields) for fields in problem_fields]
