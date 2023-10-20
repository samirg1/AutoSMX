import pytest

from design.data import get_all_scripts
from design.Item import Item
from design.Job import Job
from design.Script import Script
from design.Test import ScriptError, Test
from testing.conftest import MockSqlObject

Test.__test__ = False  # type: ignore
Job.__test__ = False  # type: ignore


def test_test_creation_and_properties() -> None:
    item = Item("001", "Test Item", "ModelX", "ManufacturerX", "XYZ001", "RM1", "2019-01-01 03:45:44.759")
    test = Test(item)

    with pytest.raises(ScriptError):
        test.determine_script()

    assert test.item == item
    assert test.script_answers == []
    assert test.jobs == []
    assert test.comments == ""
    assert test.result == ""


def test_test_determine_script(mock_sql_connect_scripts: MockSqlObject) -> None:
    item = Item("001", "Test Item", "ModelX", "ManufacturerX", "XYZ001", "RM1", "2019-01-01 03:45:44.759")
    test = Test(item)

    # Adding a custom script for testing
    custom_script = Script("CustomScript", "Custom Script", 1)
    get_all_scripts()["CustomScript"] = custom_script

    test.script = custom_script

    assert test.script == custom_script
    del get_all_scripts()["CustomScript"]
    assert test.item_model == "Custom Script -> ModelX"


def test_test_add_testjob(mock_sql_connect_scripts: MockSqlObject) -> None:
    item = Item("001", "SLING 123", "ModelX", "ManufacturerX", "XYZ001", "RM1", "2019-01-01 03:45:44.759")
    test = Test(item)

    custom_script = Script("SLING", "Custom Script", 1)
    get_all_scripts()["SLING"] = custom_script
    test.script = test.determine_script()
    assert test.script.nickname == "SLING"

    job = Job("Quality Control", "John Doe", "Performing testing on batch 1")
    test.add_job(job)

    assert len(test.jobs) == 1
    assert test.jobs[0] == job


def test_test_complete_and_full_info(mock_sql_connect_scripts: MockSqlObject) -> None:
    item = Item("001", "Test Item", "ModelX", "ManufacturerX", "XYZ001", "RM1", "2019-01-01 03:45:44.759")
    test = Test(item)

    custom = Script("CustomScript", "Custom Script", 1, (), exact_matches=["Test Item"])
    get_all_scripts()["CustomScript"] = custom
    test.script = test.determine_script()
    assert test.script.nickname == "CustomScript"
    del get_all_scripts()["CustomScript"]

    job = Job("Quality Control", "John Doe", "Performing testing on batch 1")
    test.add_job(job)

    test.complete("Test completed successfully.", "Pass", ["", "No"])
    assert test.comments == "Test completed successfully."
    assert test.result == "Pass"
    assert test.script_answers == ["N/A", "No"]
    assert str(test) == "001 - Test Item - Pass"


def test_test_item_model_property() -> None:
    item = Item("001", "Test Item", "ModelX", "ManufacturerX", "XYZ001", "RM1", "2019-01-01 03:45:44.759")
    test = Test(item)
    test.script = Script("CustomScript", "Custom Script", 1)

    assert test.item_model == "Custom Script -> ModelX"
