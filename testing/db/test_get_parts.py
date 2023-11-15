import pytest
from db.get_parts import get_parts
from testing.conftest import MockSqlObject


def test_get_parts_empty_dict() -> None:
    assert get_parts({}) == []


part = ("12345", "manufacturer", "manufacturer number", "description")

@pytest.mark.parametrize("mock_sql_connect", ([[part], []],), indirect=True)
def test_get_parts_by_string(mock_sql_connect: MockSqlObject) -> None:
    part = get_parts("1234")
    sql, fields = mock_sql_connect.calls[0]
    assert "WHERE part_no = ?" in sql
    assert fields == ("1234",)
    assert part
    assert part.description == "description"
    assert part.number == "12345"
    assert part.manufacturer == "manufacturer"
    assert part.manufacturer_number == "manufacturer number"

    part = get_parts("1234")
    assert part is None


@pytest.mark.parametrize("mock_sql_connect", ([[part], []],), indirect=True)
def test_get_parts_by_dict(mock_sql_connect: MockSqlObject) -> None:
    parts = get_parts({"manufacturer": "manu", "part_desc": "desc"})
    sql, fields = mock_sql_connect.calls[0]
    assert "WHERE manufacturer LIKE ? AND part_desc LIKE ?" in sql
    assert fields == (r"%manu%", r"%desc%")
    assert len(parts) == 1
    part, = parts
    assert part.description == "description"
    assert part.number == "12345"
    assert part.manufacturer == "manufacturer"
    assert part.manufacturer_number == "manufacturer number"

    assert get_parts({"manufacturer": "manu", "part_desc": "desc"}) == []
