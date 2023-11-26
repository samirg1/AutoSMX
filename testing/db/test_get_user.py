import pathlib
from utils.constants import BASE_FILE
from db.get_user import get_user
from testing.conftest import MockConfigObject


def test_get_user(mock_config_parse: MockConfigObject) -> None:
    user = get_user()
    assert user == "test user"
    assert mock_config_parse.read_calls == [pathlib.Path(BASE_FILE, "SMX.ini")]
    assert mock_config_parse.get_calls == [("Misc", "LastUser")]
