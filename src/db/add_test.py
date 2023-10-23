from datetime import datetime, timedelta

from db.get_connection import DatabaseFilenames, get_connection
from db.get_user import get_user
from db.models import ScriptLineModel, ScriptTesterModel, TestModel, JobModel
from design.Problem import Problem
from design.Test import Test
from design.Script import ScriptLine


class NoTestIDsError(RuntimeError):
    ...


def _get_new_test_id() -> str:
    with get_connection(DatabaseFilenames.SETTINGS, mode="rw") as connection:
        res: tuple[str, int, int] | None = connection.execute(
            """
            SELECT TABLENAME, LASTUSED, LASTRESERVED
            FROM SCMIDTABLE
            WHERE TABLENAME == 'SCMobileTestsm1' AND LASTUSED <> LASTRESERVED;
            """
        ).fetchone()

        if res is None:
            raise NoTestIDsError

        _, current, end = res

        with connection:
            connection.execute(
                """
                UPDATE SCMIDTABLE
                SET LASTUSED = ?
                WHERE TABLENAME == 'SCMobileTestsm1' AND LASTRESERVED = ?;
                """,
                (current + 1, end),
            )

    return f"SMX{str(current+1).zfill(10)}"


def add_test(test: Test, problem: Problem, *, _override: str | None = None) -> None:
    user = get_user()
    test_id = _get_new_test_id()
    spt_date = datetime.now().strftime(r"%Y-%m-%d %H:%M:%S.%f")[:-3]
    next_spt_date = (datetime.now() + timedelta(days=366)).strftime(r"%Y-%m-%d %H:%M:%S.%f")[:-3]

    with get_connection(DatabaseFilenames.TESTS, mode="rw") as connection, get_connection(DatabaseFilenames.ASSETS, mode="rw") as asset_connection:
        with connection, asset_connection:
            TestModel(test, problem, test_id, user, spt_date).insert(connection)
            ScriptTesterModel(test, test_id).insert(connection)

            lines = test.script.lines
            if test.script.number == 1287:
                track_header_line = ScriptLine(text="Disclaimer: Tests carried out are subject to conditions, available on request", number=1)
                lines = (track_header_line, *lines)

            for line in lines:
                ScriptLineModel(test, line, test_id, user).insert(connection)

            for job in test.jobs:
                JobModel(test, problem, test_id, job, user).insert(connection)

            asset_connection.execute(
                """
                UPDATE DEVICEA4
                SET service_last = ?, service_next = ?
                WHERE logical_name = ? AND service_type = ?;
                """,
                (spt_date, next_spt_date, test.item.number, test.script.service_type),
            )

            services: list[tuple[str, float, str, str]] = asset_connection.execute(
                """
                SELECT service_type, service_interval, service_last, service_next
                FROM DEVICEA4
                WHERE logical_name = ?;
                """,
                (test.item.number,),
            ).fetchall()

            servicearray = "\n".join("^".join(f"{int(s) if isinstance(s, float) else s}" for s in service) + "^" for service in services)

            connection.execute(
                """
                UPDATE devicem1_PS
                SET last_spt_date = ?, next_spt_date = ?, servicearray = ? 
                WHERE logical_name = ?;
                """,
                (spt_date, next_spt_date, servicearray, test.item.number),
            )
