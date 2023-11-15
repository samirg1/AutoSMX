from design.Job import Job
from design.Part import Part


def test_job_creation_and_string_representation() -> None:
    job = Job("Quality Control", "John Doe", "Performing\ntesting on\nnew batch.", [(Part("123", "1", "1", "1"), 1)])

    assert job.department == "Quality Control"
    assert job.contact_name == "John Doe"
    assert job.comment == "Performing\ntesting on\nnew batch.\n1 X 123"
    assert job.test_comment == "Performing\ntesting on\nnew batch."
    assert len(job.part_quantities) == 1
    assert str(job) == "Performing\ntesting on\nnew batch.\n1 X 123"
