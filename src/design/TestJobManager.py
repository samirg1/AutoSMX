from design import Item, Job, TestJob


class TestJobManager:
    def __init__(self):
        self._job_to_test_jobs: dict[Job, list[TestJob]] = {}
        self._item_to_test_job: dict[Item, list[TestJob]] = {}

    def add_test_job(self, item: Item, job: Job, test_job: TestJob):
        self._job_to_test_jobs.setdefault(job, []).append(test_job)
        self._item_to_test_job.setdefault(item, []).append(test_job)
