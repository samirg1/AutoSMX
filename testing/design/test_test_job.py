from design.TestJob import TestJob

TestJob.__test__ = False  # type: ignore


def test_test_job_creation_and_string_representation():
    test_job = TestJob(department="Quality Control", contact_name="John Doe", comment="Performing testing on new batch.")

    assert test_job.department == "Quality Control"
    assert test_job.contact_name == "John Doe"
    assert test_job.comment == "Performing testing on new batch."
    assert str(test_job) == "Performing testing on new batch."
