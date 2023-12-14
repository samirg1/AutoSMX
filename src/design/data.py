from design.ScriptInfo import ScriptInfo
from utils.constants import NA, NO, SPACE, TRACK_LOAD_TEST


SCRIPT_INFOS = (
    ScriptInfo(1278, "9999TEST", "TABLE", {9596: NA, 9597: NA, 9600: NO}, condition_line=9599),
    ScriptInfo(1261, "9999TEST", "SLING", {8875: NA}, exact_matches=("SLING", "PATIENT TRANSFER SLING, MECHANICAL LIFT"), condition_line=8877),
    ScriptInfo(1279, "9999TEST", "WALKER", {9608: NA, 9611: NO}, search_terms=("WALK", "STAND", "STEDY"), condition_line=9610),
    ScriptInfo(
        1227,
        "9999TEST",
        "CEILING",
        {8291: NA, 8298: NA, 8303: NA, 8306: NO, 8304: NA},
        exact_matches=("HOIST, CEILING", "LIFTS, PATIENT TRANSFER, OVERHEAD TRACK"),
        condition_line=8305,
        non_persistent_fields=(8304,),
    ),
    ScriptInfo(1287, "9999TEST", "TRACK", {9850: NA, 9851: TRACK_LOAD_TEST, 9853: NA}, exact_matches=("TRACK", "TRACK, CEILING HOIST", "CEILING TRACK"), required_fields=(9851,)),
    ScriptInfo(1228, "9999TEST", "COMMODE", {8312: NA, 8313: NA}, condition_line=8315),
    ScriptInfo(1222, "9999TEST", "BED", {8236: NA, 8238: NA}, condition_line=8237, non_persistent_fields=(8238,)),
    ScriptInfo(1226, "9999TEST", "FLOOR", {8273: NA, 8274: NA, 8277: NA, 8283: NA, 8285: NO}, search_terms=("LIFTS",), exact_matches=("HOIST, STANDING", "STANDING HOIST"), condition_line=8284),
    ScriptInfo(1223, "9999TEST", "RECLINER", {}, condition_line=8248),
    ScriptInfo(1230, "9999TEST", "TUB", {8330: NA, 8331: NA}, search_terms=("BATH",), exact_matches=("BATH BED",), condition_line=8333),
    ScriptInfo(1229, "9999TEST", "SCALE", {8321: NA}, search_terms=("WEIGH",), condition_line=8324),
    ScriptInfo(1113, "9999TEST", "WHEELCHAIR", {6019: NA, 6010: NA, 6011: NA, 6012: NA, 6013: NA}, condition_line=6014),
    ScriptInfo(859, "9999TEST", "CHARGER", {2824: NA, 2827: NA}),
    ScriptInfo(1065, "9999TEST", "BATTERY", {}),
    ScriptInfo(606, "11083TEST", "CLASS II", {481: NA, 483: NA, 477: SPACE}, required_fields=(478, 479, 485, 484), non_persistent_fields=(478, 479, 485, 484)),
    ScriptInfo(799, "9999TEST", "FURNITURE", {2507: NA, 2510: NA}, search_terms=("OVERBED",)),
    ScriptInfo(1190, "9999TEST", "VISUAL", {}),
    ScriptInfo(1302, "9999TEST", "HR900 BED", {}),
    ScriptInfo(
        605,
        "11083TEST",
        "CLASS I",
        {460: NA, 462: SPACE, 463: SPACE, 468: NA},
        required_fields=(461, 464, 465, 466, 471, 472, 473, 474),
        non_persistent_fields=(461, 464, 465, 466, 471, 472, 473, 474),
    ),
)
