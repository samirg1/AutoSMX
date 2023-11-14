import functools

from db.get_script import get_script
from design.Script import Script
from design.ScriptInfo import ScriptInfo

_NA = "N/A"
_NO = "No"
_LOAD = "200"
_SPACE = " "

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
    460: _NA,  # CLASSI: fuses and circuit
    462: _SPACE,  # : earth Resistance with detachable lead
    463: _SPACE,  # : earth Resistance fixed power lead
    468: _NA,  # : battery
    481: _NA,  # CLASSII: battery
    483: _NA,  # : accessories
    477: _SPACE,  # : earth resistance
    485: _SPACE,  # : touch current
    6019: _NA,  # WHEELCHAIR: attachments
    6010: _NA,  # : charger
    6011: _NA,  # : battery
    6012: _NA,  # : electric controls
    2507: _NA,  # FURNITURE: missing components
    2510: _NA,  # : electrical check
}

_REQUIRED_FREE_TEXT_FIELDS = {
    *_CONDITION_LINES,
    461,  # CLASS I: earth resistance power lead only
    464,  # : insulation resistance
    465,  # : earth leakage current
    466,  # : earth leakage current noc
    471,  # : mains lead number
    472,  # : touch current normal condition
    473,  # : touch current sfc
    474,  # : touch current noc
    478,  # CLASSII: insulation resistance
    479,  # : insulation resistance enclosure
    485,  # : touch current
    484,  # : mains lead number
    9851,  # TRACK: load test kg
}

_NON_PERSISTENT_LINES = {
    *_CONDITION_LINES,
    461,  # CLASS I: earth resistance power lead only
    464,  # : insulation resistance
    465,  # : earth leakage current
    466,  # : earth leakage current noc
    471,  # : mains lead number
    472,  # : touch current normal condition
    473,  # : touch current sfc
    474,  # : touch current noc
    478,  # CLASSII: insulation resistance
    479,  # : insulation resistance enclosure
    485,  # : touch current
    484,  # : mains lead number
    8304, # CEILING: number of lifts
}


_SCRIPT_INFOS: tuple[ScriptInfo, ...] = (
    ScriptInfo(1278, "9999TEST", "CHANGE TILT TABLE", [], []),
    ScriptInfo(1261, "9999TEST", "SLING", [], ["SLING", "PATIENT TRANSFER SLING, MECHANICAL LIFT"]),
    ScriptInfo(1279, "9999TEST", "WALKER", ["WALK", "STAND", "STEDY"], []),
    ScriptInfo(1227, "9999TEST", "CEILING", [], ["HOIST, CEILING", "LIFTS, PATIENT TRANSFER, OVERHEAD TRACK"]),
    ScriptInfo(1287, "9999TEST", "TRACK", [], ["TRACK", "TRACK, CEILING HOIST", "CEILING TRACK"]),
    ScriptInfo(1228, "9999TEST", "COMMODE", [], []),
    ScriptInfo(1222, "9999TEST", "BED", [], []),
    ScriptInfo(1226, "9999TEST", "FLOOR", ["LIFTS"], ["HOIST, STANDING", "STANDING HOIST"]),
    ScriptInfo(1223, "9999TEST", "RECLINER", [], []),
    ScriptInfo(1230, "9999TEST", "TUB", ["BATH"], ["BATH BED"]),
    ScriptInfo(1229, "9999TEST", "SCALE", ["WEIGH"], []),
    ScriptInfo(1113, "9999TEST", "WHEELCHAIR", [], []),
    ScriptInfo(859, "9999TEST", "CHARGER", [], []),
    ScriptInfo(1065, "9999TEST", "BATTERY", [], []),
    ScriptInfo(606, "11083TEST", "CLASS II", [], []),
    ScriptInfo(799, "9999TEST", "FURNITURE", ["OVERBED"], []),
    ScriptInfo(1190, "9999TEST", "VISUAL", [], []),
    ScriptInfo(1302, "9999TEST", "HR900 BED", [], []),
    ScriptInfo(605, "11083TEST", "CLASS I", [], []),
)


@functools.lru_cache(maxsize=1)
def get_all_scripts() -> dict[str, Script]:
    return {info.nickname: get_script(info, _LINE_DEFAULTS, _CONDITION_LINES, _REQUIRED_FREE_TEXT_FIELDS, _NON_PERSISTENT_LINES) for info in _SCRIPT_INFOS}
