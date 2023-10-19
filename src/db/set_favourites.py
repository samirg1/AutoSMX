from db.get_connection import get_connection, DatabaseFilenames
from design.data import get_all_scripts


def set_favourites() -> None:
    with get_connection(DatabaseFilenames.SETTINGS, mode="rw") as connection:
        with connection:
            connection.execute("DELETE FROM ScriptFavourites;")

        with connection:
            connection.executemany(
                """
                INSERT INTO ScriptFavourites
                VALUES (?);
                """,
                [(script.number,) for script in get_all_scripts().values()],
            )
