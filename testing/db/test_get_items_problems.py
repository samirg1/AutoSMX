import pytest

from db.get_items import get_items
from db.get_problems import get_problems
from testing.conftest import MockSqlObject

problem = [("company", "campus", "department", "number", 123)]


@pytest.mark.parametrize(("problem_number", "mock_sql_connect"), (["23314115", [problem, []]], ["PM1242522", [problem, []]]), indirect=["mock_sql_connect"])
def test_get_problem(problem_number: str, mock_sql_connect: MockSqlObject) -> None:
    problem = get_problems(problem_number)[0]
    assert problem
    assert problem.company == "company"
    assert problem.campus == "campus"
    assert problem.department == "department"
    assert problem.number == "number"
    assert problem_number in mock_sql_connect.calls[0][1][0]
    assert mock_sql_connect.close_called


item = [("number", "customer_number", "description", "model", "manufacturer", "serial", "room", "2019-01-01 03:45:44.759")]


@pytest.mark.parametrize("mock_sql_connect", ([item],), indirect=True)
def test_get_item(mock_sql_connect: MockSqlObject) -> None:
    item = get_items("123456")[0]
    assert item
    assert item.number == "number"
    assert item.customer_barcode == "customer_number"
    assert item.description == "description"
    assert item.model == "model"
    assert item.manufacturer == "manufacturer"
    assert item.serial == "serial"
    assert item.room == "room"
    assert item.last_update
    assert item.last_update.strftime(r"%Y-%m-%d %H:%M:%S") == "2019-01-01 03:45:44"
    assert "123456" in mock_sql_connect.calls[0][1][0]
    assert mock_sql_connect.close_called
