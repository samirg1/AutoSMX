from design.Item import Item
from design.Job import Job
from design.Test import Test
from design.Script import Script
from design.data import SCRIPTS

Test.__test__ = False  # type: ignore


def test_job_creation_and_properties():
    job = Job("CAMPEYN - ABLE VICTORIA", "CampusA", "DepartmentY")

    assert job.company == "ABLE"
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
    job1 = Job("CAMPEYN - YOORALLA", "CampusA", "DepartmentY")
    job2 = Job("BENETAS - ST PAULS", "CampusA", "DepartmentY")
    job3 = Job("JEWISH ST KILDA", "CampusA", "DepartmentY")

    assert str(job1) == "CampusA\nCAMPEYN\nDepartmentY"
    assert str(job2) == "CampusA\nBENETAS\nDepartmentY"
    assert str(job3) == "CampusA\nJEWISH CARE\nDepartmentY"


def test_job_hashing_and_eq():
    job1 = Job("CompanyX", "CampusA", "DepartmentY")
    job2 = Job("CompanyY", "CampusB", "DepartmentZ")
    job3 = Job("CompanyZ", "CampusA", "DepartmentZ")
    assert len({job1, job2}) == 2
    assert len({job1, job3}) == 1
    assert hash(job1) != hash(job2)
    assert hash(job1) == hash(job3)
