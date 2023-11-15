import pytest

from db.get_script import get_script
from design.ScriptInfo import ScriptInfo
from testing.conftest import MockSqlObject


@pytest.mark.parametrize("mock_sql_connect", ([("script_name", "type"), [(123, "line_text", 1, "type", "id")], [], []],), indirect=True)
def test_basic_get_script(mock_sql_connect: MockSqlObject) -> None:
    script = get_script(ScriptInfo(123, "123", "nickname", ["option1"], ["exact1"]), {}, set(), set(), set())

    assert script.nickname == "nickname"
    assert script.service_type == "type"
    assert script.name == "script_name"
    assert script.number == 123
    assert len(script.lines) == 1
    assert script.lines[0].text == "line_text"
    assert script.lines[0].options == ()
    assert script.search_terms == ["option1", "nickname"]
    assert script.exact_matches == ["exact1"]


@pytest.mark.parametrize(
    "mock_sql_connect",
    (
        [("script_name", "type"), [(123, "line_text", 1, "type", "id")], [("pass",), ("null",)], []],
        [("script_name", "type"), [(123, "line_text", 1, "type", "id")], [], [("pass",), ("null",)]],
    ),
    indirect=True,
)
def test_with_lines_get_script(mock_sql_connect: MockSqlObject) -> None:
    script = get_script(ScriptInfo(123, "123", "nickname", [], []), {}, set(), set(), set())

    assert script.nickname == "nickname"
    assert script.name == "script_name"
    assert script.tester_number == "123"
    assert script.number == 123
    assert len(script.lines) == 1
    assert script.lines[0].text == "line_text"
    assert script.lines[0].options == ("pass", "null")
    assert script.exact_matches == []


@pytest.mark.parametrize("mock_sql_connect", ([("script_name", "type"), [(123, "line_text", 1, "type", "id1"), (8236, "line_text", 1, None, None)], [], [], [], []],), indirect=True)
def test_8236_get_script(mock_sql_connect: MockSqlObject) -> None:
    get_script(ScriptInfo(123, "123", "nickname", [], []), {}, set(), set(), set())
    assert mock_sql_connect.calls[4][1] == ("id1",)
    assert mock_sql_connect.calls[5][1] == ("id1",)


@pytest.mark.parametrize("mock_sql_connect", ([("script_name", "type"), [(123, "line_text", 1, "type", "id1"), (124, "line_text", 1, None, None)], [], [], [], []],), indirect=True)
def test_condition_default(mock_sql_connect: MockSqlObject) -> None:
    script = get_script(ScriptInfo(123, "123", "nickname", [], []), {123: "none"}, {124}, set(), set())

    assert len(script.lines) == 2
    assert script.lines[0].default == "none"
    assert script.lines[1].default == "1"


@pytest.mark.parametrize("mock_sql_connect", ([("script_name", "type"), [(124, "line_text", 1, "header", None)], [], [], [], []],), indirect=True)
def test_header(mock_sql_connect: MockSqlObject) -> None:
    script = get_script(ScriptInfo(123, "123", "nickname", [], []), {}, set(), set(), set())
    assert len(script.lines) == 0

@pytest.mark.parametrize("mock_sql_connect", ([None],), indirect=True)
def test_valueerror(mock_sql_connect: MockSqlObject) -> None:
    with pytest.raises(ValueError):
        get_script(ScriptInfo(99999999, "123", "nickname", [], []), {}, set(), set(), set())
