from design.Script import Script, ScriptTest

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

_CASTORS_P = ScriptTest("CASTORS", _PASS, _N_A, _FAIL)
_FRAME_P = ScriptTest("FRAME", _PASS, _N_A, _FAIL)
_PAINT_P = ScriptTest("PAINT", _PASS, _N_A, _FAIL)
_LABELLING_P = ScriptTest("LABELLING", _PASS, _N_A, _FAIL)
_CHARGER_N = ScriptTest("CHARGER", _N_A, _PASS, _FAIL)
_BATTERY_N = ScriptTest("BATTERY", _N_A, _PASS, _FAIL)
_BATTERY_P = ScriptTest("BATTERY", _PASS, _N_A, _FAIL)
_CONTROL_P = ScriptTest("CONTROL", _PASS, _N_A, _FAIL)
_CONDITION_1 = ScriptTest("CONDITION", _ONE, _ZERO)
_FURTHER_ATTENTION_N = ScriptTest("ATTENTION?", _NO, _YES)
_DETAILS_P = ScriptTest("DETAILS", _PASS, _N_A, _FAIL)
_GENERAL_WEAR_P = ScriptTest("WEAR", _PASS, _N_A, _FAIL)
_STITCHING_P = ScriptTest("STITCHING", _PASS, _N_A, _FAIL)
_FITTINGS_P = ScriptTest("FITTINGS", _PASS, _N_A, _FAIL)
_VELCRO_N = ScriptTest("VELCRO", _N_A, _PASS, _FAIL)
_HARDWARE_P = ScriptTest("HARDWARE", _PASS, _N_A, _FAIL)
_OPERATION_P = ScriptTest("OPERATION", _PASS, _N_A, _FAIL)
_ATTACHMENTS_N = ScriptTest("ATTACHMENTS", _N_A, _PASS, _FAIL)
_STRAP_P = ScriptTest("STRAP", _PASS, _N_A, _FAIL)
_ROLLERS_P = ScriptTest("ROLLERS", _PASS, _N_A, _FAIL)
_MOTORS_P = ScriptTest("MOTORS", _PASS, _N_A, _FAIL)
_CHARGING_CONTACTS_P = ScriptTest("CONTACTS", _PASS, _N_A, _FAIL)
_STATUS_LEDS_P = ScriptTest("STATUS LEDS", _PASS, _N_A, _FAIL)
_END_LIMIT_P = ScriptTest("END LIMIT", _PASS, _N_A, _FAIL)
_SLING_INSPECTION_N = ScriptTest("SLING", _N_A, _PASS, _FAIL)
_LOAD_TEST_P = ScriptTest("LOAD TEST", _PASS, _N_A, _FAIL)
_EMERGENCY_OFF_P = ScriptTest("EMERGENCY OFF", _PASS, _N_A, _FAIL)
_MECHANICAL_LOWERING_P = ScriptTest("MECH LOWERING", _PASS, _N_A, _FAIL)
_ELECTRICAL_LOWERING_P = ScriptTest("ELEC LOWERING", _PASS, _N_A, _FAIL)
_ELECTRICAL_LIFTING_P = ScriptTest("ELEC LIFTING", _PASS, _N_A, _FAIL)
_RESET_N = ScriptTest("RESET", _N_A, _PASS, _FAIL)
_NUMBER_OF_LIFTS = ScriptTest("#LIFTS")
_USAGE_ENVIRONMENT_N = ScriptTest("ENVIRONMENT", _NO, _YES)
_FEATURES_P = ScriptTest("FEATURES", _PASS, _N_A, _FAIL)
_TRACK_DUST_P = ScriptTest("TRACK DUST", _PASS, _N_A, _FAIL)
_TRACK_LOAD_KG = ScriptTest("TRACK LOAD", _TRACK_LOAD)
_ELECTRIC_TEST_N = ScriptTest("ELECTRICALS", _N_A, _PASS, _FAIL)
_HELP_POLE_N = ScriptTest("HELP POLE", _N_A, _PASS, _FAIL)
_VISUAL_P = ScriptTest("VISUAL", _PASS, _N_A, _FAIL)
_PIVOTS_P = ScriptTest("PIVOTS", _PASS, _N_A, _FAIL)
_SWIVEL_P = ScriptTest("SWIVEL", _PASS, _N_A, _FAIL)
_ACCURACY_P = ScriptTest("ACCURACY", _PASS, _N_A, _FAIL)
_SEAT_FUNCTIONS_P = ScriptTest("SEAT FUNC", _PASS, _N_A, _FAIL)
_ELECTRIC_N = ScriptTest("ELECTRIC", _N_A, _PASS, _FAIL)
_CAPACITY_P = ScriptTest("CAPACITY", _PASS, _N_A, _FAIL)
_DATE_P = ScriptTest("DATE", _PASS, _N_A, _FAIL)
_MAINS_P = ScriptTest("MAINS", _PASS, _N_A, _FAIL)
_FUSES_P = ScriptTest("FUSES", _PASS, _N_A, _FAIL)
_EARTH_RESISTANCE = ScriptTest("EARTH R", _SPACE)
_INSULATION_RESISTANCE = ScriptTest("INSULATION R", _INSULATION)
_INSULATION_RESISTANCE_ENCLOSURE = ScriptTest("IRE", _INSULATION)
_TOUCH_CURRENT = ScriptTest("CURRENT", _SPACE)
_IEC_MAINS_LEAD = ScriptTest("IEC MAINS")
_MISSING_COMPONENTS_N = ScriptTest("MISSING", _NO, _YES)
_POLES_P = ScriptTest("POLES", _PASS, _N_A, _FAIL)
_CLEAN_P = ScriptTest("CLEAN", _PASS, _N_A, _FAIL)
_PERFORMANCE_P = ScriptTest("PERFORMANCE", _PASS, _N_A, _FAIL)
_INTEGRITY_P = ScriptTest("INTEGRITY", _PASS, _N_A, _FAIL)
_ACCESSORIES_P = ScriptTest("ACCESSORIES", _PASS, _N_A, _FAIL)
_ACTUATOR_P = ScriptTest("ACTUATOR", _PASS, _N_A, _FAIL)


