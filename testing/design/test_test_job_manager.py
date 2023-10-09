from design.Item import Item
from design.Job import Job
from design.TestJob import TestJob
from design.TestJobManager import TestJobManager

TestJob.__test__ = False  # type: ignore
TestJobManager.__test__ = False  # type: ignore


def test_test_job_manager_multiple_testjobs() -> None:
    manager = TestJobManager()

    item1 = Item("001", "Test Item 1", "ModelX", "ManufacturerX", "XYZ001", "R1", "2019-01-01 03:45:44.759")
    job1 = Job("Company", "Campus", "Department", "123", 123, get_problems=False)
    testjob1 = TestJob("Quality Control", "John Doe", "Performing testing on batch 1")
    testjob2 = TestJob("Quality Control", "Jane Smith", "Inspection for defects")

    manager.add_testjob(item1, job1, testjob1)
    manager.add_testjob(item1, job1, testjob2)

    assert len(manager.job_to_testjobs[job1]) == 2
    assert manager.testjob_to_item[testjob1] == item1
    assert manager.testjob_to_item[testjob2] == item1

    manager.delete_testjob(job1, testjob1)

    assert len(manager.job_to_testjobs[job1]) == 1
    assert manager.testjob_to_item[testjob2] == item1


def test_test_job_manager_multiple_items() -> None:
    manager = TestJobManager()

    item1 = Item("001", "Test Item 1", "ModelX", "ManufacturerX", "XYZ001", "RM1", "2019-01-01 03:45:44.759")
    item2 = Item("002", "Test Item 2", "ModelY", "ManufacturerY", "XYZ002", "RM1", "2019-01-01 03:45:44.759")
    job1 = Job("Company", "Campus", "Department", "123", 123, get_problems=False)
    testjob1 = TestJob("Quality Control", "John Doe", "Performing testing on batch 1")

    manager.add_testjob(item1, job1, testjob1)
    manager.add_testjob(item2, job1, testjob1)

    assert len(manager.job_to_testjobs[job1]) == 2
    assert manager.testjob_to_item[testjob1] == item2
