from db.get_connection import get_connection
from design.data import SCRIPT_INFOS


def set_favourites() -> None:
    with get_connection("Settings") as connection:
        with connection:
            connection.execute("DELETE FROM ScriptFavourites")

        with connection:
            connection.executemany(
                """
                INSERT INTO ScriptFavourites
                VALUES (?)
            """,
                [(info.number,) for info in SCRIPT_INFOS],
            )
