import pytest

from db.get_script import get_script
from design.ScriptInfo import ScriptInfo
from testing.conftest import MockSqlObject


@pytest.mark.parametrize("mock_sql_connect", (
        [("script_name",), [(123, "line_text", "type", "id")], [], []],
), indirect=True)
def test_basic_get_script(mock_sql_connect: MockSqlObject) -> None:
    script = get_script(ScriptInfo(123, "nickname", ["option1"], ["exact1"]), {}, set())

    assert script.nickname == "nickname"
    assert script.name == "script_name"
    assert script.number == 123
    assert len(script.lines) == 1
    assert script.lines[0].name == "line_text"
    assert script.lines[0].options == ()
    assert script.search_terms == ["option1", "nickname"]
    assert script.exact_matches == ["exact1"]


@pytest.mark.parametrize("mock_sql_connect", (
        [("script_name",), [(123, "line_text", "type", "id")], [("pass",),("null",)], []],
        [("script_name",), [(123, "line_text", "type", "id")], [], [("pass",),("null",)]],
), indirect=True)
def test_with_lines_get_script(mock_sql_connect: MockSqlObject) -> None:
    script = get_script(ScriptInfo(123, "nickname", [], []), {}, set())

    assert script.nickname == "nickname"
    assert script.name == "script_name"
    assert script.number == 123
    assert len(script.lines) == 1
    assert script.lines[0].name == "line_text"
    assert script.lines[0].options == ('pass', 'null')
    assert script.exact_matches == []


@pytest.mark.parametrize("mock_sql_connect", (
        [("script_name",), [(123, "line_text", "type", "id1"), (8236, "line_text", None, None)], [], [], [], []],
), indirect=True)
def test_8236_get_script(mock_sql_connect: MockSqlObject) -> None:
    get_script(ScriptInfo(123, "nickname", [], []), {}, set())
    assert mock_sql_connect.calls[4][1] == ("id1",)
    assert mock_sql_connect.calls[5][1] == ("id1",)


@pytest.mark.parametrize("mock_sql_connect", (
        [("script_name",), [(123, "line_text", "type", "id1"), (124, "line_text", None, None)], [], [], [], []],
), indirect=True)
def test_condition_default(mock_sql_connect: MockSqlObject) -> None:
    script = get_script(ScriptInfo(123, "nickname", [], []), {123: "none"}, {124})

    assert len(script.lines) == 2
    assert script.lines[0].selected == "none"
    assert script.lines[1].selected == "1"


@pytest.mark.parametrize("mock_sql_connect", (
        [("script_name",), [(124, "line_text", "header", None)], [], [], [], []],
), indirect=True)
def test_header(mock_sql_connect: MockSqlObject) -> None:
    script = get_script(ScriptInfo(123, "nickname", [], []), {}, set())
    assert len(script.lines) == 0
