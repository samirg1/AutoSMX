import functools
from typeguard import check_type
from db.get_connection import get_connection
from utils.constants import DatabaseFilenames


@functools.lru_cache(1)
def get_all_scripts() -> list[tuple[int, str]]:
    with get_connection(DatabaseFilenames.LOOKUP) as connection:
        results = check_type(
            connection.execute(
                """
                SELECT script_no, script_name
                FROM SCMOBILESCRIPTSM1
                ORDER BY script_name
                """
            ).fetchall(),
            list[tuple[float, str]]
        )
    
    return [(int(number), name) for number, name in results]
