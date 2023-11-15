from typeguard import check_type

from db.get_connection import get_connection
from design.Item import Item
from utils.constants import DatabaseFilenames


def get_items(item_number: str) -> list[Item]:
    with get_connection(DatabaseFilenames.TESTS) as connection:
        item_fields = check_type(
            connection.execute(
                """
                SELECT logical_name, customer_barcode, description, model, manufacturer, serial_no_, room, last_spt_date
                FROM devicem1_PS
                WHERE logical_name LIKE ?;
                """,
                (item_number + "%",),
            ).fetchall(),
            list[tuple[str, str | None, str | None, str | None, str | None, str | None, str | None, str | None]],
        )

    return [Item(*fields) for fields in item_fields]
