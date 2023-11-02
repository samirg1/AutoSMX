from typing import NamedTuple


class ScriptInfo(NamedTuple):
    number: int
    tester_number: str
    nickname: str
    search_terms: list[str]
    exact_matches: list[str]
