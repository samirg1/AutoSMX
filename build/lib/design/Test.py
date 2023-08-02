from typing import Literal

from design.TestJob import TestJob
from design.data import SCRIPTS
from design.Item import Item

TTestResult = Literal["PASS", "TAGGED", "REMOVED", "FIXED", "RAISED"]


class Test:
    def __init__(self, item: Item) -> None:
        self._item = item
        self._script = (resolve() for resolve in SCRIPTS[item.description])
        self._test_jobs: list[TestJob] = []
        self._comment = ""
        self._final_result = ""

    def add_job(self, department: str, contact_name: str | None) -> TestJob:
        self._test_jobs.append(TestJob(department, contact_name))
        return self._test_jobs[-1]

    def complete(self, comment: str, final_result: TTestResult):
        self._comment = comment
        self._final_result = final_result

    def full_info(self) -> str:
        base = f"{str(self)}"
        if self._comment:
            base += f"\nComment: {self._comment}"
        
        if self._test_jobs:
            base += "\nJobs:\n" + "\n".join(f"\t{job}" for job in self._test_jobs)

        return base
    
    def __str__(self) -> str:
        return f"{self._item} - {self._final_result}"

    
