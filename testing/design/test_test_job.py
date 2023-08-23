import pytest

from design.TestJob import TestJob

TestJob.__test__ = False  # type: ignore


def test_test_job_creation_and_string_representation():
    test_job = TestJob("Quality Control", "John Doe", "Performing\ntesting on\nnew batch.")

    assert test_job.department == "Quality Control"
    assert test_job.contact_name == "John Doe"
    assert test_job.comment == "Performing\ntesting on\nnew batch."
    assert test_job.test_comment == "Performing\ntesting on\nnew batch."
    assert test_job.part_number == ""
    assert test_job.part_quantity == 0
    assert str(test_job) == "Performing\ntesting on\nnew batch."


@pytest.mark.parametrize("comment", ("C\nD\nE\n1 X 12345\n", "C\nD\nE\n1 x 12345\n\n"))
def test_test_job_test_comment(comment: str):
    test_job = TestJob("A", "B", comment)

    assert test_job.comment == comment.strip()
    assert test_job.test_comment == "C\nD\nE"
    assert test_job.part_number == "12345"
    assert test_job.part_quantity == 1


@pytest.mark.parametrize("comment", ("C\nD\nE\na X 12345\n    ", "C\nD\nE\n2 a 12345   \n"))
def test_test_job_invalid_last_line(comment: str):
    test_job = TestJob("A", "B", comment)

    assert test_job.comment == test_job.test_comment == comment.strip()
    assert test_job.part_number == ""
    assert test_job.part_quantity == 0
