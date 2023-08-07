from design import Test


class Job:
    def __init__(self, company: str, campus: str, department: str) -> None:
        self.company = company
        self.campus = campus
        self.department = department
        self.tests: list[Test] = []

    def add_test(self, test: Test):
        self.tests.append(test)

    def __str__(self) -> str:
        return f"{self.campus}\n{self.company}\n{self.department}"

    def full_info(self) -> str:
        base = f"{str(self)}\nTests:\n"
        base += "\n".join(f"\t{test}" for test in self.tests)
        return base

    def __hash__(self) -> int:
        return hash(self.campus)
