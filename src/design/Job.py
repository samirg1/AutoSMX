from attrs import field, frozen

from design.Test import Test


@frozen(repr=False)
class Job:
    company: str = field(hash=False, eq=False)
    campus: str
    department: str = field(hash=False, eq=False)
    tests: list[Test] = field(factory=list, init=False, hash=False, eq=False)
    test_breakdown: dict[str, int] = field(factory=dict, init=False, hash=False, eq=False)

    def add_test(self, test: Test):
        self.tests.append(test)
        self.test_breakdown[test.script.nickname] = self.test_breakdown.get(test.script.nickname, 0) + 1

    def __str__(self) -> str:
        return f"{self.campus}\n{self.company}\n{self.department}"

    def full_info(self) -> str:
        base = f"{str(self)}\nTests:\n"
        base += "\n".join(f"\t{test}" for test in self.tests)
        return base
