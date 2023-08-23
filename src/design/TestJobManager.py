from design.Item import Item
from design.Job import Job
from design.TestJob import TestJob


class TestJobManager:
    def __init__(self):
        self.job_to_testjobs: dict[Job, list[TestJob]] = {}
        self.item_to_testjob: dict[Item, list[TestJob]] = {}
        self.testjob_to_item: dict[TestJob, Item] = {}

    def add_testjob(self, item: Item, job: Job, testjob: TestJob):
        self.job_to_testjobs.setdefault(job, []).append(testjob)
        self.item_to_testjob.setdefault(item, []).append(testjob)
        self.testjob_to_item[testjob] = item

    def delete_testjob(self, item: Item, job: Job, testjob: TestJob):
        self.job_to_testjobs[job].pop()
        self.item_to_testjob[item].pop()
        del self.testjob_to_item[testjob]
