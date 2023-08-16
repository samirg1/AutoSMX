from dataclasses import dataclass, field
from design.Test import Test


@dataclass(frozen=True, repr=False, slots=True, order=True)
class Job:
    company: str = field(compare=False)
    campus: str = field(compare=True, hash=True)
    department: str = field(compare=False)
    tests: list[Test] = field(compare=False, default_factory=list)
    test_breakdown: dict[str, int] = field(compare=False, default_factory=dict)

    def add_test(self, test: Test):
        self.tests.append(test)
        self.test_breakdown[test.script.nickname] = self.test_breakdown.get(test.script.nickname, 0) + 1

    def __str__(self) -> str:
        return f"{self.campus}\n{self.company}\n{self.department}"

    def full_info(self) -> str:
        base = f"{str(self)}\nTests:\n"
        base += "\n".join(f"\t{test}" for test in self.tests)
        return base
