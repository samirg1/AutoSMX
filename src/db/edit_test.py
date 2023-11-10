from db.get_connection import get_connection
from db.add_test import add_test
from design.Problem import Problem
from design.Test import Test
from utils.constants import DatabaseFilenames


def edit_test(test: Test, problem: Problem, *, remove_only: bool = False) -> None:
    with get_connection(DatabaseFilenames.TESTS, mode="rw") as connection:
        with connection:
            connection.execute("DELETE FROM SCMobileTestsm1 WHERE test_id = ?;", (test.id,))
            connection.execute("DELETE FROM SCMobileTesterNumbersm1 WHERE test_id = ?", (test.id,))
            connection.execute("DELETE FROM SCMobileTestLinesm1 WHERE test_id = ?", (test.id,))
            connection.execute("DELETE FROM SCMProbsUploadm1 WHERE test_id = ?", (test.id,))

    if not remove_only:
        add_test(test, problem)
