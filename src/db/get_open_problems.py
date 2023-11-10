from typing import NamedTuple

from utils.convert_stringed_date import convert_stringed_date
from db.get_connection import get_connection
from utils.constants import DAYMONTHYEAR_FORMAT, DatabaseFilenames
from utils.validate_type import validate_type


class OpenProblem(NamedTuple):
    number: str
    description: str
    date_opened: str
    asset_description: str
    asset_serial: str | None

    def __repr__(self) -> str:
        converted = convert_stringed_date(self.date_opened)
        date_opened = "Not found" if converted is None else converted.strftime(DAYMONTHYEAR_FORMAT)
        return f"{self.number} - Opened: {date_opened} - {self.asset_description} ({self.asset_serial}) : {self.description}"


def get_open_problems(location: str) -> list[OpenProblem]:
    with get_connection(DatabaseFilenames.LOOKUP) as connection:
        results = validate_type(
            list[tuple[str, str, str, str, str | None]],
            connection.execute(
                """
                SELECT number, brief_description, open_time, asset_description, serial_no_
                FROM probsummarym1
                WHERE location == ? AND problem_status == 'open';
                """,
                (location,),
            ).fetchall(),
        )

    return [OpenProblem(*res) for res in results]
