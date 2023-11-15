import functools

from db.get_script import get_script
from design.Script import Script
from design.ScriptInfo import ScriptInfo
from utils.constants import NA, NO, TRACK_LOAD_TEST, SPACE

CONDITION_LINES = {8877, 8305, 9610, 9599, 8315, 8237, 8284, 8333, 8324, 6014, 8248}

LINE_DEFAULTS: dict[int, str] = {
    8875: NA,  # SLING: velcro
    8291: NA,  # CEILING: charger
    8298: NA,  # : sling
    8303: NA,  # : reset
    8306: NO,  # : usage
    9850: NA,  # TRACK: charger
    9851: TRACK_LOAD_TEST,  # : load test
    9853: NA,  # : electrical
    9608: NA,  # WALKER: attachments
    9611: NO,  # : needs attention
    9596: NA,  # TABLE: charger
    9597: NA,  # : battery
    9600: NO,  # : needs attention
    8312: NA,  # COMMODE: charger
    8313: NA,  # : battery
    8236: NA,  # BED: battery/charger
    8238: NA,  # : self help pole
    8273: NA,  # FLOOR: charger
    8274: NA,  # : battey
    8277: NA,  # : sling
    8283: NA,  # : reset
    8285: NO,  # : usage
    8330: NA,  # TUB: charger
    8331: NA,  # : battey
    8321: NA,  # SCALE: charger
    2824: NA,  # CHARGER: battery
    2827: NA,  # : accessories
    460: NA,  # CLASSI: fuses and circuit
    462: SPACE,  # : earth Resistance with detachable lead
    463: SPACE,  # : earth Resistance fixed power lead
    468: NA,  # : battery
    481: NA,  # CLASSII: battery
    483: NA,  # : accessories
    477: SPACE,  # : earth resistance
    485: SPACE,  # : touch current
    6019: NA,  # WHEELCHAIR: attachments
    6010: NA,  # : charger
    6011: NA,  # : battery
    6012: NA,  # : electric controls
    2507: NA,  # FURNITURE: missing components
    2510: NA,  # : electrical check
}

REQUIRED_FREE_TEXT_FIELDS = {
    *CONDITION_LINES,
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

NON_PERSISTENT_LINES = {
    *CONDITION_LINES,
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
    8304,  # CEILING: number of lifts
}


SCRIPT_INFOS: list[ScriptInfo] = [
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
]


@functools.lru_cache(maxsize=1)
def get_all_scripts() -> dict[str, Script]:
    return {info.nickname: get_script(info, LINE_DEFAULTS, CONDITION_LINES, REQUIRED_FREE_TEXT_FIELDS, NON_PERSISTENT_LINES) for info in SCRIPT_INFOS}
