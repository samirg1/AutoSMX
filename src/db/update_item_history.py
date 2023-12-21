from datetime import datetime, timedelta
from sqlite3 import Connection
from typeguard import TypeCheckError, check_type
from design.Item import Item
from utils.get_sysmodtime import get_sysmodtime


def update_item_history(item: Item, service_type: str, to_date: datetime | None, test_connection: Connection, asset_connection: Connection) -> None:
    if to_date is None:
        last_spt_date = next_spt_date = "NULL"
    else:
        last_spt_date = get_sysmodtime(to_date)
        next_spt_date = get_sysmodtime((to_date + timedelta(days=366)))

    asset_connection.execute(
        """
        UPDATE DEVICEA4
        SET service_last = ?, service_next = ?
        WHERE logical_name = ? AND service_type = ?;
        """,
        (last_spt_date, next_spt_date, item.number, service_type),
    )

    try:
        services = check_type(
            asset_connection.execute(
                """
                SELECT service_type, service_interval, service_last, service_next
                FROM DEVICEA4
                WHERE logical_name = ?;
                """,
                (item.number,),
            ).fetchall(), 
            list[tuple[str, float, str, str]]
        )
    except TypeCheckError as e:
        print(e)
        services = []
        
    servicearray = "\n".join("^".join(f"{int(s) if isinstance(s, float) else s}" for s in service) + "^" for service in services)

    test_connection.execute(
        """
        UPDATE devicem1_PS
        SET last_spt_date = ?, next_spt_date = ?, servicearray = ?
        WHERE logical_name = ?;
        """,
        (last_spt_date, next_spt_date, servicearray, item.number),
    )