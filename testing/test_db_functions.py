import sqlite3

import pytest

from gui.db_functions import get_items, get_jobs


class JobMock:
    def fetchall(self) -> list[tuple[str, ...]]:
        return [("company", "location", "dept", "number")]


class ItemMock:
    def fetchall(self) -> list[tuple[str, ...]]:
        return [("number", "description", "model", "manufacturer", "serial", "room", "last_update")]


class sql_job:
    def __init__(self) -> None:
        self.called_with: list[str] = []
        self.close_called = False

    def execute(self, _: str, number: tuple[str]) -> JobMock:
        self.called_with.append(number[0])

        return JobMock()

    def close(self) -> None:
        self.close_called = True


class sql_item:
    def __init__(self) -> None:
        self.called_with: list[str] = []
        self.close_called = False

    def execute(self, _: str, number: tuple[str]) -> ItemMock:
        self.called_with.append(number[0])

        return ItemMock()

    def close(self) -> None:
        self.close_called = True


@pytest.fixture
def mock_sql_job(monkeypatch: pytest.MonkeyPatch) -> sql_job:
    obj = sql_job()

    def mock_connect(_: str) -> sql_job:
        return obj

    monkeypatch.setattr(sqlite3, "connect", mock_connect)

    return obj


@pytest.fixture
def mock_sql_item(monkeypatch: pytest.MonkeyPatch) -> sql_item:
    obj = sql_item()

    def mock_connect(_: str) -> sql_item:
        return obj

    monkeypatch.setattr(sqlite3, "connect", mock_connect)

    return obj


@pytest.mark.parametrize("job_number", ("23314115", "PM1242522"))
def test_get_job(job_number: str, mock_sql_job: sql_job) -> None:
    job = get_jobs(job_number)[0]
    assert job
    assert job.campus == "location"
    assert job.department == "dept"
    assert job.number == "number"
    assert job.company == "company"
    assert job_number in mock_sql_job.called_with[0]
    assert mock_sql_job.close_called


def test_get_item(mock_sql_item: sql_job) -> None:
    item = get_items("123456")[0]
    assert item
    assert item.description == "description"
    assert item.number == "number"
    assert item.last_update == "last_update"
    assert item.manufacturer == "manufacturer"
    assert item.model == "model"
    assert item.serial == "serial"
    assert item.room == "room"
    assert "123456" in mock_sql_item.called_with[0]
    assert mock_sql_item.close_called
