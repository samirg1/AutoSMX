from db.get_connection import get_connection

_FAVOURITES = [1227, 1261, 1287, 1279, 1278, 1228, 1222, 1226, 1230, 1229, 859, 1065, 606, 1113, 799, 1190, 1223]


def set_favourites(script_numbers: list[int] = _FAVOURITES):
    values = [(number,) for number in script_numbers]
    with get_connection("Settings") as connection:
        with connection:
            connection.execute("DELETE FROM ScriptFavourites")

        with connection:
            connection.executemany(
                """
                INSERT INTO ScriptFavourites
                VALUES (?)
            """,
                values,
            )
