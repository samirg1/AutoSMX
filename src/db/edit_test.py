from db.get_connection import get_connection, DatabaseFilenames
from db.add_test import add_test
from design.Problem import Problem
from design.Test import Test


def edit_test(test: Test, problem: Problem) -> None:
    with get_connection(DatabaseFilenames.TESTS, mode="rw") as connection:
        connection.execute("DELETE FROM SCMobileTestsm1 WHERE test_id = ?;", (test.id,))
        connection.execute("DELETE FROM SCMobileTesterNumbersm1 WHERE test_id = ?", (test.id,))
        connection.execute("DELETE FROM SCMobileTestLinesm1 WHERE test_id = ?", (test.id,))
        connection.execute("DELETE FROM SCMProbsUploadm1 WHERE test_id = ?", (test.id,))

    add_test(test, problem)
