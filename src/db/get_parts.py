from typing import Literal, overload

from typeguard import check_type

from db.get_connection import get_connection
from design.Part import Part
from utils.constants import DatabaseFilenames

PART_FIELDS = Literal["manufacturer", "manufacturer_part_number", "part_desc"]


@overload
def get_parts(search: str) -> Part | None:
    ...


@overload
def get_parts(search: dict[PART_FIELDS, str]) -> list[Part]:
    ...


def get_parts(search: str | dict[PART_FIELDS, str]) -> list[Part] | Part | None:
    if isinstance(search, dict) and len(search) == 0:
        return []

    if isinstance(search, str):
        where = "part_no = ?"
        fields = (search,)
    else:
        where = " AND ".join(f"{field} LIKE ?" for field in search.keys())
        fields = tuple(f"%{value}%" for value in search.values())

    with get_connection(DatabaseFilenames.LOOKUP) as connection:
        part_fields = check_type(
            connection.execute(
                f"""
                SELECT part_no, manufacturer, manufacturer_part_number, part_desc
                FROM MODELM1
                WHERE {where};
                """,
                fields,
            ).fetchall(),
            list[tuple[str, str, str | None, str]],
        )

    if isinstance(search, str):
        return None if len(part_fields) == 0 else Part(*part_fields[0])
    return [Part(*fields) for fields in part_fields]
