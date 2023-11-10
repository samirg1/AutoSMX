import configparser

from utils.constants import BASE_FILE


def get_user() -> str:
    parser = configparser.ConfigParser()
    parser.read(rf"{BASE_FILE}\SMX.ini")
    return parser.get("Misc", "LastUser")
