from dataclasses import dataclass, field


@dataclass(frozen=True, repr=False, slots=True, order=True)
class Item:
    number: str = field(hash=True)
    description: str = field(compare=False, hash=False)
    model: str = field(compare=False, hash=False)
    manufacturer: str = field(compare=False, hash=False)
    room: str = field(compare=False, hash=False)
    last_service: str = field(compare=False, hash=False)
    serial: str = field(compare=False, hash=False)

    def __str__(self) -> str:
        return f"{self.number} - {self.description}"

    def full_info(self) -> str:
        return f"{str(self)}\nModel: {self.model}\nManufacturer: {self.manufacturer}\nRoom: {self.room}\nLast Service: {self.last_service}\nSerial: {self.serial}"

    def __hash__(self) -> int:
        return hash(self.number)
