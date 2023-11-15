from attrs import frozen, field


@frozen(repr=False)
class Part:
    number: str
    manufacturer: str = field(hash=False, eq=False)
    manufacturer_number: str | None = field(hash=False, eq=False)
    description: str = field(hash=False, eq=False)

    def __repr__(self) -> str:
        return f"PN: {self.number}, {self.description}"
