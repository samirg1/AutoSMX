from typing import Sequence
from db.get_script import get_script
from design.Script import Script
from design.ScriptInfo import ScriptInfo
from utils.script_infos import SCRIPT_INFOS
from utils.constants import ImmutableDict


_available_scripts: ImmutableDict[str, Script] | None = None


def get_available_scripts(added_script_infos: Sequence[ScriptInfo] | None = None, deleteds: set[int] | None = None) -> ImmutableDict[str, Script]:
    global _available_scripts
    if added_script_infos is None and deleteds is None:
        if _available_scripts is None:
            raise ValueError("using empty argument 'get_all_scripts' when scripts have not been set")
        return _available_scripts

    deleteds = deleteds or set()
    added_script_infos = added_script_infos or []
    script_infos = [info for info in SCRIPT_INFOS if info.number not in deleteds]
    for info in added_script_infos:
        if info.number in deleteds:
            continue
        try:
            duplicate_index = next(i for i, s_info in enumerate(script_infos) if s_info.number == info.number)
            script_infos[duplicate_index] = info
        except StopIteration:
            script_infos.append(info)

    _available_scripts = ImmutableDict({info.nickname: get_script(info) for info in script_infos})

    return _available_scripts