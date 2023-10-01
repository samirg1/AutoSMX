from typing import NamedTuple

class ScriptInfo(NamedTuple):
    number: int
    nickname: str
    search_terms: list[str]
    exact_matches: list[str]
    