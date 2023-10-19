from db.get_connection import BASE_FILE
import configparser


def get_user() -> str:
    parser = configparser.ConfigParser()
    parser.read(fr"{BASE_FILE}\SMX.ini")
    return parser.get("Misc", "LastUser")
