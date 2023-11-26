from typing import NamedTuple

from design.ScriptInfo import ScriptInfo


class AddedScript(NamedTuple):
    info: ScriptInfo
    condition_line: int | None
    line_defaults: dict[int, str]
    required_fields: list[int]
    non_persistent_fields: list[int]
