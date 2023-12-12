from utils.constants import DAYMONTHYEAR_FORMAT
from utils.convert_stringed_date import convert_stringed_date


from typing import NamedTuple


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