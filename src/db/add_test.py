from datetime import datetime
from typing import Any

from db.get_connection import DatabaseFilenames, get_connection
from db.get_user import get_user
from db.models import ScriptLineModel, ScriptTesterModel, TestModel
from design.Item import Item
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

        if res is None:  #!! CHECK THIS
            raise NoTestIDsError

        _, current, end = res

        # with connection:
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
    time = datetime.now().strftime(r"%Y-%m-%d %H:%M:%S.%f")[:-3]

    with get_connection(DatabaseFilenames.TESTS, mode="rw") as connection:
        # with connection:
        TestModel(test, problem, test_id, user, time).insert(connection)
        ScriptTesterModel(test, test_id).insert(connection)

        lines = test.script.lines
        if test.script.number == 1287:
            track_header_line = ScriptLine(text="Disclaimer: Tests carried out are subject to conditions, available on request", number=1)
            lines = (track_header_line, *lines)

        for line in lines:
            ScriptLineModel(test, line, test_id, user).insert(connection)

        # test_id = test_id if _override is None else _override

        # output: dict[str, Any] = {}

        # res = connection.execute(
        #     f"""
        #     SELECT * from SCMobileTestsm1 WHERE test_id == '{test_id}';
        # """
        # )
        # output["Test"] = list(zip((d[0] for d in res.description), res.fetchone()))

        # res = connection.execute(
        #     f"""
        #     SELECT * from SCMobileTesterNumbersm1 WHERE test_id == '{test_id}';
        # """
        # )
        # output["Script Number"] = list(zip((d[0] for d in res.description), res.fetchone()))

        # res = connection.execute(
        #     f"""
        #     SELECT * from SCMobileTestLinesm1 WHERE test_id == '{test_id}';
        # """
        # )
        # descs = [d[0] for d in res.description]
        # output["Lines"] = [list(zip(descs, r)) for r in res.fetchall()]

        # return output


# if __name__ == "__main__":
#     t = Test(item=Item("123456", "BED", "model", "manu", "serial", "room", None))
#     t.script = t.determine_script()
#     t.complete("comment", "final_res", ["pass"] * len(t.script.lines))

#     print(add_test(t, Problem("company", "campus", "dept", "pm12345", 1)))
