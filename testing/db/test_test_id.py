import pytest

from db.get_new_test_id import NoTestIDsError, get_new_test_id
from testing.conftest import MockSqlObject


@pytest.mark.parametrize("mock_sql_connect", ([(20, 30), None, (21, 30), None],), indirect=True)
def test_get_id(mock_sql_connect: MockSqlObject) -> None:
    test_id = get_new_test_id()
    assert test_id == "SMX0000000021"
    test_id = get_new_test_id()
    assert test_id == "SMX0000000022"


@pytest.mark.parametrize("mock_sql_connect", ([None],), indirect=True)
def test_get_id_fail(mock_sql_connect: MockSqlObject) -> None:
    with pytest.raises(NoTestIDsError):
        get_new_test_id()
