import pytest

from design.data import get_all_scripts
from design.Item import Item
from design.Problem import Problem
from design.Script import Script
from design.Test import Test
from testing.conftest import MockSqlObject

Test.__test__ = False  # type: ignore


@pytest.mark.parametrize("mock_sql_connect", ([[]],), indirect=True)
def test_problem_creation_and_properties(mock_sql_connect: MockSqlObject) -> None:
    problem = Problem("CAMPEYN - ABLE VICTORIA", "CampusA", "DepartmentY", "123", "123")

    assert problem.company == "CAMPEYN - ABLE VICTORIA"
    assert problem.campus == "CampusA"
    assert problem.department == "DepartmentY"
    assert problem.number == "123"
    assert problem.customer_number == "123"
    assert problem.previous_item_number == ""
    assert problem.open_problems == []
    assert len(problem.tests) == 0

    problem.set_previous_item_number("1234")
    assert problem.previous_item_number == "1234"


def test_problem_add_test(mock_sql_connect_scripts: MockSqlObject) -> None:
    problem = Problem("CompanyX", "CampusA", "DepartmentY", "123", "123", get_open_problems=False)

    test1 = Test(Item("001", "001", "Test Item 1", "ModelX", "ManufacturerX", "XYZ001", "RM1", "2019-01-01 03:45:44.759"))
    test2 = Test(Item("002", "001", "Test Item 2", "ModelY", "ManufacturerY", "XYZ002", "RM1", "2019-01-01 03:45:44.759"))

    custom1 = Script("Custom1", "Custom Script", 1, "999", "type", (), (), exact_matches=["Test Item 1"])
    get_all_scripts()["Custom1"] = custom1
    test1.script = test1.determine_script()
    custom2 = Script("Custom2", "Custom Script", 1, "999", "type", (), (), exact_matches=["Test Item 2"])
    get_all_scripts()["Custom2"] = custom2
    test2.script = test2.determine_script()

    problem.add_test(test1)
    problem.add_test(test1)
    problem.add_test(test2)

    assert len(problem.tests) == 3
    assert len(problem.test_breakdown) == 2
    assert problem.test_breakdown["Custom1"] == 2
    assert problem.test_breakdown["Custom2"] == 1


def test_problem_remove_test(mock_sql_connect_scripts: MockSqlObject) -> None:
    custom1 = Script("Custom1", "Custom Script", 1, "999", "type", (), (), exact_matches=["Test Item 1"])
    get_all_scripts()["Custom1"] = custom1
    test1 = Test(Item("001", "001", "Test Item 1", "ModelX", "ManufacturerX", "XYZ001", "RM1", "2019-01-01 03:45:44.759"))
    test1.script = test1.determine_script()
    problem = Problem("CompanyX", "CampusA", "DepartmentY", "123", "123", get_open_problems=False)
    problem.add_test(test1)
    problem.remove_test(test1)

    assert len(problem.tests) == 0
    assert len(problem.test_breakdown) == 0
    assert "Custom1" not in problem.test_breakdown


def test_problem_string_representation() -> None:
    problem1 = Problem("CAMPEYN - YOORALLA", "CampusA", "DepartmentY", "123", "123", get_open_problems=False)
    problem2 = Problem("BENETAS - ST PAULS", "CampusA", "DepartmentY", "123", "123", get_open_problems=False)
    problem3 = Problem("JEWISH ST KILDA", "CampusA", "DepartmentY", "123", "123", get_open_problems=False)

    assert str(problem1) == "123 - CampusA - CAMPEYN - YOORALLA"
    assert str(problem2) == "123 - CampusA - BENETAS - ST PAULS"
    assert str(problem3) == "123 - CampusA - JEWISH ST KILDA"


def test_problem_hashing_and_eq() -> None:
    problem1 = Problem("CompanyX", "CampusA", "DepartmentY", "123", "123", get_open_problems=False)
    problem2 = Problem("CompanyY", "CampusB", "DepartmentZ", "123", "123", get_open_problems=False)
    problem3 = Problem("CompanyZ", "CampusA", "DepartmentZ", "123", "123", get_open_problems=False)
    assert len({problem1, problem2}) == 2
    assert len({problem1, problem3}) == 1
    assert hash(problem1) != hash(problem2)
    assert hash(problem1) == hash(problem3)
