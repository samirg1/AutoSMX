import os
import pathlib
import sys
from enum import StrEnum
from typing import Literal

APPLICATION_PATH = os.path.dirname(sys.executable)
ICON_PATH = pathlib.Path(APPLICATION_PATH, "autosmx.ico")

PAGE_NAMES = Literal["PROBLEM", "TEST", "TUTORIAL", "SETTINGS"]
EDITABLE_ITEM_FIELDS = Literal["room"]
PART_FIELDS = Literal["manufacturer", "manufacturer_part_number", "part_desc"]

SYSMODTIME_FORMAT = r"%Y-%m-%d %H:%M:%S.%f"
DAYMONTHYEAR_FORMAT = r"%d-%m-%Y"
SIMPLIFIED_TIME_FORMAT = r"%I:%M%p"

DEFAULT_TEXT_COLOUR_LABEL = "black"
ERROR_TEXT_COLOUR_LABEL = "indian red"
UNSYNCED_TEXT_COLOUR_LABEL = "SteelBlue4"

DEFAULT_TEXT_COLOUR_BUTTON = "white"
FOCUSED_TEXT_COLOUR_BUTTON = "black"
BASE_FILE = rf"C:\Users\{os.getenv('USERNAME')}\AppData\Local\SMXMobile"

HORIZONTAL_LINE = "-" * 600
CTK_TEXT_START = "1.0"

NA = "N/A"
NO = "No"
TRACK_LOAD_TEST = "200"
SPACE = " "

ON = "on"
OFF = "off"

OPTION_SELECT_POPUP_WIDTH = 1440
ADD_SCRIPT_POPUP_WIDTH = 1080


class DatabaseFilenames(StrEnum):
    TESTS = "SCMTests"
    ASSETS = "SCMAssets"
    LOOKUP = "SCMLookup"
    SETTINGS = "Settings"
