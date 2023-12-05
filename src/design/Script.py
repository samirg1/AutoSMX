from attrs import field, frozen
from db.get_tester_numbers import get_tester_numbers

from design.ScriptLine import ScriptLine



class InvalidTesterNumberError(ValueError):
    ...


@frozen(repr=False)
class Script:
    nickname: str = field(hash=False, eq=False)
    name: str = field(hash=False, eq=False)
    number: int
    tester_number: str = field(hash=False, eq=False)
    service_type: str = field(hash=False, eq=False)
    lines: tuple[ScriptLine, ...] = field(hash=False, eq=False)
    header_lines: tuple[ScriptLine, ...] = field(hash=False, eq=False)
    exact_matches: set[str] = field(factory=list, kw_only=True, hash=False, eq=False)
    search_terms: set[str] = field(factory=list, kw_only=True, hash=False, eq=False)

    def __attrs_post_init__(self) -> None:
        self.search_terms.add(self.nickname)

    def is_for(self, item_description: str) -> bool:
        return any(term in item_description for term in self.search_terms)
    
    def set_tester_number(self, tester_number: str) -> None:
        if tester_number not in get_tester_numbers():
            raise InvalidTesterNumberError(f"Tester number '{tester_number}' not found for use for any user")
        object.__setattr__(self, "tester_number", tester_number)

    def __repr__(self) -> str:
        return self.name
