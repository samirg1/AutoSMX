import pytest

from design.data import get_all_scripts
from design.Item import Item
from design.Job import Job
from design.Script import Script, ScriptLine
from design.Test import InvalidTestResultError, ScriptError, Test
from testing.conftest import MockConfigObject, MockSqlObject

Test.__test__ = False  # type: ignore


def test_test_creation_and_properties() -> None:
    item = Item("001", "001", "Test Item", "ModelX", "ManufacturerX", "XYZ001", "RM1", "2019-01-01 03:45:44.759")
    test = Test(item)

    with pytest.raises(ScriptError):
        test.determine_script()

    assert test.item == item
    assert test.jobs == []
    assert test.comments == ""
    assert test.result == ""

    assert repr(test) == "Test({'item': 001 - Test Item, 'jobs': [], 'comments': '', 'result': '', 'id': '', 'user': '', 'date': '', 'completed': False, 'synced': False})"


def test_test_determine_script(mock_sql_connect_scripts: MockSqlObject) -> None:
    item = Item("001", "001", "Test Item", "ModelX", "ManufacturerX", "XYZ001", "RM1", "2019-01-01 03:45:44.759")
    test = Test(item)

    # Adding a custom script for testing
    custom_script = Script("CustomScript", "Custom Script", 1, "999", "type", (), ())
    get_all_scripts()["CustomScript"] = custom_script

    test.script = custom_script

    assert test.script == custom_script
    del get_all_scripts()["CustomScript"]
    assert test.item_model == "Custom Script -> ModelX"


def test_test_add_testjob(mock_sql_connect_scripts: MockSqlObject) -> None:
    item = Item("001", "001", "SLING 123", "ModelX", "ManufacturerX", "XYZ001", "RM1", "2019-01-01 03:45:44.759")
    test = Test(item)

    custom_script = Script("SLING", "Custom Script", 1, "999", "type", (), ())
    get_all_scripts()["SLING"] = custom_script
    test.script = test.determine_script()
    assert test.script.nickname == "SLING"

    job = Job("Quality Control", "John Doe", "Performing testing on batch 1", [])
    test.add_job(job)

    assert len(test.jobs) == 1
    assert test.jobs[0] == job


def test_test_complete_and_full_info(mock_sql_connect_scripts: MockSqlObject) -> None:
    item = Item("001", "001", "Test Item", "ModelX", "ManufacturerX", "XYZ001", "RM1", "2019-01-01 03:45:44.759")
    test = Test(item)

    custom = Script("CustomScript", "Custom Script", 1, "999", "type", (), (), exact_matches=["Test Item"])
    get_all_scripts()["CustomScript"] = custom
    test.script = test.determine_script()
    assert test.script.nickname == "CustomScript"
    del get_all_scripts()["CustomScript"]


@pytest.mark.parametrize("mock_sql_connect", ([(20, 30), None],), indirect=True)
def test_test_complete(mock_sql_connect: MockSqlObject, mock_config_parse: MockConfigObject) -> None:
    item = Item("001", "001", "Test Item", "ModelX", "ManufacturerX", "XYZ001", "RM1", "2019-01-01 03:45:44.759")
    test = Test(item)
    line = ScriptLine("Test 1", 1, 1, "Pass", "Fail")
    test.script = Script("CustomScript", "Custom Script", 1, "999", "type", (line,), (), exact_matches=["Test Item"])
    test.complete("comment", "result", ["Pass"])

    assert test.comments == "comment"
    assert test.result == "result"
    assert test.completed
    assert test.user == "test user"
    assert test.id == "SMX0000000021"
    assert test.script.lines[0].result == "Pass"

    test2 = Test(item)
    test2.id = "SMX0000000021"
    assert test2 == test
    assert test != "SMX0000000021"


def test_test_item_model_property() -> None:
    item = Item("001", "001", "Test Item", "ModelX", "ManufacturerX", "XYZ001", "RM1", "2019-01-01 03:45:44.759")
    test = Test(item)
    test.script = Script("CustomScript", "Custom Script", 1, "999", "type", (), ())

    assert test.item_model == "Custom Script -> ModelX"

@pytest.mark.parametrize(("result", "add_job", "comment", "script_answers"), [
    ("", False, "", []),
    ("Pass A/R", True, "", []),
    ("Pass", True, "comment", []),
    ("Fail", False, "", ["Fail"]),
    ("Pass", False, "comment", ["Fail"]),
    ("Passed A/R", False, "comment", ["Fail"]),
    ("Pass", False, "", [""]),
    ("Pass", False, "", [" "]),

])
def test_invalids(result: str, add_job: bool, comment: str, script_answers: list[str]) -> None:
    item = Item("001", "001", "Test Item", "ModelX", "ManufacturerX", "XYZ001", "RM1", "2019-01-01 03:45:44.759")
    test = Test(item)
    line = ScriptLine("Test 1", 1, 1, "Pass", "Fail")
    line.required = True
    test.script = Script("CustomScript", "Custom Script", 1, "999", "type", (line,), (), exact_matches=["Test Item"])

    if add_job:
        job = Job("Quality Control", "John Doe", "Performing testing on batch 1", [])
        test.add_job(job)

    with pytest.raises(InvalidTestResultError):
        test.complete(comment, result, script_answers)
