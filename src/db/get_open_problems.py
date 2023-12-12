
from typeguard import check_type
from design.OpenProblem import OpenProblem

from db.get_connection import get_connection
from utils.constants import DatabaseFilenames


def get_open_problems(location: str) -> list[OpenProblem]:
    with get_connection(DatabaseFilenames.LOOKUP) as connection:
        results = check_type(
            connection.execute(
                """
                SELECT number, brief_description, open_time, asset_description, serial_no_
                FROM probsummarym1
                WHERE location == ? AND problem_status == 'open';
                """,
                (location,),
            ).fetchall(),
            list[tuple[str, str, str, str, str | None]],
        )

    return [OpenProblem(*res) for res in results]
