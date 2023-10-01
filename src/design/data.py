from design.Script import Script
from design.ScriptInfo import ScriptInfo
from db.get_script import get_script


SCRIPT_INFOS: tuple[ScriptInfo, ...] = (
    ScriptInfo(1278, "CHANGE TILT TABLE", [], []),
    ScriptInfo(1261, "SLING", [], ["SLING", "PATIENT TRANSFER SLING, MECHANICAL LIFT"]),
    ScriptInfo(1279, "WALKER", ["WALK", "STAND", "STEDY"], []),
    ScriptInfo(1227, "CEILING", [], ["HOIST, CEILING", "LIFTS, PATIENT TRANSFER, OVERHEAD TRACK"]),
    ScriptInfo(1287, "TRACK", [], ["TRACK", "TRACK, CEILING HOIST", "CEILING TRACK"]),
    ScriptInfo(1228, "COMMODE", [], []),
    ScriptInfo(1222, "BED", [], []),
    ScriptInfo(1226, "FLOOR", ["LIFTS"], ["HOIST, STANDING", "STANDING HOIST"]),
    ScriptInfo(1223, "RECLINER", [], []),
    ScriptInfo(1230, "TUB", ["BATH"], ["BATH BED"]),
    ScriptInfo(1229, "SCALE", ["WEIGH"], []),
    ScriptInfo(1113, "WHEELCHAIR", [], []),
    ScriptInfo(859, "CHARGER", [], []),
    ScriptInfo(1065, "BATTERY", [], []),
    ScriptInfo(606, "CLASS II", [], []),
    ScriptInfo(799, "FURNITURE", ["OVERBED"], []),
    ScriptInfo(1190, "VISUAL", [], []),
)

SCRIPTS: dict[str, Script] = {info.nickname: get_script(info) for info in SCRIPT_INFOS}
SCRIPT_DOWNS: dict[int, int] = {script.number: i for i, script in enumerate(sorted(SCRIPTS.values(), key=lambda script: script.name))}
