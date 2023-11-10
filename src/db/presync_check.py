from collections import Counter

from db.get_connection import get_connection
from design.Problem import Problem
from utils.constants import DatabaseFilenames
from typeguard import check_type


def get_double_ups(problem: Problem) -> dict[str, list[str]]:
    double_ups: dict[str, list[str]] = {}

    if not len(problem.tests):
        return {}

    with get_connection(DatabaseFilenames.TESTS) as connection:
        current_tests = check_type(
            connection.execute(
                f"""
                SELECT logical_name, description, overall
                FROM SCMobileTestsm1
                WHERE test_id IN (?{", ?" * (len(problem.tests) - 1)});
                """,
                [test.id for test in problem.tests],
            ).fetchall(),
            list[tuple[str, str, str]],
        )

        test_counter = Counter(number for number, *_ in current_tests)
        for number, count in test_counter.items():
            if count > 1:
                double_tests = [test for test in problem.tests if test.item.number == number and not test.synced]
                if not double_tests:
                    continue
                old = double_ups.get("Tests", [])
                old.extend(f"{number}: {test.item.description} ({test.script.nickname}) -> {test.result}" for test in double_tests)
                double_ups["Tests"] = old

        current_jobs = check_type(
            connection.execute(
                f"""
                SELECT logical_name, actionprgn
                FROM SCMProbsUploadm1
                WHERE test_id IN (?{", ?" * (len(problem.tests) - 1)});
                """,
                [test.id for test in problem.tests],
            ).fetchall(),
            list[tuple[str, str]],
        )

        job_counter = Counter(number for number, *_ in current_jobs)
        jobs_items = [(job, test.item.number) for test in problem.tests for job in test.jobs]
        for number, count in job_counter.items():
            if count > 1:
                double_jobs = [job for job in jobs_items if job[1] == number and not job[0].synced]
                if not double_jobs:
                    continue
                old = double_ups.get("Jobs", [])
                first_lines = [job[0].comment.split("\n")[0] for job in double_jobs]
                old.extend(f"{item}: {line}" for (_, item), line in zip(double_jobs, first_lines))
                double_ups["Jobs"] = old

    return double_ups
