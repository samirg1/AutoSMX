from design.Item import Item
from design.Job import Job
from design.TestJob import TestJob


class TestJobManager:
    def __init__(self):
        self.job_to_testjobs: dict[Job, list[TestJob]] = {}
        self.testjob_to_item: dict[TestJob, Item] = {}

    def add_testjob(self, item: Item, job: Job, testjob: TestJob):
        self.job_to_testjobs.setdefault(job, []).append(testjob)
        self.testjob_to_item[testjob] = item

    def delete_testjob(self, job: Job, testjob: TestJob):
        self.job_to_testjobs[job].pop()
        del self.testjob_to_item[testjob]
