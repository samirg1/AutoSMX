import functools
from typing import NamedTuple

from db.get_connection import DatabaseFilenames, get_connection


class TestResult(NamedTuple):
    nickname: str
    fullname: str


@functools.lru_cache(maxsize=5)
def get_overall_results(customer_id: int) -> list[TestResult]:
    with get_connection(DatabaseFilenames.LOOKUP) as connection:
        results: list[tuple[str, str]] = connection.execute(
            """
            SELECT overall_id, overall_text
            FROM SCMobileOverallm1
            WHERE (customer_id IS NULL OR customer_id = ?) AND
                    (exclude_customer_id IS NULL OR exclude_customer_id NOT LIKE ?);
            """,
            (customer_id, f"%{customer_id},%"),
        ).fetchall()

    return [TestResult(nickname, fullname) for nickname, fullname in results]
