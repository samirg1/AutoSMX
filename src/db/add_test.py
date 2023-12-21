from datetime import datetime

from db.get_connection import get_connection
from db.models import JobModel, ScriptLineModel, ScriptTesterModel, TestModel
from db.update_item_history import update_item_history
from design.Problem import Problem
from design.Test import Test
from utils.constants import DatabaseFilenames


def add_test(test: Test, problem: Problem) -> None:
    with get_connection(DatabaseFilenames.TESTS, mode="rw") as connection, get_connection(DatabaseFilenames.ASSETS, mode="rw") as asset_connection:
        with connection, asset_connection:
            TestModel(test, problem).insert(connection)
            ScriptTesterModel(test).insert(connection)

            for line in test.script.lines + test.script.header_lines:
                ScriptLineModel(test, line).insert(connection)

            for job in test.jobs:
                JobModel(test, problem, job).insert(connection)

            update_item_history(test.item, test.script.service_type, datetime.now(), connection, asset_connection)
