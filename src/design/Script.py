from attrs import field, frozen


class ScriptLine:
    def __init__(self, text: str, number: int, *options: str) -> None:
        self.text = text
        self.number = number
        self.default = options[0] if options else ""
        self.options = options
        self.result = ""

    def __repr__(self) -> str:
        return f"{self.text} -> {self.options}"


@frozen(repr=False)
class Script:
    nickname: str = field(hash=False, eq=False)
    name: str = field(hash=False, eq=False)
    number: int
    tester_number: str = field(hash=False, eq=False)
    service_type: str = field(hash=False, eq=False)
    lines: tuple[ScriptLine, ...] = field(factory=tuple, hash=False, eq=False)
    exact_matches: list[str] = field(factory=list, kw_only=True, hash=False, eq=False)
    search_terms: list[str] = field(factory=list, kw_only=True, hash=False, eq=False)

    def __attrs_post_init__(self) -> None:
        self.search_terms.append(self.nickname)

    def is_for(self, item_description: str) -> bool:
        return any(term in item_description for term in self.search_terms)

    def __str__(self) -> str:
        return self.name
