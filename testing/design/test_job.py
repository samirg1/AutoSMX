import pytest

from design.Job import Job


def test_job_creation_and_string_representation() -> None:
    job = Job("Quality Control", "John Doe", "Performing\ntesting on\nnew batch.")

    assert job.department == "Quality Control"
    assert job.contact_name == "John Doe"
    assert job.comment == "Performing\ntesting on\nnew batch."
    assert job.test_comment == "Performing\ntesting on\nnew batch."
    assert job.part_number == ""
    assert job.part_quantity == 0
    assert str(job) == "Performing\ntesting on\nnew batch."


@pytest.mark.parametrize("comment", ("C\nD\nE\n1 X 12345\n", "C\nD\nE\n1 x 12345\n\n"))
def test_job_test_comment(comment: str) -> None:
    job = Job("A", "B", comment)

    assert job.comment == comment.strip()
    assert job.test_comment == "C\nD\nE"
    assert job.part_number == "12345"
    assert job.part_quantity == 1


@pytest.mark.parametrize("comment", ("C\nD\nE\na X 12345\n    ", "C\nD\nE\n2 a 12345   \n"))
def test_job_invalid_last_line(comment: str) -> None:
    job = Job("A", "B", comment)

    assert job.comment == job.test_comment == comment.strip()
    assert job.part_number == ""
    assert job.part_quantity == 0
