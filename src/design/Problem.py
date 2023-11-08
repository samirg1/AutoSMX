from attrs import field, frozen

from db.get_open_problems import OpenProblem, get_open_problems
from design.Test import Test


@frozen(repr=False)
class Problem:
    company: str = field(hash=False, eq=False)
    campus: str
    department: str | None = field(hash=False, eq=False)
    number: str = field(hash=False, eq=False)
    customer_number: str = field(hash=False, eq=False)
    get_open_problems: bool = field(default=True, hash=False, eq=False, kw_only=True)
    open_problems: list[OpenProblem] = field(factory=list, init=False, hash=False, eq=False)
    tests: list[Test] = field(factory=list, init=False, hash=False, eq=False)
    item_number_to_tests: dict[str, list[Test]] = field(factory=dict, init=False, hash=False, eq=False)
    previous_item_number: str = field(factory=str, init=False, hash=False, eq=False)
    test_breakdown: dict[str, int] = field(factory=dict, init=False, hash=False, eq=False)

    def __attrs_post_init__(self) -> None:
        if self.get_open_problems:
            self.open_problems.extend(get_open_problems(self.campus))

    def add_test(self, test: Test) -> None:
        self.tests.append(test)
        self.test_breakdown[test.script.nickname] = self.test_breakdown.get(test.script.nickname, 0) + 1
        self.item_number_to_tests[test.item.number] = self.item_number_to_tests.get(test.item.number, []) + [test]

    def remove_test(self, test: Test) -> None:
        self.tests.remove(test)
        self.test_breakdown[test.script.nickname] -= 1
        if self.test_breakdown[test.script.nickname] == 0:
            del self.test_breakdown[test.script.nickname]
        self.item_number_to_tests[test.item.number].remove(test)

    def set_previous_item_number(self, number: str) -> None:
        object.__setattr__(self, "previous_item_number", number)

    def __str__(self) -> str:
        return f"{self.number} - {self.campus} - {self.company}"
