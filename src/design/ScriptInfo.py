from typing import NamedTuple


class ScriptInfo(NamedTuple):
    number: int
    tester_number: str
    nickname: str
    search_terms: list[str]
    exact_matches: list[str]


class AddedScript(NamedTuple):
    info: ScriptInfo
    condition_line: int | None
    line_defaults: dict[int, str]
    required_fields: list[int]
    non_persistent_fields: list[int]
