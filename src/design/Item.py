from attrs import field, frozen


@frozen(repr=False)
class Item:
    number: str
    description: str = field(hash=False, eq=False)
    model: str = field(hash=False, eq=False)
    manufacturer: str = field(hash=False, eq=False)
    serial: str = field(hash=False, eq=False)
    room: str = field(hash=False, eq=False, default="")
    last_update: str = field(hash=False, eq=False, default="")

    def __str__(self) -> str:
        return f"{self.number} - {self.description}"
