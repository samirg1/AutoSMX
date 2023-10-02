from design.Script import Script
from design.ScriptInfo import ScriptInfo
from db.get_script import get_script

_NA = "N/A"
_NO = "No"
_LOAD = "200"
_199 = "199"

_CONDITION_LINES = {8877, 8305, 9610, 9599, 8315, 8237, 8284, 8333, 8324, 6014, 8248}

_LINE_DEFAULTS: dict[int, str] = {
    8875: _NA,  # SLING: velcro
    8291: _NA,  # CEILING: charger
    8298: _NA,  # : sling
    8303: _NA,  # : reset
    8306: _NO,  # : usage
    9850: _NA,  # TRACK: charger
    9851: _LOAD,  # : load test
    9853: _NA,  # : electrical
    9608: _NA,  # WALKER: attachments
    9611: _NO,  # : needs attention
    9596: _NA,  # TABLE: charger
    9597: _NA,  # : battery
    9600: _NO,  # : needs attention
    8312: _NA,  # COMMODE: charger
    8313: _NA,  # : battery
    8236: _NA,  # BED: battery/charger
    8238: _NA,  # : self help pole
    8273: _NA,  # FLOOR: charger
    8274: _NA,  # : battey
    8277: _NA,  # : sling
    8283: _NA,  # : reset
    8285: _NO,  # : usage
    8330: _NA,  # TUB: charger
    8331: _NA,  # : battey
    8321: _NA,  # SCALE: charger
    2824: _NA,  # CHARGER: battery
    2827: _NA,  # : accessories
    481: _NA,  # CLASSII: battery
    483: _NA,  # : accessories
    478: _199,  # : insulation resistance
    479: _199,  # : insulation resistance enclosure
    6019: _NA,  # WHEELCHAIR: attachments
    6010: _NA,  # : charger
    6011: _NA,  # : battery
    6012: _NA,  # : electric controls
    2507: _NA,  # FURNITURE: missing components
    2510: _NA,  # : electrical check
}


_SCRIPT_INFOS: tuple[ScriptInfo, ...] = (
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

_scripts: dict[str, Script] = {}


def get_all_scripts() -> dict[str, Script]:
    global _scripts
    if not _scripts:
        _scripts = {info.nickname: get_script(info, _LINE_DEFAULTS, _CONDITION_LINES) for info in _SCRIPT_INFOS}
    return _scripts


SCRIPT_DOWNS: dict[int, int] = {script.number: i for i, script in enumerate(_SCRIPT_INFOS)}
