from db.add_test import add_test
from db.get_connection import get_connection
from db.update_item_history import update_item_history
from design.Problem import Problem
from design.Test import Test
from utils.constants import DatabaseFilenames


def edit_test(test: Test, problem: Problem, *, remove_only: bool = False) -> None:
    with get_connection(DatabaseFilenames.TESTS, mode="rw") as connection, get_connection(DatabaseFilenames.ASSETS, mode="rw") as asset_connection:
        with connection, asset_connection:
            connection.execute("DELETE FROM SCMobileTestsm1 WHERE test_id = ?;", (test.id,))
            connection.execute("DELETE FROM SCMobileTesterNumbersm1 WHERE test_id = ?", (test.id,))
            connection.execute("DELETE FROM SCMobileTestLinesm1 WHERE test_id = ?", (test.id,))
            connection.execute("DELETE FROM SCMProbsUploadm1 WHERE test_id = ?", (test.id,))

            update_item_history(test.item, test.script.service_type, test.item.last_update, connection, asset_connection)

    if not remove_only:
        add_test(test, problem)
