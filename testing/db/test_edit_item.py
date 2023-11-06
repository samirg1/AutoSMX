from testing.conftest import MockSqlObject
from db.edit_item import edit_item


def test_get_item_no_update(mock_sql_connect: MockSqlObject) -> None:
    edit_item("12345", {})

    assert len(mock_sql_connect.calls) == 0


def test_get_item(mock_sql_connect: MockSqlObject) -> None:
    edit_item("12345", {"room": "Room 1"})

    assert len(mock_sql_connect.calls) == 1
    ((sql, variables),) = mock_sql_connect.calls
    assert "room = ?" in sql
    assert len(variables) == 4
    assert variables[2] == "Room 1"
    assert variables[3] == "12345"
