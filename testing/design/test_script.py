import pytest

from design.Script import Script, ScriptLine


def test_script_creation() -> None:
    script = Script("Nick", "Script Name", 1)
    assert script.nickname == "Nick"
    assert script.name == "Script Name"
    assert script.number == 1
    assert len(script.lines) == 0
    assert script.search_terms == ["Nick"]


def test_script_creation_with_tests() -> None:
    test1 = ScriptLine("Test 1", "Pass", "Fail")
    test2 = ScriptLine("Test 2", "N/A", "Yes", "No")
    script = Script("Nickname", "Test Script", 1, (test1, test2))
    assert script.nickname == "Nickname"
    assert script.name == "Test Script"
    assert len(script.lines) == 2
    assert script.search_terms == ["Nickname"]


def test_script_creation_with_extra_terms() -> None:
    script = Script("UniqueNick", "Unique Script", 1, search_terms=["tag1", "tag2"])
    assert script.nickname == "UniqueNick"
    assert script.name == "Unique Script"
    assert len(script.lines) == 0
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
def test_script_matches(match_description: str, expected: bool) -> None:
    script = Script("Tester", "Matching Script", 1, search_terms=["tag3"])
    assert script.is_for(match_description) == expected


def test_script_to_string() -> None:
    script = Script("MyNick", "Awesome Script", 1)
    assert str(script) == "Awesome Script"


def test_hash_and_eq() -> None:
    script1 = Script("Nick1", "Script 1", 1)
    script2 = Script("Nick2", "Script 2", 1)
    script3 = Script("Nick3", "Script 1", 1)
    assert len({script1, script2}) == 2
    assert len({script1, script3}) == 1
    assert hash(script1) != hash(script2)
    assert hash(script1) == hash(script3)
