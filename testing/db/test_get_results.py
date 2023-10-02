import pytest

from db.get_overall_results import get_overall_results
from testing.conftest import MockSqlObject


@pytest.mark.parametrize("mock_sql_connect", ([[("Pass", "Passed")]],), indirect=True)
def test_get_results(mock_sql_connect: MockSqlObject) -> None:
    results = get_overall_results(123)

    assert len(results) == 1
    assert results[0] == ("Pass", "Passed")

    args = mock_sql_connect.calls[0][1]
    assert len(args) == 2
    assert args[0] == 123
    assert "123" in args[1]
