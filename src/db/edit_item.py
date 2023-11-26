from datetime import datetime
from typing import Any

from db.get_connection import get_connection
from utils.constants import EDITABLE_ITEM_FIELDS, DatabaseFilenames
from utils.get_sysmodtime import get_sysmodtime


def edit_item(number: str, update: dict[EDITABLE_ITEM_FIELDS, Any]) -> None:
    if not update:
        return

    fields, values = zip(*update.items())
    time = get_sysmodtime(datetime.now())
    with get_connection(DatabaseFilenames.TESTS, mode="rw") as connection:
        with connection:
            connection.execute(
                f"""
                UPDATE devicem1_PS
                SET sysmodtime = ?, last_update = ?, {", ".join(field + " = ?" for field in fields)}
                WHERE logical_name = ?;
                """,
                (time, time, *(value for value in values), number),
            )
