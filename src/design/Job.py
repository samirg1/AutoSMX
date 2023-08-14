from dataclasses import dataclass, field
from design.Test import Test

@dataclass(frozen=True, repr=False, slots=True, order=True)
class Job:
    company: str = field(compare=False)
    campus: str = field(compare=True, hash=True)
    department: str = field(compare=False)
    tests: list[Test] = field(compare=False, default_factory=list)

    def add_test(self, test: Test):
        self.tests.append(test)

    def __str__(self) -> str:
        return f"{self.campus}\n{self.company}\n{self.department}"

    def full_info(self) -> str:
        base = f"{str(self)}\nTests:\n"
        base += "\n".join(f"\t{test}" for test in self.tests)
        return base
