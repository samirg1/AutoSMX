from attrs import field, frozen


class ScriptTest:
    def __init__(self, name: str, *options: str):
        self.name = name
        self.selected = options[0] if options else ""
        self.options = sorted(options, reverse=True)


@frozen(repr=False)
class Script:
    nickname: str = field(hash=False, eq=False)
    name: str
    downs: int = field(hash=False, eq=False)
    tests: tuple[ScriptTest, ...] = field(factory=tuple, hash=False, eq=False)
    exact_matches: list[str] = field(factory=list, kw_only=True, hash=False, eq=False)
    search_terms: list[str] = field(factory=list, kw_only=True, hash=False, eq=False)

    def __attrs_post_init__(self) -> None:
        self.search_terms.append(self.nickname)

    def is_for(self, item_description: str) -> bool:
        return any(term in item_description for term in self.search_terms)

    def __str__(self) -> str:
        return self.name
