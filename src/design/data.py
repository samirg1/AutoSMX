_PASS = "Pass"
_FAIL = "Fail"
_N_A = "N/A"
_NO = "No"
_PES = "Yes"
_ONE = "1"
_ZERO = "0"
_SPACE = " "


class ScriptTest:
    def __init__(self, name: str, *options: str):
        self.name = name
        self.selected = options[0] if options else ""
        self.options = sorted(options, key=lambda x: -1 if x == _PASS else 0 if x == _N_A else 1)


_CASTORS_P = ScriptTest("CASTORS", _PASS, _N_A, _FAIL)
_FRAME_P = ScriptTest("FRAME", _PASS, _N_A, _FAIL)
_PAINT_P = ScriptTest("PAINT", _PASS, _N_A, _FAIL)
_LABELLING_P = ScriptTest("LABELLING", _PASS, _N_A, _FAIL)
_CHARGER_N = ScriptTest("CHARGER", _N_A, _PASS, _FAIL)
_BATTERY_N = ScriptTest("BATTERY", _N_A, _PASS, _FAIL)
_BATTERY_P = ScriptTest("BATTERY", _PASS, _N_A, _FAIL)
_CONTROL_P = ScriptTest("CONTROL", _PASS, _N_A, _FAIL)
_CONDITION_1 = ScriptTest("CONDITION", _ONE, _ZERO)
_FURTHER_ATTENTION_N = ScriptTest("ATTENTION?", _NO, _PES)
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
_USAGE_ENVIRONMENT_N = ScriptTest("ENVIRONMENT", _NO, _PES)
_FEATURES_P = ScriptTest("FEATURES", _PASS, _N_A, _FAIL)
_TRACK_DUST_P = ScriptTest("TRACK DUST", _PASS, _N_A, _FAIL)
_TRACK_LOAD_KG = ScriptTest("TRACK LOAD", "200")
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
_INSULATION_RESISTANCE = ScriptTest("INSULATION R", "199")
_INSULATION_RESISTANCE_ENCLOSURE = ScriptTest("IRE", "199")
_TOUCH_CURRENT = ScriptTest("TOUCH CURRENT", _SPACE)
_IEC_MAINS_LEAD = ScriptTest("IEC MAINS")
_MISSING_COMPONENTS_N = ScriptTest("MISSING", _NO, _PES)
_POLES_P = ScriptTest("POLES", _PASS, _N_A, _FAIL)
_CLEAN_P = ScriptTest("CLEAN", _PASS, _N_A, _FAIL)
_PERFORMANCE_P = ScriptTest("PERFORMANCE", _PASS, _N_A, _FAIL)


class Script:
    def __init__(self, nickname: str, name: str, downs: int, *tests: ScriptTest, extra_terms: list[str] | None = None) -> None:
        self.nickname = nickname
        self.name = name
        self.tests = tests
        self.downs = downs
        self._search_terms = extra_terms or []
        self._search_terms.append(nickname)

    def matches(self, search: str) -> bool:
        return any(term in search for term in self._search_terms)

    def __str__(self) -> str:
        return self.name


SCRIPTS: dict[str, Script] = {
    "CHANGE TILT TABLE": Script(
        "CHANGE TILT TABLE", "AT - CHANGE / TILT TABLE, ELECTRIC/MANUAL", 0, _CASTORS_P, _FRAME_P, _PAINT_P, _LABELLING_P, _CHARGER_N, _BATTERY_N, _CONTROL_P, _CONDITION_1, _FURTHER_ATTENTION_N
    ),
    "SLING": Script("SLING", "AT - SLING", 1, _DETAILS_P, _GENERAL_WEAR_P, _STITCHING_P, _FITTINGS_P, _VELCRO_N, _LABELLING_P, _CONDITION_1),
    "WALKER": Script(
        "WALKER",
        "AT - WALKER / STANDER",
        2,
        _CASTORS_P,
        _CASTORS_P,
        _CASTORS_P,
        _FRAME_P,
        _HARDWARE_P,
        _PAINT_P,
        _OPERATION_P,
        _ATTACHMENTS_N,
        _LABELLING_P,
        _CONDITION_1,
        _FURTHER_ATTENTION_N,
        extra_terms=["WALK", "STAND", "STEDY"],
    ),
    "CEILING HOIST": Script(
        "CEILING",
        "AT - CEILING HOIST",
        3,
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
    "TRACK": Script("TRACK", "AT - TRACK", 4, _FEATURES_P, _TRACK_DUST_P, _CHARGER_N, _TRACK_LOAD_KG, _LOAD_TEST_P, _ELECTRIC_TEST_N),
    "COMMODE": Script("COMMODE", "AT - COMMODE", 5, _CASTORS_P, _FRAME_P, _PAINT_P, _OPERATION_P, _LABELLING_P, _CHARGER_N, _BATTERY_N, _CONTROL_P, _CONDITION_1),
    "BED": Script("BED", "AT - ELECTRIC BED", 6, _CASTORS_P, _FRAME_P, _HARDWARE_P, _CONTROL_P, _PAINT_P, _OPERATION_P, _LABELLING_P, _CHARGER_N, _HELP_POLE_N, _CONDITION_1),
    "FLOOR HOIST": Script(
        "FLOOR",
        "AT - FLOOR HOIST",
        7,
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
        extra_terms=["LIFTS"],
    ),
    "TUB": Script("TUB", "AT - TUB / BATH CHAIRS", 8, _CASTORS_P, _FRAME_P, _PAINT_P, _OPERATION_P, _LABELLING_P, _CHARGER_N, _BATTERY_N, _CONTROL_P, _CONDITION_1, extra_terms=["BATH"]),
    "SCALE": Script("SCALE", "AT - WEIGH CHAIR / SCALE", 9, _CASTORS_P, _FRAME_P, _PAINT_P, _OPERATION_P, _LABELLING_P, _CHARGER_N, _BATTERY_P, _ACCURACY_P, _CONDITION_1, extra_terms=["WEIGH"]),
    "WHEELCHAIR": Script(
        "WHEELCHAIR",
        "AT - WHEELCHAIR",
        10,
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
    "CHARGER": Script("CHARGER", "BATTERY OPERATED / VISUAL TEST", 11, _BATTERY_N, _CONTROL_P, _VISUAL_P, _ATTACHMENTS_N),
    "BATTERY": Script("BATTERY", "BATTERY PACK", 12, _VISUAL_P, _CAPACITY_P, _DATE_P),
    "CLASS II": Script(
        "CLASS II",
        "CLASS II NO APPLIED PARTS",
        13,
        _MAINS_P,
        _FUSES_P,
        _CONTROL_P,
        _BATTERY_N,
        _VISUAL_P,
        _ATTACHMENTS_N,
        _EARTH_RESISTANCE,
        _INSULATION_RESISTANCE,
        _INSULATION_RESISTANCE_ENCLOSURE,
        _TOUCH_CURRENT,
        _IEC_MAINS_LEAD,
    ),
    "FURNITURE": Script(
        "FURNITURE",
        "FURNITURE GENERIC",
        14,
        _CONDITION_1,
        _CASTORS_P,
        _CASTORS_P,
        _PAINT_P,
        _CASTORS_P,
        _MISSING_COMPONENTS_N,
        _POLES_P,
        _CLEAN_P,
        _ELECTRIC_N,
        _PERFORMANCE_P,
        extra_terms=["OVERBED"],
    ),
}
