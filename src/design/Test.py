from design.TestJob import TestJob
from design.data import SCRIPTS, Script
from design.Item import Item


class ScriptError(ValueError):
    ...


class Test:
    def __init__(self, item: Item) -> None:
        self._item = item
        self.script = self._determine_script()
        self.script_result: list[str] = []
        self.test_jobs: list[TestJob] = []
        self.comment = ""
        self.final_result = ""

    def _determine_script(self) -> Script:
        for script in SCRIPTS.values():
            if script.matches(self._item.description):
                return script

        raise ScriptError("No script found")
    
    @property
    def testjobs(self) -> list[TestJob]:
        return self.test_jobs

    def add_job(self, test_job: TestJob):
        self.test_jobs.append(test_job)

    def complete(self, comment: str, final_result: str, stest_answers: list[str]):
        self.script_result = stest_answers
        self.comment = comment
        self.final_result = final_result

    def full_info(self) -> str:
        base = f"{str(self)}"
        if self.comment:
            base += f"\nComment: {self.comment}"
        
        if self.test_jobs:
            base += "\nJobs:\n" + "\n".join(f"\t{job}" for job in self.test_jobs)

        return base
    
    def __str__(self) -> str:
        return f"{self._item} - {self.final_result}"

    
