from typing import Mapping
from attr import frozen, field

from utils.constants import ImmutableDict


def _immutabledict_converter(d: Mapping[int, str]) -> ImmutableDict[int, str]:
    return ImmutableDict(d)


@frozen(repr=False)
class ScriptInfo:
    number: int
    tester_number: str
    nickname: str
    line_defaults: ImmutableDict[int, str] = field(converter=_immutabledict_converter)
    search_terms: set[str] = field(converter=set, factory=set, kw_only=True)
    exact_matches: set[str] = field(converter=set, factory=set, kw_only=True)
    condition_line: int | None = field(default=None, kw_only=True)
    required_fields: frozenset[int] = field(converter=frozenset, factory=frozenset, kw_only=True)
    non_persistent_fields: frozenset[int] = field(converter=frozenset, factory=frozenset, kw_only=True)