SCRIPTS: dict[str, Script] = {
    "CHANGE TILT TABLE": Script(
        "CHANGE TILT TABLE",
        "AT - CHANGE / TILT TABLE, ELECTRIC/MANUAL",
        (_CASTORS_P, _FRAME_P, _PAINT_P, _LABELLING_P, _CHARGER_N, _BATTERY_N, _CONTROL_P, _CONDITION_1, _FURTHER_ATTENTION_N),
    ),
    "SLING": Script(
        "SLING",
        "AT - SLING",
        (_DETAILS_P, _GENERAL_WEAR_P, _STITCHING_P, _FITTINGS_P, _VELCRO_N, _LABELLING_P, _CONDITION_1),
        exact_matches=["SLING", "PATIENT TRANSFER SLING, MECHANICAL LIFT"],
    ),
    "WALKER": Script(
        "WALKER",
        "AT - WALKER / STANDER",
        (_CASTORS_P, _CASTORS_P, _CASTORS_P, _FRAME_P, _HARDWARE_P, _PAINT_P, _OPERATION_P, _ATTACHMENTS_N, _LABELLING_P, _CONDITION_1, _FURTHER_ATTENTION_N),
        search_terms=["WALK", "STAND", "STEDY"],
    ),
    "CEILING HOIST": Script(
        "CEILING",
        "AT - CEILING HOIST",
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
        (_FEATURES_P, _TRACK_DUST_P, _CHARGER_N, _TRACK_LOAD_KG, _LOAD_TEST_P, _ELECTRIC_TEST_N),
        exact_matches=["TRACK", "TRACK, CEILING HOIST"],
    ),
    "COMMODE": Script(
        "COMMODE",
        "AT - COMMODE",
        (_CASTORS_P, _FRAME_P, _PAINT_P, _OPERATION_P, _LABELLING_P, _CHARGER_N, _BATTERY_N, _CONTROL_P, _CONDITION_1),
    ),
    "BED": Script(
        "BED",
        "AT - ELECTRIC BED",
        (_CASTORS_P, _FRAME_P, _HARDWARE_P, _CONTROL_P, _PAINT_P, _OPERATION_P, _LABELLING_P, _CHARGER_N, _HELP_POLE_N, _CONDITION_1),
    ),
    "FLOOR HOIST": Script(
        "FLOOR",
        "AT - FLOOR HOIST",
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
        exact_matches=["HOIST, STANDING"],
        search_terms=["LIFTS"],
    ),
    "RECLINER": Script(
        "RECLINER",
        "AT - LIFT RECLINER",
        (_HARDWARE_P, _ACTUATOR_P, _CONTROL_P, _FRAME_P, _PAINT_P, _OPERATION_P, _LABELLING_P, _BATTERY_N, _CONDITION_1),
    ),
    "TUB": Script(
        "TUB",
        "AT - TUB / BATH CHAIRS",
        (_CASTORS_P, _FRAME_P, _PAINT_P, _OPERATION_P, _LABELLING_P, _CHARGER_N, _BATTERY_N, _CONTROL_P, _CONDITION_1),
        search_terms=["BATH"],
        exact_matches=["BATH BED"],
    ),
    "SCALE": Script(
        "SCALE",
        "AT - WEIGH CHAIR / SCALE",
        (_CASTORS_P, _FRAME_P, _PAINT_P, _OPERATION_P, _LABELLING_P, _CHARGER_N, _BATTERY_P, _ACCURACY_P, _CONDITION_1),
        search_terms=["WEIGH"],
    ),
    "WHEELCHAIR": Script(
        "WHEELCHAIR",
        "AT - WHEELCHAIR",
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
        (_BATTERY_N, _CONTROL_P, _VISUAL_P, _ATTACHMENTS_N),
    ),
    "BATTERY": Script("BATTERY", "BATTERY PACK", (_VISUAL_P, _CAPACITY_P, _DATE_P)),
    "CLASS II": Script(
        "CLASS II",
        "CLASS II NO APPLIED PARTS",
        (_MAINS_P, _FUSES_P, _CONTROL_P, _BATTERY_N, _VISUAL_P, _ATTACHMENTS_N, _EARTH_RESISTANCE, _INSULATION_RESISTANCE, _INSULATION_RESISTANCE_ENCLOSURE, _TOUCH_CURRENT, _IEC_MAINS_LEAD),
    ),
    "FURNITURE": Script(
        "FURNITURE",
        "FURNITURE GENERIC",
        (_CONDITION_1, _CASTORS_P, _CASTORS_P, _PAINT_P, _CASTORS_P, _MISSING_COMPONENTS_N, _POLES_P, _CLEAN_P, _ELECTRIC_N, _PERFORMANCE_P),
        search_terms=["OVERBED"],
    ),
    "VISUAL": Script("VISUAL", "VISUAL INSPECTION ONLY", (_INTEGRITY_P, _ACCESSORIES_P)),
}

SCRIPT_DOWNS: dict[str, int] = {script.nickname: i for i, script in enumerate(SCRIPTS.values())}
