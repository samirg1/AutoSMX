from design.Script import ScriptLine


def test_script_test_creation() -> None:
    test = ScriptLine("Test Name")
    assert test.name == "Test Name"
    assert test.selected == ""
    assert test.options == []


def test_script_test_with_options() -> None:
    test = ScriptLine("Test Name", "Fail", "Pass", "N/A")
    assert test.name == "Test Name"
    assert test.selected == "Fail"
    assert test.options == ["Pass", "N/A", "Fail"]


def test_script_test_with_no_options() -> None:
    test = ScriptLine("Another Test")
    assert test.name == "Another Test"
    assert test.selected == ""
    assert test.options == []


def test_script_test_sorting() -> None:
    test = ScriptLine("Sorting Test", "1", "Pass", "0", "N/A", " ")
    assert test.name == "Sorting Test"
    assert test.selected == "1"
    assert test.options == ["Pass", "N/A", "1", "0", " "]
