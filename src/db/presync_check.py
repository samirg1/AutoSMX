from collections import Counter

from db.get_connection import get_connection, DatabaseFilenames
from design.Problem import Problem


def get_double_ups(problem: Problem) -> dict[str, list[str]]:
    double_ups: dict[str, list[str]] = {}

    if not len(problem.tests):
        return {}
    
    with get_connection(DatabaseFilenames.TESTS) as connection:
        current_tests: list[tuple[str, str, str]] = connection.execute(
            f"""
            SELECT logical_name, description, overall
            FROM SCMobileTestsm1
            WHERE test_id IN (?{", ?" * (len(problem.tests) - 1)})
            """,
            [test.id for test in problem.tests],
        ).fetchall()

        test_counter = Counter(number for number, *_ in current_tests)
        for number, count in test_counter.items():
            if count > 1:
                double_tests = [test for test in current_tests if test[0] == number]
                old = double_ups.get("Tests", [])
                old.extend(f"{number}: {desc} -> {overall}" for number, desc, overall in double_tests)
                double_ups["Tests"] = old
        

        current_jobs: list[tuple[str, str]] = connection.execute(
            f"""
            SELECT logical_name, actionprgn
            FROM SCMProbsUploadm1
            WHERE test_id IN (?{", ?" * (len(problem.tests) - 1)})
            """,
            [test.id for test in problem.tests]
        ).fetchall()

        job_counter = Counter(number for number, *_ in current_jobs)
        for number, count in job_counter.items():
            if count > 1:
                double_jobs = [job for job in current_jobs if job[0] == number]
                old = double_ups.get("Jobs", [])
                first_lines = [actionprgn.split('\n')[0] for _, actionprgn in double_jobs]
                old.extend(f"{number}: {line}" for (number, _), line in zip(double_jobs, first_lines))
                double_ups["Jobs"] = old

    return double_ups
