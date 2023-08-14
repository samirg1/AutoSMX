from design.data import SCRIPTS, Script
from design.Item import Item
from design.Test import ScriptError, Test
from design.TestJob import TestJob
import pytest

Test.__test__ = False  # type: ignore
TestJob.__test__ = False  # type: ignore


def test_test_creation_and_properties():
    item = Item("001", "Test Item", "ModelX", "ManufacturerX", "Room A", "2022-01-01", "XYZ001")
    test = Test(item)

    with pytest.raises(ScriptError):
        test.set_script()

    assert test.item == item
    assert test.script_answers == []
    assert test.testjobs == []
    assert test.comment == ""
    assert test.final_result == ""


def test_test_determine_script():
    item = Item("001", "Test Item", "ModelX", "ManufacturerX", "Room A", "2022-01-01", "XYZ001")
    test = Test(item)

    # Adding a custom script for testing
    custom_script = Script("CustomScript", "Custom Script", 2)
    SCRIPTS["CustomScript"] = custom_script

    test.set_script(custom_script)

    assert test.script == custom_script


def test_test_add_testjob():
    item = Item("001", "SLING", "ModelX", "ManufacturerX", "Room A", "2022-01-01", "XYZ001")
    test = Test(item)

    test.set_script()
    assert test.script.nickname == "SLING"

    testjob = TestJob("Quality Control", "John Doe", "Performing testing on batch 1")
    test.add_testjob(testjob)

    assert len(test.testjobs) == 1
    assert test.testjobs[0] == testjob


def test_test_complete_and_full_info():
    item = Item("001", "Test Item", "ModelX", "ManufacturerX", "Room A", "2022-01-01", "XYZ001")
    test = Test(item)

    testjob = TestJob("Quality Control", "John Doe", "Performing testing on batch 1")
    test.add_testjob(testjob)

    test.complete("Test completed successfully.", "Pass", ["", "No"])

    full_info = test.full_info()
    assert str(test) in full_info


def test_test_item_model_property():
    item = Item("001", "Test Item", "ModelX", "ManufacturerX", "Room A", "2022-01-01", "XYZ001")
    test = Test(item)
    test.script = Script("CustomScript", "Custom Script", 2)

    assert test.item_model == "Custom Script -> ModelX"


# Run the tests
test_test_creation_and_properties()
test_test_determine_script()
test_test_add_testjob()
test_test_complete_and_full_info()
test_test_item_model_property()
