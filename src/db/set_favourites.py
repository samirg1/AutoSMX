from db.get_connection import get_connection
from design.data import SCRIPTS

def set_favourites():
    script_numbers = [(script.number,) for script in SCRIPTS.values()]
    with get_connection("Settings") as connection:
        with connection:
            connection.execute("DELETE FROM ScriptFavourites")

        with connection:
            connection.executemany(
                """
                INSERT INTO ScriptFavourites
                VALUES (?)
            """,
                script_numbers,
            )
