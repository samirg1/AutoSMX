from design.Script import ScriptLine


def test_script_test_creation() -> None:
    test = ScriptLine("Test Name", 1)
    assert test.number == 1
    assert test.text == "Test Name"
    assert test.default == ""
    assert test.options == ()


def test_script_test_with_options() -> None:
    test = ScriptLine("Test Name", 1, "Fail", "Pass", "N/A")
    assert test.text == "Test Name"
    assert test.default == "Fail"
    assert test.options == ("Fail", "Pass", "N/A")


def test_script_test_with_no_options() -> None:
    test = ScriptLine("Another Test", 1)
    assert str(test) == "Another Test -> ()"
    assert test.text == "Another Test"
    assert test.default == ""
    assert test.options == ()
