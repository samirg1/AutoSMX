import pytest

from design.data import SCRIPTS
from design.Item import Item
from design.Script import Script
from design.Test import ScriptError, Test
from design.TestJob import TestJob

Test.__test__ = False  # type: ignore
TestJob.__test__ = False  # type: ignore


def test_test_creation_and_properties():
    item = Item("001", "Test Item", "ModelX", "ManufacturerX", "XYZ001", "RM1", "2019")
    test = Test(item)

    with pytest.raises(ScriptError):
        test.determine_script()

    assert test.item == item
    assert test.script_answers == []
    assert test.testjobs == []
    assert test.comment == ""
    assert test.final_result == ""


def test_test_determine_script():
    item = Item("001", "Test Item", "ModelX", "ManufacturerX", "XYZ001", "RM1", "2019")
    test = Test(item)

    # Adding a custom script for testing
    custom_script = Script("CustomScript", "Custom Script")
    SCRIPTS["CustomScript"] = custom_script

    test.script = custom_script

    assert test.script == custom_script
    del SCRIPTS["CustomScript"]
    assert test.item_model == "Custom Script -> ModelX"


def test_test_add_testjob():
    item = Item("001", "SLING 123", "ModelX", "ManufacturerX", "XYZ001", "RM1", "2019")
    test = Test(item)

    test.script = test.determine_script()
    assert test.script.nickname == "SLING"

    testjob = TestJob("Quality Control", "John Doe", "Performing testing on batch 1")
    test.add_testjob(testjob)

    assert len(test.testjobs) == 1
    assert test.testjobs[0] == testjob


def test_test_complete_and_full_info():
    item = Item("001", "Test Item", "ModelX", "ManufacturerX", "XYZ001", "RM1", "2019")
    test = Test(item)

    custom = Script("CustomScript", "Custom Script", (), exact_matches=["Test Item"])
    SCRIPTS["CustomScript"] = custom
    test.script = test.determine_script()
    assert test.script.nickname == "CustomScript"
    del SCRIPTS["CustomScript"]

    testjob = TestJob("Quality Control", "John Doe", "Performing testing on batch 1")
    test.add_testjob(testjob)

    test.complete("Test completed successfully.", "Pass", ["", "No"])
    assert test.comment == "Test completed successfully."
    assert test.final_result == "Pass"
    assert test.script_answers == ["N/A", "No"]
    assert str(test) == "001 - Test Item - Pass"


def test_test_item_model_property():
    item = Item("001", "Test Item", "ModelX", "ManufacturerX", "XYZ001", "RM1", "2019")
    test = Test(item)
    test.script = Script("CustomScript", "Custom Script")

    assert test.item_model == "Custom Script -> ModelX"
