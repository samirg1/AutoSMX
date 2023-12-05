import configparser

from utils.constants import BASE_PATH


def get_user() -> str:
    parser = configparser.ConfigParser()
    parser.read(BASE_PATH / "SMX.ini")
    return parser.get("Misc", "LastUser")
