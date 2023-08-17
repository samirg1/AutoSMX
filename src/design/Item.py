from attrs import field, frozen


@frozen(repr=False)
class Item:
    number: str
    description: str = field(hash=False, eq=False)
    model: str = field(hash=False, eq=False)
    manufacturer: str = field(hash=False, eq=False)
    room: str = field(hash=False, eq=False)
    last_service: str = field(hash=False, eq=False)
    serial: str = field(hash=False, eq=False)

    def __str__(self) -> str:
        return f"{self.number} - {self.description}"

    def full_info(self) -> str:
        return f"{str(self)}\nModel: {self.model}\nManufacturer: {self.manufacturer}\nRoom: {self.room}\nLast Service: {self.last_service}\nSerial: {self.serial}"
