import configparser
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
        self.empty = not bool(return_values)
        self.current = 0
        self.return_values = return_values
        self.close_called = False
        self.calls: list[tuple[str, tuple[Any, ...]]] = []

    def execute(self, sql: str, params: tuple[Any, ...] | None = None) -> Any:
        params = params or ()
        self.calls.append((sql, params))
        if self.constant:
            value = self.MockFetchedObject(self.return_values[self.current])
            self.current = (self.current + 1) % len(self.return_values)
            return value
        elif self.empty:
            return self.MockFetchedObject(None)
        return self.MockFetchedObject(self.return_values.pop())

    def executemany(self, sql: str, params: tuple[Any, ...]) -> Any:
        return self.execute(sql, params)

    def close(self) -> None:
        self.close_called = True

    def __enter__(self) -> None:
        return

    def __exit__(self, *_: Any) -> None:
        return


def base(monkeypatch: pytest.MonkeyPatch, values: list[Any], constant: bool = False) -> MockSqlObject:
    obj = MockSqlObject(values, constant)

    def mock_connect(path: str, *, uri: bool) -> MockSqlObject:
        return obj

    monkeypatch.setattr(sqlite3, "connect", mock_connect)

    return obj


@pytest.fixture
def mock_sql_connect(monkeypatch: pytest.MonkeyPatch, request: pytest.FixtureRequest) -> MockSqlObject:
    return_values: list[Any] = []
    try:
        if isinstance(request.param, list):
            return_values = request.param[::-1]
    except AttributeError:
        pass
    return base(monkeypatch, return_values)


@pytest.fixture
def mock_sql_connect_scripts(monkeypatch: pytest.MonkeyPatch) -> MockSqlObject:
    return_values: list[Any] = [("script_name", "type"), []]
    return base(monkeypatch, return_values, constant=True)


class MockConfigObject:
    def __init__(self) -> None:
        self.read_calls: list[str] = []
        self.get_calls: list[tuple[str, str]] = []

    def read(self, s: str) -> None:
        self.read_calls.append(s)

    def get(self, s1: str, s2: str) -> str:
        self.get_calls.append((s1, s2))
        return "test user"


@pytest.fixture
def mock_config_parse(monkeypatch: pytest.MonkeyPatch) -> MockConfigObject:
    obj = MockConfigObject()

    def mock_config() -> MockConfigObject:
        return obj

    monkeypatch.setattr(configparser, "ConfigParser", mock_config)

    return obj
