from design import Item, Test

class Job:
    def __init__(self, company: str, campus: str, department: str) -> None:
        self._company = company
        self._campus = campus
        self._department = department
        self._tests: list[Test] = []

    def add_test(self, item: Item) -> Test:
        self._tests.append(Test(item))
        return self._tests[-1]

    def __str__(self) -> str:
        return f"{self._campus}\n{self._company}\n{self._department}"

    def __hash__(self) -> int:
        return hash(self._campus)
