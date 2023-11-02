from datetime import datetime
from typing import Any, Literal

from db.get_connection import get_connection, DatabaseFilenames

_EDITABLE_ITEM_FIELDS = Literal["room"]


def edit_item(number: str, update: dict[_EDITABLE_ITEM_FIELDS, Any]) -> None:
    if not update:
        return
    
    fields = tuple(update.items())
    time = datetime.now().strftime(r"%Y-%m-%d %H:%M:%S.%f")[:-3]
    with get_connection(DatabaseFilenames.TESTS, mode="rw") as connection:
        with connection:
            connection.execute(
                f"""
                UPDATE devicem1_PS
                SET sysmodtime = ?, last_update = ?, {", ".join(field[0] + " = ?" for field in fields)}
                WHERE logical_name = ?;
                """,
                (time, time, *(field[1] for field in fields), number)
            )
