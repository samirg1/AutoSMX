from datetime import datetime, timedelta

from db.get_connection import get_connection
from db.models import JobModel, ScriptLineModel, ScriptTesterModel, TestModel
from design.Problem import Problem
from design.Script import ScriptLine
from design.Test import Test
from utils.constants import DatabaseFilenames
from utils.get_sysmodtime import get_sysmodtime
from utils.validate_type import validate_type


def add_test(test: Test, problem: Problem) -> None:
    next_spt_date = get_sysmodtime((datetime.now() + timedelta(days=366)))

    with get_connection(DatabaseFilenames.TESTS, mode="rw") as connection, get_connection(DatabaseFilenames.ASSETS, mode="rw") as asset_connection:
        with connection, asset_connection:
            TestModel(test, problem).insert(connection)
            ScriptTesterModel(test).insert(connection)

            lines = test.script.lines
            if test.script.number == 1287:
                track_header_line = ScriptLine(text="Disclaimer: Tests carried out are subject to conditions, available on request", number=1)
                lines = (track_header_line, *lines)

            for line in lines:
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

            services = validate_type(
                list[tuple[str, float, str, str]],
                asset_connection.execute(
                    """
                    SELECT service_type, service_interval, service_last, service_next
                    FROM DEVICEA4
                    WHERE logical_name = ?;
                    """,
                    (test.item.number,),
                ).fetchall(),
            )

            servicearray = "\n".join("^".join(f"{int(s) if isinstance(s, float) else s}" for s in service) + "^" for service in services)

            connection.execute(
                """
                UPDATE devicem1_PS
                SET last_spt_date = ?, next_spt_date = ?, servicearray = ?
                WHERE logical_name = ?;
                """,
                (test.date, next_spt_date, servicearray, test.item.number),
            )
