from design.Script import Script, ScriptLine

_PASS = "Pass"
_FAIL = "Fail"
_N_A = "N/A"
_NO = "No"
_YES = "Yes"
_ONE = "1"
_ZERO = "0"
_SPACE = " "
_TRACK_LOAD = "200"
_INSULATION = "199"

_CASTORS_P = ScriptLine("CASTORS", _PASS, _N_A, _FAIL)
_FRAME_P = ScriptLine("FRAME", _PASS, _N_A, _FAIL)
_PAINT_P = ScriptLine("PAINT", _PASS, _N_A, _FAIL)
_LABELLING_P = ScriptLine("LABELLING", _PASS, _N_A, _FAIL)
_CHARGER_N = ScriptLine("CHARGER", _N_A, _PASS, _FAIL)
_BATTERY_N = ScriptLine("BATTERY", _N_A, _PASS, _FAIL)
_BATTERY_P = ScriptLine("BATTERY", _PASS, _N_A, _FAIL)
_CONTROL_P = ScriptLine("CONTROL", _PASS, _N_A, _FAIL)
_CONDITION_1 = ScriptLine("CONDITION", _ONE, _ZERO)
_FURTHER_ATTENTION_N = ScriptLine("ATTENTION?", _NO, _YES)
_DETAILS_P = ScriptLine("DETAILS", _PASS, _N_A, _FAIL)
_GENERAL_WEAR_P = ScriptLine("WEAR", _PASS, _N_A, _FAIL)
_STITCHING_P = ScriptLine("STITCHING", _PASS, _N_A, _FAIL)
_FITTINGS_P = ScriptLine("FITTINGS", _PASS, _N_A, _FAIL)
_VELCRO_N = ScriptLine("VELCRO", _N_A, _PASS, _FAIL)
_HARDWARE_P = ScriptLine("HARDWARE", _PASS, _N_A, _FAIL)
_OPERATION_P = ScriptLine("OPERATION", _PASS, _N_A, _FAIL)
_ATTACHMENTS_N = ScriptLine("ATTACHMENTS", _N_A, _PASS, _FAIL)
_STRAP_P = ScriptLine("STRAP", _PASS, _N_A, _FAIL)
_ROLLERS_P = ScriptLine("ROLLERS", _PASS, _N_A, _FAIL)
_MOTORS_P = ScriptLine("MOTORS", _PASS, _N_A, _FAIL)
_CHARGING_CONTACTS_P = ScriptLine("CONTACTS", _PASS, _N_A, _FAIL)
_STATUS_LEDS_P = ScriptLine("STATUS LEDS", _PASS, _N_A, _FAIL)
_END_LIMIT_P = ScriptLine("END LIMIT", _PASS, _N_A, _FAIL)
_SLING_INSPECTION_N = ScriptLine("SLING", _N_A, _PASS, _FAIL)
_LOAD_TEST_P = ScriptLine("LOAD TEST", _PASS, _N_A, _FAIL)
_EMERGENCY_OFF_P = ScriptLine("EMERGENCY OFF", _PASS, _N_A, _FAIL)
_MECHANICAL_LOWERING_P = ScriptLine("MECH LOWERING", _PASS, _N_A, _FAIL)
_ELECTRICAL_LOWERING_P = ScriptLine("ELEC LOWERING", _PASS, _N_A, _FAIL)
_ELECTRICAL_LIFTING_P = ScriptLine("ELEC LIFTING", _PASS, _N_A, _FAIL)
_RESET_N = ScriptLine("RESET", _N_A, _PASS, _FAIL)
_NUMBER_OF_LIFTS = ScriptLine("#LIFTS")
_USAGE_ENVIRONMENT_N = ScriptLine("ENVIRONMENT", _NO, _YES)
_FEATURES_P = ScriptLine("FEATURES", _PASS, _N_A, _FAIL)
_TRACK_DUST_P = ScriptLine("TRACK DUST", _PASS, _N_A, _FAIL)
_TRACK_LOAD_KG = ScriptLine("TRACK LOAD", _TRACK_LOAD)
_ELECTRIC_TEST_N = ScriptLine("ELECTRICALS", _N_A, _PASS, _FAIL)
_HELP_POLE_N = ScriptLine("HELP POLE", _N_A, _PASS, _FAIL)
_VISUAL_P = ScriptLine("VISUAL", _PASS, _N_A, _FAIL)
_PIVOTS_P = ScriptLine("PIVOTS", _PASS, _N_A, _FAIL)
_SWIVEL_P = ScriptLine("SWIVEL", _PASS, _N_A, _FAIL)
_ACCURACY_P = ScriptLine("ACCURACY", _PASS, _N_A, _FAIL)
_SEAT_FUNCTIONS_P = ScriptLine("SEAT FUNC", _PASS, _N_A, _FAIL)
_ELECTRIC_N = ScriptLine("ELECTRIC", _N_A, _PASS, _FAIL)
_CAPACITY_P = ScriptLine("CAPACITY", _PASS, _N_A, _FAIL)
_DATE_P = ScriptLine("DATE", _PASS, _N_A, _FAIL)
_MAINS_P = ScriptLine("MAINS", _PASS, _N_A, _FAIL)
_FUSES_P = ScriptLine("FUSES", _PASS, _N_A, _FAIL)
_EARTH_RESISTANCE = ScriptLine("EARTH R", _SPACE)
_INSULATION_RESISTANCE = ScriptLine("INSULATION R", _INSULATION)
_INSULATION_RESISTANCE_ENCLOSURE = ScriptLine("IRE", _INSULATION)
_TOUCH_CURRENT = ScriptLine("CURRENT", _SPACE)
_IEC_MAINS_LEAD = ScriptLine("IEC MAINS")
_MISSING_COMPONENTS_N = ScriptLine("MISSING", _NO, _YES)
_POLES_P = ScriptLine("POLES", _PASS, _N_A, _FAIL)
_CLEAN_P = ScriptLine("CLEAN", _PASS, _N_A, _FAIL)
_PERFORMANCE_P = ScriptLine("PERFORMANCE", _PASS, _N_A, _FAIL)
_INTEGRITY_P = ScriptLine("INTEGRITY", _PASS, _N_A, _FAIL)
_ACCESSORIES_P = ScriptLine("ACCESSORIES", _PASS, _N_A, _FAIL)
_ACTUATOR_P = ScriptLine("ACTUATOR", _PASS, _N_A, _FAIL)
_POWER_P = ScriptLine("POWER", _PASS, _N_A, _FAIL)
_CHASIS_P = ScriptLine("CHASIS", _PASS, _N_A, _FAIL)


