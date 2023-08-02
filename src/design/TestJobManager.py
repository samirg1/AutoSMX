from typing import Any, Callable

from design import Item, Job, TestJob

class setter:
    def __init__(self, func: Callable[[Any, Any], None], doc: str | None = None):
        self.func = func
        self.__doc__ = doc or func.__doc__

    def __set__(self, obj: Any, value: Any):
        self.func(obj, value)


class TestJobManager:

    def __init__(self):
        self._job_to_test_jobs: dict[Job, list[TestJob]] = {}
        self._item_to_test_job: dict[Item, list[TestJob]] = {}

        self._current_job: Job | None = None
        self._current_item: Item | None = None

    @setter
    def current_job(self, job: Job):
        self._current_job = job

    @setter
    def current_item(self, item: Item):
        self._current_item = item

    def add_test_job(self, test_job: TestJob):
        if self._current_job is None or self._current_item is None:
            raise ValueError("No current job or item")

        self._job_to_test_jobs.setdefault(self._current_job, []).append(test_job)
        self._item_to_test_job.setdefault(self._current_item, []).append(test_job) 
