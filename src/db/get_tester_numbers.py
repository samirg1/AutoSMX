import functools

from typeguard import check_type

from db.get_connection import get_connection
from utils.constants import DatabaseFilenames


@functools.lru_cache(1)
def get_tester_numbers() -> set[str]:
    with get_connection(DatabaseFilenames.TESTS) as connection:
        numbers = check_type(
            connection.execute(
                """
                SELECT logical_name
                FROM SCMOBILEMYEQUIPMENTM1
                """
            ).fetchall(),
            list[tuple[str]],
        )

    return set(number for number, in numbers if number)
