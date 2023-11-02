import pytest

from db.edit_test import edit_test
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
            None,  # deletions
            None,
            None,
            None,
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
def test_edit_test(mock_sql_connect: MockSqlObject, mock_config_parse: MockConfigObject) -> None:
    test = Test(Item("1", "1A", "d", "m", "manu", "s", "r", None))
    line = ScriptLine("Test 1", 1, "Pass", "Fail")
    test.script = Script("CustomScript", "Custom Script", 1287, "999", "type", (line,))
    test.add_job(Job("dept", "contact", "comment"))
    test.complete("comments", "result", [])
    problem = Problem("comp", "camp", "dept", "PM123", "customer_no", get_open_problems=False)

    edit_test(test, problem)

    calls = mock_sql_connect.calls
    assert len(calls) == 14

    for i, table in enumerate(["SCMobileTestsm1", "SCMobileTesterNumbersm1", "SCMobileTestLinesm1", "SCMProbsUploadm1"]):
        sql, params = calls[i + 2]
        assert sql.startswith(f"DELETE FROM {table} WHERE test_id")
        assert params == ("SMX0000000021",)


@pytest.mark.parametrize("mock_sql_connect", ([("None", 20, 30), [], None, None, None, None],), indirect=True)  # get test id  # get open problems  # deletions
def test_edit_remove_only(mock_sql_connect: MockSqlObject, mock_config_parse: MockConfigObject) -> None:
    test = Test(Item("1", "1A", "d", "m", "manu", "s", "r", None))
    line = ScriptLine("Test 1", 1, "Pass", "Fail")
    test.script = Script("CustomScript", "Custom Script", 1287, "999", "type", (line,))
    test.add_job(Job("dept", "contact", "comment"))
    test.complete("comments", "result", [])
    problem = Problem("comp", "camp", "dept", "PM123", "customer_no", get_open_problems=False)

    edit_test(test, problem, remove_only=True)

    calls = mock_sql_connect.calls
    assert len(calls) == 6

    for i, table in enumerate(["SCMobileTestsm1", "SCMobileTesterNumbersm1", "SCMobileTestLinesm1", "SCMProbsUploadm1"]):
        sql, params = calls[i + 2]
        assert sql.startswith(f"DELETE FROM {table} WHERE test_id")
        assert params == ("SMX0000000021",)
