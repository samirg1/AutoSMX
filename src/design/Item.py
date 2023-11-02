from datetime import datetime, timedelta

from attrs import field, frozen

from db.convert_stringed_date import convert_stringed_date


@frozen(repr=False)
class Item:
    number: str
    customer_barcode: str = field(hash=False, eq=False)
    description: str = field(hash=False, eq=False)
    model: str = field(hash=False, eq=False)
    manufacturer: str = field(hash=False, eq=False)
    serial: str = field(hash=False, eq=False)
    room: str | None = field(hash=False, eq=False)
    last_update: datetime | None = field(hash=False, eq=False, converter=convert_stringed_date)

    def __str__(self) -> str:
        return f"{self.number} - {self.description}"
    
    def set_room(self, room: str | None):
        object.__setattr__(self, "room", room)

    @property
    def full_info(self) -> str:
        last_update = "Not found"
        if self.last_update is not None:
            today = datetime.today()
            if self.last_update.date() == today.date():
                last_update = f"Today {self.last_update.strftime("%I:%M%p")}"
            elif self.last_update.date() == (today - timedelta(days=1)).date():
                last_update = f"Yesterday {self.last_update.strftime("%I:%M%p")}"
            else:
                last_update = self.last_update.strftime(r"%d-%m-%Y %I:%M%p")
        return f"{self} - Model: {self.model} - Manufacturer: {self.manufacturer} - SN: {self.serial} - Last Update: {last_update}"
