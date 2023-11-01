import pytest

from db.presync_check import get_double_ups
from design.Item import Item
from design.Problem import Problem
from design.Test import Test
from testing.conftest import MockSqlObject

Test.__test__ = False  # type: ignore


@pytest.mark.parametrize("mock_sql_connect", ([[]],), indirect=True)
def test_double_ups_no_tests(mock_sql_connect: MockSqlObject) -> None:
    problem = Problem("company", "campus", "dept", "PM123", "123")
    assert get_double_ups(problem) == {}


@pytest.mark.parametrize(
    "mock_sql_connect",
    (
        [
            [],
            [("name", "desc", "overall")],
            [("name", "action")],
        ],
    ),
    indirect=True,
)
def test_no_double_ups(mock_sql_connect: MockSqlObject) -> None:
    problem = Problem("company", "campus", "dept", "PM123", "123")
    assert get_double_ups(problem) == {}


@pytest.mark.parametrize(
    "mock_sql_connect",
    (
        [
            [],
            [("name", "desc", "overall1"), ("name", "desc", "overall2")],
            [],
        ],
    ),
    indirect=True,
)
def test_item_double_ups(mock_sql_connect: MockSqlObject) -> None:
    problem = Problem("company", "campus", "dept", "PM123", "123")
    problem.tests.append(Test(Item("", "", "", "", "", "", "", None)))
    assert get_double_ups(problem) == {"Tests": ["name: desc -> overall1", "name: desc -> overall2"]}


@pytest.mark.parametrize(
    "mock_sql_connect",
    (
        [
            [],
            [],
            [("name", "action1"), ("name", "action2")],
        ],
    ),
    indirect=True,
)
def test_job_double_ups(mock_sql_connect: MockSqlObject) -> None:
    problem = Problem("company", "campus", "dept", "PM123", "123")
    problem.tests.append(Test(Item("", "", "", "", "", "", "", None)))
    assert get_double_ups(problem) == {"Jobs": ["name: action1", "name: action2"]}


@pytest.mark.parametrize(
    "mock_sql_connect",
    (
        [
            [],
            [("name", "desc", "overall1"), ("name", "desc", "overall2")],
            [("name", "action1"), ("name", "action2")],
        ],
    ),
    indirect=True,
)
def test_both_double_ups(mock_sql_connect: MockSqlObject) -> None:
    problem = Problem("company", "campus", "dept", "PM123", "123")
    problem.tests.append(Test(Item("", "", "", "", "", "", "", None)))
    assert get_double_ups(problem) == {"Tests": ["name: desc -> overall1", "name: desc -> overall2"], "Jobs": ["name: action1", "name: action2"]}
