import sqlite3
from typing import Any

import pytest


class MockSqlObject:
    class MockFetchedObject:
        def __init__(self, return_value: Any) -> None:
            self.return_value = return_value

        def fetchone(self) -> Any:
            return self.return_value

        def fetchall(self) -> Any:
            return self.fetchone()

    def __init__(self, return_values: list[Any], constant: bool) -> None:
        self.constant = constant
        self.current = 0
        self.return_values = return_values
        self.close_called = False
        self.calls: list[tuple[str, list[Any]]] = []

    def execute(self, sql: str, params: list[Any]) -> Any:
        self.calls.append((sql, params))
        if self.constant:
            value = self.MockFetchedObject(self.return_values[self.current])
            self.current = (self.current + 1) % len(self.return_values)
            return value
        return self.MockFetchedObject(self.return_values.pop())

    def executemany(self, sql: str, params: list[Any]) -> Any:
        return self.execute(sql, params)

    def close(self) -> None:
        self.close_called = True


def base(monkeypatch: pytest.MonkeyPatch, values: list[Any], constant: bool = False) -> MockSqlObject:
    obj = MockSqlObject(values, constant)

    def mock_connect(path: str, *, uri: bool) -> MockSqlObject:
        return obj

    monkeypatch.setattr(sqlite3, "connect", mock_connect)

    return obj


@pytest.fixture
def mock_sql_connect(monkeypatch: pytest.MonkeyPatch, request: pytest.FixtureRequest) -> MockSqlObject:
    return_values: list[Any] = []
    if isinstance(request.param, list):
        return_values = request.param[::-1]
    return base(monkeypatch, return_values)


@pytest.fixture
def mock_sql_connect_scripts(monkeypatch: pytest.MonkeyPatch) -> MockSqlObject:
    return_values: list[Any] = [("script_name",), []]
    return base(monkeypatch, return_values, constant=True)