SCRIPTS: dict[str, Script] = {
    "CHANGE TILT TABLE": Script(
        "CHANGE TILT TABLE",
        "AT - CHANGE / TILT TABLE",
        1278,
        (_CASTORS_P, _FRAME_P, _PAINT_P, _LABELLING_P, _CHARGER_N, _BATTERY_N, _CONTROL_P, _CONDITION_1, _FURTHER_ATTENTION_N),
    ),
    "SLING": Script(
        "SLING",
        "AT - SLING",
        1261,
        (_DETAILS_P, _GENERAL_WEAR_P, _STITCHING_P, _FITTINGS_P, _VELCRO_N, _LABELLING_P, _CONDITION_1),
        exact_matches=["SLING", "PATIENT TRANSFER SLING, MECHANICAL LIFT"],
    ),
    "WALKER": Script(
        "WALKER",
        "AT - WALKER / STANDER",
        1279,
        (_CASTORS_P, _CASTORS_P, _CASTORS_P, _FRAME_P, _HARDWARE_P, _PAINT_P, _OPERATION_P, _ATTACHMENTS_N, _LABELLING_P, _CONDITION_1, _FURTHER_ATTENTION_N),
        search_terms=["WALK", "STAND", "STEDY"],
    ),
    "CEILING HOIST": Script(
        "CEILING",
        "AT - CEILING HOIST",
        1227,
        (
            _OPERATION_P,
            _CONTROL_P,
            _STRAP_P,
            _ROLLERS_P,
            _MOTORS_P,
            _CHARGER_N,
            _BATTERY_P,
            _CHARGING_CONTACTS_P,
            _STATUS_LEDS_P,
            _END_LIMIT_P,
            _LABELLING_P,
            _HARDWARE_P,
            _SLING_INSPECTION_N,
            _LOAD_TEST_P,
            _EMERGENCY_OFF_P,
            _MECHANICAL_LOWERING_P,
            _ELECTRICAL_LOWERING_P,
            _RESET_N,
            _NUMBER_OF_LIFTS,
            _CONDITION_1,
            _USAGE_ENVIRONMENT_N,
        ),
        exact_matches=["HOIST, CEILING", "LIFTS, PATIENT TRANSFER, OVERHEAD TRACK"],
    ),
    "TRACK": Script(
        "TRACK",
        "AT - TRACK",
        1287,
        (_FEATURES_P, _TRACK_DUST_P, _CHARGER_N, _TRACK_LOAD_KG, _LOAD_TEST_P, _ELECTRIC_TEST_N),
        exact_matches=["TRACK", "TRACK, CEILING HOIST", "CEILING TRACK"],
    ),
    "COMMODE": Script(
        "COMMODE",
        "AT - COMMODE",
        1228,
        (_CASTORS_P, _FRAME_P, _PAINT_P, _OPERATION_P, _LABELLING_P, _CHARGER_N, _BATTERY_N, _CONTROL_P, _CONDITION_1),
    ),
    "BED": Script(
        "BED",
        "AT - ELECTRIC BED",
        1222,
        (_CASTORS_P, _FRAME_P, _HARDWARE_P, _CONTROL_P, _PAINT_P, _OPERATION_P, _LABELLING_P, _CHARGER_N, _HELP_POLE_N, _CONDITION_1),
    ),
    "FLOOR HOIST": Script(
        "FLOOR",
        "AT - FLOOR HOIST",
        1226,
        (
            _CASTORS_P,
            _VISUAL_P,
            _PIVOTS_P,
            _PAINT_P,
            _OPERATION_P,
            _HARDWARE_P,
            _CHARGER_N,
            _BATTERY_N,
            _CONTROL_P,
            _SWIVEL_P,
            _SLING_INSPECTION_N,
            _LOAD_TEST_P,
            _EMERGENCY_OFF_P,
            _MECHANICAL_LOWERING_P,
            _ELECTRICAL_LOWERING_P,
            _ELECTRICAL_LIFTING_P,
            _RESET_N,
            _CONDITION_1,
            _USAGE_ENVIRONMENT_N,
        ),
        exact_matches=["HOIST, STANDING", "STANDING HOIST"],
        search_terms=["LIFTS"],
    ),
    "RECLINER": Script(
        "RECLINER",
        "AT - LIFT RECLINER",
        1223,
        (_HARDWARE_P, _ACTUATOR_P, _CONTROL_P, _FRAME_P, _PAINT_P, _OPERATION_P, _LABELLING_P, _BATTERY_N, _POWER_P, _CONDITION_1),
    ),
    "TUB": Script(
        "TUB",
        "AT - TUB / BATH CHAIRS",
        1230,
        (_CASTORS_P, _FRAME_P, _PAINT_P, _OPERATION_P, _LABELLING_P, _CHARGER_N, _BATTERY_N, _CONTROL_P, _CONDITION_1),
        search_terms=["BATH"],
        exact_matches=["BATH BED"],
    ),
    "SCALE": Script(
        "SCALE",
        "AT - WEIGH CHAIR / SCALE",
        1229,
        (_CASTORS_P, _FRAME_P, _PAINT_P, _OPERATION_P, _LABELLING_P, _CHARGER_N, _BATTERY_P, _ACCURACY_P, _CONDITION_1),
        search_terms=["WEIGH"],
    ),
    "WHEELCHAIR": Script(
        "WHEELCHAIR",
        "AT - WHEELCHAIR",
        1113,
        (
            _CASTORS_P,
            _CASTORS_P,
            _CASTORS_P,
            _CASTORS_P,
            _CASTORS_P,
            _PAINT_P,
            _FRAME_P,
            _FRAME_P,
            _HARDWARE_P,
            _ATTACHMENTS_N,
            _PAINT_P,
            _SEAT_FUNCTIONS_P,
            _OPERATION_P,
            _OPERATION_P,
            _ATTACHMENTS_N,
            _LABELLING_P,
            _CHARGER_N,
            _BATTERY_N,
            _ELECTRIC_N,
            _ELECTRIC_N,
            _CONDITION_1,
        ),
    ),
    "CHARGER": Script(
        "CHARGER",
        "BATTERY OPERATED / VISUAL TEST",
        859,
        (_BATTERY_N, _CONTROL_P, _VISUAL_P, _ATTACHMENTS_N),
    ),
    "BATTERY": Script("BATTERY", "BATTERY PACK", 1065, (_VISUAL_P, _CAPACITY_P, _DATE_P)),
    "CLASS II": Script(
        "CLASS II",
        "CLASS II NO APPLIED PARTS",
        606,
        (_MAINS_P, _FUSES_P, _CONTROL_P, _BATTERY_N, _VISUAL_P, _ATTACHMENTS_N, _EARTH_RESISTANCE, _INSULATION_RESISTANCE, _INSULATION_RESISTANCE_ENCLOSURE, _TOUCH_CURRENT, _IEC_MAINS_LEAD),
    ),
    "FURNITURE": Script(
        "FURNITURE",
        "FURNITURE GENERIC",
        799,
        (_CHASIS_P, _CASTORS_P, _CASTORS_P, _PAINT_P, _CASTORS_P, _MISSING_COMPONENTS_N, _POLES_P, _CLEAN_P, _ELECTRIC_N, _PERFORMANCE_P),
        search_terms=["OVERBED"],
    ),
    "VISUAL": Script("VISUAL", "VISUAL INSPECTION ONLY", 1190, (_INTEGRITY_P, _ACCESSORIES_P)),
}

SCRIPT_DOWNS: dict[str, int] = {script.nickname: i for i, script in enumerate(SCRIPTS.values())}
