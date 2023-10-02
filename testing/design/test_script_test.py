from design.Script import ScriptLine

def test_script_test_creation() -> None:
    test = ScriptLine("Test Name")
    assert test.name == "Test Name"
    assert test.selected == ""
    assert test.options == ()


def test_script_test_with_options() -> None:
    test = ScriptLine("Test Name", "Fail", "Pass", "N/A")
    assert test.name == "Test Name"
    assert test.selected == "Fail"
    assert test.options == ("Fail", "Pass", "N/A")


def test_script_test_with_no_options() -> None:
    test = ScriptLine("Another Test")
    assert str(test) == "Another Test -> ()"
    assert test.name == "Another Test"
    assert test.selected == ""
    assert test.options == ()
