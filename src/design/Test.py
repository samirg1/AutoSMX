from design.data import SCRIPTS, Script
from design.Item import Item
from design.TestJob import TestJob


class ScriptError(ValueError):
    ...


class Test:
    def __init__(self, item: Item) -> None:
        self._item = item
        self.script = self._determine_script()
        self.script_answers: list[str] = []
        self.testjobs: list[TestJob] = []
        self.comment = ""
        self.final_result = ""

    def _determine_script(self) -> Script:
        for script in SCRIPTS.values():
            if script.matches(self._item.description):
                return script

        raise ScriptError("No script found")

    def add_testjob(self, testjob: TestJob):
        self.testjobs.append(testjob)

    def complete(self, comment: str, final_result: str, script_answers: list[str]):
        self.script_answers = script_answers
        self.comment = comment
        self.final_result = final_result

    def full_info(self) -> str:
        base = f"{str(self)}"
        if self.comment:
            base += f"\nComment: {self.comment}"

        if self.testjobs:
            base += "\nJobs:\n" + "\n".join(f"\t{job}" for job in self.testjobs)

        return base

    def __str__(self) -> str:
        return f"{self._item} - {self.final_result}"
