from attrs import field, frozen

from design.ScriptLine import ScriptLine


@frozen(repr=False)
class Script:
    nickname: str = field(hash=False, eq=False)
    name: str = field(hash=False, eq=False)
    number: int
    tester_number: str = field(hash=False, eq=False)
    service_type: str = field(hash=False, eq=False)
    lines: tuple[ScriptLine, ...] = field(hash=False, eq=False)
    header_lines: tuple[ScriptLine, ...] = field(hash=False, eq=False)
    exact_matches: list[str] = field(factory=list, kw_only=True, hash=False, eq=False)
    search_terms: list[str] = field(factory=list, kw_only=True, hash=False, eq=False)

    def __attrs_post_init__(self) -> None:
        self.search_terms.append(self.nickname)

    def is_for(self, item_description: str) -> bool:
        return any(term in item_description for term in self.search_terms)

    def __repr__(self) -> str:
        return self.name
