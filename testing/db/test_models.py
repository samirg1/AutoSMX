import pytest
from db.get_connection import get_connection
from db.models import TestModel, ScriptLineModel, ScriptTesterModel, JobModel
from design.Item import Item
from design.Job import Job
from design.Problem import Problem
from design.Script import Script
from design.ScriptLine import ScriptLine
from design.Test import Test
from testing.conftest import MockConfigObject, MockSqlObject
from utils.constants import DatabaseFilenames

TestModel.__test__ = False  # type: ignore
Test.__test__ = False  # type: ignore


@pytest.mark.parametrize("mock_sql_connect", ([(20, 30), None, None],), indirect=True)
def test_test_model(mock_sql_connect: MockSqlObject, mock_config_parse: MockConfigObject) -> None:
    test = Test(Item("1", "1A", "d", "m", "manu", "s", "r", None))
    test.script = Script("CustomScript", "Custom Script", 1, "999", "type", (), ())
    test.complete("", "Pass", [])
    problem = Problem("", "", "", "", "", get_open_problems=False)

    model = TestModel(test, problem)

    assert model.table_name == "SCMobileTestsm1"
    assert model.__dict__ == {
        "test_id": test.id,
        "logical_name": test.item.number,
        "customer_barcode": test.item.customer_barcode,
        "test_date": test.date,
        "sysmoduser": test.user,
        "problem_number": problem.number,
        "user_name": test.user,
        "comments": test.comments,
        "customer_id": problem.customer_number,
        "company_name": problem.company,
        "location": problem.campus,
        "dept": problem.department,
        "pointsync_id": None,
        "overall": test.result,
        "building": "",
        "floor": "",
        "room": test.item.room,
        "model": test.item.model,
        "manufacturer": test.item.manufacturer,
        "description": test.item.description,
        "serial_no_": test.item.serial,
        "pointsync_time": None,
        "sysmodtime": test.date,
        "interfaced": None,
    }

    with get_connection(DatabaseFilenames.ASSETS) as connection:
        model.insert(connection)

    assert "INSERT" in mock_sql_connect.calls[-1][0]
    assert model.table_name in mock_sql_connect.calls[-1][0]


@pytest.mark.parametrize("mock_sql_connect", ([(20, 30), None, None],), indirect=True)
def test_script_tester_model(mock_sql_connect: MockSqlObject, mock_config_parse: MockConfigObject) -> None:
    test = Test(Item("1", "1A", "d", "m", "manu", "s", "r", None))
    test.script = Script("CustomScript", "Custom Script", 1, "999", "type", (), ())
    test.complete("", "Pass", [])

    model = ScriptTesterModel(test)

    assert model.table_name == "SCMobileTesterNumbersm1"
    assert model.__dict__ == {
        "test_id": test.id,
        "script_number": test.script.number,
        "tester_number": test.script.tester_number,
    }

    with get_connection(DatabaseFilenames.ASSETS) as connection:
        model.insert(connection)

    assert "INSERT" in mock_sql_connect.calls[-1][0]
    assert model.table_name in mock_sql_connect.calls[-1][0]


@pytest.mark.parametrize("mock_sql_connect", ([(20, 30), None, None],), indirect=True)
def test_script_line_model(mock_sql_connect: MockSqlObject, mock_config_parse: MockConfigObject) -> None:
    test = Test(Item("1", "1A", "d", "m", "manu", "s", "r", None))
    test.script = Script("CustomScript", "Custom Script", 1, "999", "type", (), ())
    test.complete("", "Pass", [])
    line = ScriptLine("Test 1", 1, 1, "Pass", "Fail")

    model = ScriptLineModel(test, line)

    assert model.table_name == "SCMobileTestLinesm1"
    assert model.__dict__ == {
        "test_id": test.id,
        "script_number": test.script.number,
        "script_line": line.number,
        "result": line.result,
        "comments": None,
        "date_performed": None,
        "performed_by": test.user,
        "script_line_text": line.text,
        "set_point": 200 if (test.script.number == 1287 and line.number == 5) else None,
        "page": None,
        "orderprgn": None,
    }

    with get_connection(DatabaseFilenames.ASSETS) as connection:
        model.insert(connection)

    assert "INSERT" in mock_sql_connect.calls[-1][0]
    assert model.table_name in mock_sql_connect.calls[-1][0]


@pytest.mark.parametrize("mock_sql_connect", ([(20, 30), None, None],), indirect=True)
def test_job_model(mock_sql_connect: MockSqlObject, mock_config_parse: MockConfigObject) -> None:
    test = Test(Item("1", "1A", "d", "m", "manu", "s", "r", None))
    test.script = Script("CustomScript", "Custom Script", 1, "999", "type", (), ())
    test.complete("", "Pass", [])
    problem = Problem("", "", "", "", "", get_open_problems=False)
    job = Job("dept", "contact", "comment", [])

    model = JobModel(test, problem, job)

    assert model.table_name == "SCMProbsUploadm1"
    assert len(model.pointsync_id) == 38
    assert model.pointsync_id[0] == "{"
    assert model.pointsync_id[-1] == "}"
    model.pointsync_id = ""
    assert model.__dict__ == {
        "pointsync_id": "",
        "customer_no_": problem.customer_number,
        "location": problem.campus,
        "building": None,
        "floor": None,
        "room": test.item.room,
        "category": None,
        "subcategory": None,
        "logical_name": test.item.number,
        "customer_barcode": test.item.customer_barcode,
        "actionprgn": job.comment,
        "assignment": None,
        "dept": job.department,
        "contact_name": job.contact_name,
        "contact_phone": None,
        "contact_email": None,
        "assignee_name": test.user,
        "asset_description": test.item.description,
        "opened_by": test.user,
        "link_to_problem": problem.number,
        "test_id": test.id,
    }

    with get_connection(DatabaseFilenames.ASSETS) as connection:
        model.insert(connection)

    assert "INSERT" in mock_sql_connect.calls[-1][0]
    assert model.table_name in mock_sql_connect.calls[-1][0]
