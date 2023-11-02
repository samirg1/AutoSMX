from design.Item import Item
from design.Job import Job
from design.JobManager import JobManager
from design.Problem import Problem


def test_test_job_manager_multiple_jobs() -> None:
    manager = JobManager()

    item1 = Item("001", "002", "Test Item 1", "ModelX", "ManufacturerX", "XYZ001", "R1", "2019-01-01 03:45:44.759")
    problem = Problem("Company", "Campus", "Department", "PM123", "123", get_open_problems=False)
    job1 = Job("Quality Control", "John Doe", "Performing testing on batch 1")
    job2 = Job("Quality Control", "Jane Smith", "Inspection for defects")

    manager.add_job(item1, problem, job1)
    manager.add_job(item1, problem, job2)

    assert len(manager.problem_to_jobs[problem]) == 2
    assert manager.job_to_item[job1] == item1
    assert manager.job_to_item[job2] == item1

    manager.delete_job(problem, job1)

    assert len(manager.problem_to_jobs[problem]) == 1
    assert manager.job_to_item[job2] == item1


def test_test_job_manager_multiple_items() -> None:
    manager = JobManager()

    item1 = Item("001", "001", "Test Item 1", "ModelX", "ManufacturerX", "XYZ001", "RM1", "2019-01-01 03:45:44.759")
    item2 = Item("002", "002", "Test Item 2", "ModelY", "ManufacturerY", "XYZ002", "RM1", "2019-01-01 03:45:44.759")
    problem = Problem("Company", "Campus", "Department", "123", "123", get_open_problems=False)
    job = Job("Quality Control", "John Doe", "Performing testing on batch 1")

    manager.add_job(item1, problem, job)
    manager.add_job(item2, problem, job)

    assert len(manager.problem_to_jobs[problem]) == 2
    assert manager.job_to_item[job] == item2
