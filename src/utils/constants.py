import os
import pathlib
import pyautogui
import sys
from enum import StrEnum
from typing import Literal

APP_NAME = "AutoSMX"

IS_DEV_MODE = "--dev" in sys.argv
APPLICATION_PATH = "" if IS_DEV_MODE else os.path.dirname(sys.executable)
ICON_PATH = pathlib.Path(APPLICATION_PATH, "autosmx.ico")

SCREEN_WIDTH, SCREEN_HEIGHT = pyautogui.size()
APP_WIDTH = SCREEN_WIDTH - 410
APP_HEIGHT = SCREEN_HEIGHT - 290
APP_GEOMETRY = f"{APP_WIDTH}x{APP_HEIGHT}+0+0"

OPTION_SELECT_POPUP_WIDTH = 1440
ADD_SCRIPT_POPUP_WIDTH = 1080
PART_POPUP_WIDTH = 1080

PAGE_NAMES = Literal["PROBLEM", "TEST", "TUTORIAL", "SETTINGS", "SCRIPTS"]
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

HORIZONTAL_LINE = "-" * 600
CTK_TEXT_START = "1.0"

NA = "N/A"
NO = "No"
TRACK_LOAD_TEST = "200"
SPACE = " "

ON = "on"
OFF = "off"


BASE_PATH = pathlib.Path("~", "AppData", "Local", "SMXMobile").expanduser()
SYNC_LOG_PATH = BASE_PATH / "SCMSync.log"
SYNC_EXECUTABLE_NAME = "SCMSync.exe"
SYNC_EXECUTABLE_PATH = pathlib.Path("C:\\Program Files (x86)", "SMX", SYNC_EXECUTABLE_NAME)

PASS_WITH_CONDITIONS_RESULT = "Pass W/C"


class DatabaseFilenames(StrEnum):
    TESTS = "SCMTests"
    ASSETS = "SCMAssets"
    LOOKUP = "SCMLookup"
    SETTINGS = "Settings"


ImmutableDict = dict  # don't edit this dictionary
