from db.set_favourites import set_favourites
from design.data import get_all_scripts, SCRIPT_DOWNS
from testing.conftest import MockSqlObject


def test_set_favourites(mock_sql_connect_scripts: MockSqlObject) -> None:
    get_all_scripts()
    set_favourites()

    sql, params = mock_sql_connect_scripts.calls[-1]
    assert "INSERT INTO" in sql
    assert len(params) == len(SCRIPT_DOWNS)

    sql, params = mock_sql_connect_scripts.calls[-2]
    assert sql == "DELETE FROM ScriptFavourites;"
    assert len(params) == 0
