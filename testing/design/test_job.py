from design.Item import Item
from design.Job import Job
from design.Test import Test
from design.data import SCRIPTS, Script

Test.__test__ = False  # type: ignore


def test_job_creation_and_properties():
    job = Job("CompanyX", "CampusA", "DepartmentY")

    assert job.company == "CompanyX"
    assert job.campus == "CampusA"
    assert job.department == "DepartmentY"
    assert len(job.tests) == 0


def test_job_add_test():
    job = Job("CompanyX", "CampusA", "DepartmentY")

    test1 = Test(Item("001", "Test Item 1", "ModelX", "ManufacturerX", "Room A", "2022-01-01", "XYZ001"))
    test2 = Test(Item("002", "Test Item 2", "ModelY", "ManufacturerY", "Room B", "2022-02-01", "XYZ002"))

    custom1 = Script("Custom1", "Custom Script", 2, (), exact_matches=["Test Item 1"])
    SCRIPTS["Custom1"] = custom1
    test1.set_script()
    custom2 = Script("Custom2", "Custom Script", 2, (), exact_matches=["Test Item 2"])
    SCRIPTS["Custom2"] = custom2
    test2.set_script()

    job.add_test(test1)
    job.add_test(test1)
    job.add_test(test2)

    assert len(job.tests) == 3
    assert len(job.test_breakdown) == 2
    assert job.test_breakdown["Custom1"] == 2
    assert job.test_breakdown["Custom2"] == 1


def test_job_string_representation():
    job = Job("CompanyX", "CampusA", "DepartmentY")

    assert str(job) == "CampusA\nCompanyX\nDepartmentY"


def test_job_full_info():
    job = Job("CompanyX", "CampusA", "DepartmentY")

    test1 = Test(Item("001", "Test Item 1", "ModelX", "ManufacturerX", "Room A", "2022-01-01", "XYZ001"))
    custom1 = Script("Custom1", "Custom Script", 2, (), exact_matches=["Test Item 1"])
    SCRIPTS["Custom1"] = custom1
    test1.set_script()

    job.add_test(test1)

    full_info = job.full_info()
    assert str(job) in full_info
    assert "\t001 - Test Item 1 - " in full_info

def test_job_hashing():
    job1 = Job("CompanyX", "CampusA", "DepartmentY")
    job2 = Job("CompanyY", "CampusB", "DepartmentZ")

    jobs_set = {job1, job2}

    assert len(jobs_set) == 2  # Ensure both jobs are considered distinct
