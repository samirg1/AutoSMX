from typing import Literal

from design import Item, Test

TJOB = Literal["CAMPEYN", "BENETAS", "ABLE", "JEWISH"]


class Job:
    def __init__(self, number: str, campus: str, address: str, type: TJOB) -> None:
        self._number = number
        self._campus = campus
        self._address = address
        self._type = type
        self._tests: list[Test] = []

    def add_test(self, item: Item) -> Test:
        self._tests.append(Test(item))
        return self._tests[-1]

    def __str__(self) -> str:
        return f"{self._number} - {self._campus}\n{self._type}\n{self._address}"

    def __hash__(self) -> int:
        return hash(self._number)
