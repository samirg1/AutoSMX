import pytest

from db.presync_check import get_double_ups
from design.Item import Item
from design.Job import Job
from design.Problem import Problem
from design.Script import Script
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
    problem.tests.append(Test(Item("name", "", "desc", "", "", "", "", None)))
    problem.tests.append(Test(Item("name", "", "desc", "", "", "", "", None)))
    problem.tests[0].script = Script("nick1", "name", 1, "1", "type", (), ())
    problem.tests[1].script = Script("nick2", "name", 1, "1", "type", (), ())
    problem.tests[0].result = "overall1"
    problem.tests[1].result = "overall2"
    assert get_double_ups(problem) == {"Tests": ["name: desc (nick1) -> overall1", "name: desc (nick2) -> overall2"]}

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
def test_item_double_ups_synced(mock_sql_connect: MockSqlObject) -> None:
    problem = Problem("company", "campus", "dept", "PM123", "123")
    problem.tests.append(Test(Item("name", "", "desc", "", "", "", "", None)))
    problem.tests.append(Test(Item("name", "", "desc", "", "", "", "", None)))
    problem.tests[0].script = Script("nick1", "name", 1, "1", "type", (), ())
    problem.tests[1].script = Script("nick2", "name", 1, "1", "type", (), ())
    problem.tests[0].result = "overall1"
    problem.tests[1].result = "overall2"
    problem.tests[0].synced = True
    problem.tests[1].synced = True
    assert get_double_ups(problem) == {}

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
    problem.tests.append(Test(Item("name", "", "desc", "", "", "", "", None)))
    problem.tests[0].script = Script("nick1", "name", 1, "1", "type", (), ())
    problem.tests[0].add_job(Job("dept", "cont", "action1", []))
    problem.tests[0].add_job(Job("dept", "cont", "action2", []))

    assert get_double_ups(problem) == {"Jobs": ["name: action1", "name: action2"]}

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
def test_job_double_ups_synced(mock_sql_connect: MockSqlObject) -> None:
    problem = Problem("company", "campus", "dept", "PM123", "123")
    problem.tests.append(Test(Item("name", "", "desc", "", "", "", "", None)))
    problem.tests[0].script = Script("nick1", "name", 1, "1", "type", (), ())
    problem.tests[0].add_job(Job("dept", "cont", "action1", []))
    problem.tests[0].add_job(Job("dept", "cont", "action2", []))
    problem.tests[0].jobs[0].synced = True
    problem.tests[0].jobs[1].synced = True

    assert get_double_ups(problem) == {}

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
    problem.tests.append(Test(Item("name", "", "desc", "", "", "", "", None)))
    problem.tests.append(Test(Item("name", "", "desc", "", "", "", "", None)))
    problem.tests[0].add_job(Job("dept", "cont", "action1", []))
    problem.tests[0].add_job(Job("dept", "cont", "action2", []))
    problem.tests[0].script = Script("nick1", "name", 1, "1", "type", (), ())
    problem.tests[1].script = Script("nick2", "name", 1, "1", "type", (), ())
    problem.tests[0].result = "overall1"
    problem.tests[1].result = "overall2"
    assert get_double_ups(problem) == {"Tests": ["name: desc (nick1) -> overall1", "name: desc (nick2) -> overall2"], "Jobs": ["name: action1", "name: action2"]}
