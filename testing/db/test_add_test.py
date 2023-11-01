import pytest

from db.add_test import add_test
from design.Item import Item
from design.Job import Job
from design.Problem import Problem
from design.Script import Script, ScriptLine
from design.Test import Test
from testing.conftest import MockConfigObject, MockSqlObject

Test.__test__ = False  # type: ignore


@pytest.mark.parametrize(
    "mock_sql_connect",
    (
        [
            ("None", 20, 30),  # get test id
            [],  # get open problems
            None,  # insert test
            None,  # insert script-tester
            None,  # insert header line
            None,  # insert regular line
            None,  # insert job
            None,  # update item services
            [("EPP", 12.0, "last1", "next1"), ("SPT", 6.0, "last2", "next2")],  # get item services
            None,  # update item
        ],
    ),
    indirect=True,
)
def test_add_test(mock_sql_connect: MockSqlObject, mock_config_parse: MockConfigObject) -> None:
    test = Test(Item("1", "1A", "d", "m", "manu", "s", "r", None))
    line = ScriptLine("Test 1", 1, "Pass", "Fail")
    test.script = Script("CustomScript", "Custom Script", 1287, "999", "type", (line,))
    test.add_job(Job("dept", "contact", "comment"))
    test.complete("comments", "result", [])
    problem = Problem("comp", "camp", "dept", "PM123", "customer_no", get_open_problems=False)

    add_test(test, problem)

    calls = mock_sql_connect.calls
    assert len(calls) == 10

    sql, params = calls[-3]
    assert "UPDATE DEVICEA4" in sql
    assert params[0] == test.date
    assert params[2] == "1"
    assert params[3] == "type"

    sql, params = calls[-2]
    assert sql.count(",") == 3
    assert "FROM DEVICEA4" in sql
    assert params == ("1",)

    sql, params = calls[-1]
    assert "UPDATE devicem1_PS" in sql
    assert params[0] == test.date
    assert params[2] == "EPP^12^last1^next1^\nSPT^6^last2^next2^"
    assert params[3] == "1"
