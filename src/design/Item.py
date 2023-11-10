from datetime import datetime, timedelta

from attrs import field, frozen

from utils.convert_stringed_date import convert_stringed_date
from utils.constants import DAYMONTHYEAR_FORMAT, SIMPLIFIED_TIME_FORMAT


@frozen(repr=False)
class Item:
    number: str
    customer_barcode: str | None = field(hash=False, eq=False)
    description: str | None = field(hash=False, eq=False)
    model: str | None = field(hash=False, eq=False)
    manufacturer: str | None = field(hash=False, eq=False)
    serial: str | None = field(hash=False, eq=False)
    room: str | None = field(hash=False, eq=False)
    last_update: datetime | None = field(hash=False, eq=False, converter=convert_stringed_date)

    def __repr__(self) -> str:
        return f"{self.number} - {self.description}"

    def set_room(self, room: str | None) -> None:
        object.__setattr__(self, "room", room)

    @property
    def full_info(self) -> str:
        last_update = "Not found"
        if self.last_update is not None:
            today = datetime.today()
            if self.last_update.date() == today.date():
                last_update = f"Today {self.last_update.strftime(SIMPLIFIED_TIME_FORMAT)}"
            elif self.last_update.date() == (today - timedelta(days=1)).date():
                last_update = f"Yesterday {self.last_update.strftime(SIMPLIFIED_TIME_FORMAT)}"
            else:
                last_update = self.last_update.strftime(f"{DAYMONTHYEAR_FORMAT} {SIMPLIFIED_TIME_FORMAT}")
        return f"{self} - Model: {self.model} - Manufacturer: {self.manufacturer} - SN: {self.serial} - Last Update: {last_update}"
