from design import Test

class Job:
    def __init__(self, company: str, campus: str, department: str) -> None:
        self._company = company
        self._campus = campus
        self._department = department
        self._tests: list[Test] = []

    @property
    def campus(self) -> str:
        return self._campus

    def add_test(self, test: Test):
        self._tests.append(test)

    def __str__(self) -> str:
        return f"{self._campus}\n{self._company}\n{self._department}"
    
    def full_info(self) -> str:
        base = f"{str(self)}\nTests:\n"
        base += "\n".join(f"\t{test}" for test in self._tests)
        return base

    def __hash__(self) -> int:
        return hash(self._campus)
