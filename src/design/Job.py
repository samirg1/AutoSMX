from attrs import field, frozen

from design.Test import Test
from db.get_open_problems import Problem, get_open_problems

_JOB_COMPANIES_SEARCH = {"ABLE": "ABLE", "CAMPEYN": "CAMPEYN", "BENETAS": "BENETAS", "JEWISH CARE": "JEWISH"}


def _job_company_converter(original_company: str) -> str:
    for company, search_term in _JOB_COMPANIES_SEARCH.items():
        if search_term in original_company:
            return company
    return original_company


@frozen(repr=False)
class Job:
    company: str = field(hash=False, eq=False, converter=_job_company_converter)
    campus: str
    department: str = field(hash=False, eq=False)
    number: str = field(hash=False, eq=False)
    customer_number: int = field(hash=False, eq=False, converter=int)
    get_problems: bool = field(default=True, hash=False, eq=False, kw_only=True)
    open_problems: list[Problem] = field(factory=list, init=False, hash=False, eq=False)
    tests: list[Test] = field(factory=list, init=False, hash=False, eq=False)
    test_breakdown: dict[str, int] = field(factory=dict, init=False, hash=False, eq=False)

    def __attrs_post_init__(self) -> None:
        if self.get_problems:
            self.open_problems.extend(get_open_problems(self.campus))

    def add_test(self, test: Test) -> None:
        self.tests.append(test)
        self.test_breakdown[test.script.nickname] = self.test_breakdown.get(test.script.nickname, 0) + 1

    def remove_test(self, test: Test) -> None:
        self.tests.remove(test)
        self.test_breakdown[test.script.nickname] -= 1
        if self.test_breakdown[test.script.nickname] == 0:
            del self.test_breakdown[test.script.nickname]

    def __str__(self) -> str:
        return f"{self.campus}\n{self.company}\n{self.number}"
