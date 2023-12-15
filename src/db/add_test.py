from datetime import datetime, timedelta

from typeguard import TypeCheckError, check_type

from db.get_connection import get_connection
from db.models import JobModel, ScriptLineModel, ScriptTesterModel, TestModel
from design.Problem import Problem
from design.Test import Test
from utils.constants import DatabaseFilenames
from utils.get_sysmodtime import get_sysmodtime


def add_test(test: Test, problem: Problem) -> None:
    next_spt_date = get_sysmodtime((datetime.now() + timedelta(days=366)))

    with get_connection(DatabaseFilenames.TESTS, mode="rw") as connection, get_connection(DatabaseFilenames.ASSETS, mode="rw") as asset_connection:
        with connection, asset_connection:
            TestModel(test, problem).insert(connection)
            ScriptTesterModel(test).insert(connection)

            for line in test.script.lines + test.script.header_lines:
                ScriptLineModel(test, line).insert(connection)

            for job in test.jobs:
                JobModel(test, problem, job).insert(connection)

            asset_connection.execute(
                """
                UPDATE DEVICEA4
                SET service_last = ?, service_next = ?
                WHERE logical_name = ? AND service_type = ?;
                """,
                (test.date, next_spt_date, test.item.number, test.script.service_type),
            )

            services = asset_connection.execute(
                """
                SELECT service_type, service_interval, service_last, service_next
                FROM DEVICEA4
                WHERE logical_name = ?;
                """,
                (test.item.number,),
            ).fetchall()

            try:
                services = check_type(services, list[tuple[str, float, str, str]])
            except TypeCheckError:
                services = []
                
            servicearray = "\n".join("^".join(f"{int(s) if isinstance(s, float) else s}" for s in service) + "^" for service in services)

            connection.execute(
                """
                UPDATE devicem1_PS
                SET last_spt_date = ?, next_spt_date = ?, servicearray = ?
                WHERE logical_name = ?;
                """,
                (test.date, next_spt_date, servicearray, test.item.number),
            )
