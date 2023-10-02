import pytest

from db.get_items_jobs import get_items, get_jobs
from testing.conftest import MockSqlObject

job = [("company", "campus", "department", "number")]


@pytest.mark.parametrize(("job_number", "mock_sql_connect"), (["23314115", [job]], ["PM1242522", [job]]), indirect=["mock_sql_connect"])
def test_get_job(job_number: str, mock_sql_connect: MockSqlObject) -> None:
    job = get_jobs(job_number)[0]
    assert job
    assert job.company == "company"
    assert job.campus == "campus"
    assert job.department == "department"
    assert job.number == "number"
    assert job_number in mock_sql_connect.calls[0][1][0]
    assert mock_sql_connect.close_called


item = [("number", "description", "model", "manufacturer", "serial", "room", "last_update")]


@pytest.mark.parametrize("mock_sql_connect", ([item],), indirect=True)
def test_get_item(mock_sql_connect: MockSqlObject) -> None:
    item = get_items("123456")[0]
    assert item
    assert item.number == "number"
    assert item.description == "description"
    assert item.model == "model"
    assert item.manufacturer == "manufacturer"
    assert item.serial == "serial"
    assert item.room == "room"
    assert item.last_update == "last_update"
    assert "123456" in mock_sql_connect.calls[0][1][0]
    assert mock_sql_connect.close_called
