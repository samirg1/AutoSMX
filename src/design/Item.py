from datetime import datetime

from attrs import field, frozen

from db.convert_stringed_date import convert_stringed_date


@frozen(repr=False)
class Item:
    number: str
    description: str = field(hash=False, eq=False)
    model: str = field(hash=False, eq=False)
    manufacturer: str = field(hash=False, eq=False)
    serial: str = field(hash=False, eq=False)
    room: str = field(hash=False, eq=False)
    last_update: datetime | None = field(hash=False, eq=False, converter=convert_stringed_date)

    def __str__(self) -> str:
        return f"{self.number} - {self.description}"

    @property
    def full_info(self) -> str:
        return f"{self}\nModel: {self.model}\nManufacturer: {self.manufacturer}\nSN: {self.serial}\nRoom: {self.room}\nLast Update: {'Not found' if self.last_update is None else self.last_update.strftime(r'%d-%m-%Y %I:%M%p')}"
