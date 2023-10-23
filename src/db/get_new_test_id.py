from db.get_connection import DatabaseFilenames, get_connection


class NoTestIDsError(RuntimeError):
    ...


def get_new_test_id() -> str:
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
