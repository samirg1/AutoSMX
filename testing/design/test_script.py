# pyright: reportPrivateUsage=false
import pytest

from design.data import Script, ScriptTest


def test_script_creation():
    script = Script("Nick", "Script Name", 3)
    assert script.nickname == "Nick"
    assert script.name == "Script Name"
    assert script.downs == 3
    assert len(script.tests) == 0
    assert script.search_terms == ["Nick"]


def test_script_creation_with_tests():
    test1 = ScriptTest("Test 1", "Pass", "Fail")
    test2 = ScriptTest("Test 2", "N/A", "Yes", "No")
    script = Script("Nickname", "Test Script", 2, (test1, test2))
    assert script.nickname == "Nickname"
    assert script.name == "Test Script"
    assert script.downs == 2
    assert len(script.tests) == 2
    assert script.search_terms == ["Nickname"]


def test_script_creation_with_extra_terms():
    script = Script("UniqueNick", "Unique Script", 1, search_terms=["tag1", "tag2"])
    assert script.nickname == "UniqueNick"
    assert script.name == "Unique Script"
    assert script.downs == 1
    assert len(script.tests) == 0
    assert script.search_terms == ["tag1", "tag2", "UniqueNick"]


@pytest.mark.parametrize(
    "match_description, expected",
    [
        ("Tester", True),
        ("Matching Script", False),
        ("tag3", True),
        ("NonExistent", False),
        ("Different", False),
    ],
)
def test_script_matches(match_description: str, expected: bool):
    script = Script("Tester", "Matching Script", 0, search_terms=["tag3"])
    assert script.is_for(match_description) == expected


def test_script_to_string():
    script = Script("MyNick", "Awesome Script", 5)
    assert str(script) == "Awesome Script"
