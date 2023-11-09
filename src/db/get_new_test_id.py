from db.get_connection import DatabaseFilenames, get_connection
from utils.validate_type import validate_type


class NoTestIDsError(RuntimeError):
    ...


def get_new_test_id() -> str:
    with get_connection(DatabaseFilenames.SETTINGS, mode="rw") as connection:
        res = validate_type(
            tuple[int, int] | None,
            connection.execute(
                """
                SELECT LASTUSED, LASTRESERVED
                FROM SCMIDTABLE
                WHERE TABLENAME == 'SCMobileTestsm1' AND LASTUSED <> LASTRESERVED;
                """
            ).fetchone(),
        )

        if res is None:
            raise NoTestIDsError

        current, end = res

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
