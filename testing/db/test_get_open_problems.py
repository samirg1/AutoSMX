import pytest

from db.get_open_problems import get_open_problems
from testing.conftest import MockSqlObject

problem = ("123", "description", "2019-01-01 03:45:44.759", "bed", "serial")


@pytest.mark.parametrize("mock_sql_connect", ([[problem]],), indirect=True)
def test_get_open_problems(mock_sql_connect: MockSqlObject) -> None:
    problems = get_open_problems("location")

    assert len(problems) == 1
    assert repr(problems[0]) == "123 - Opened: 01-01-2019 - bed (serial) : description"
