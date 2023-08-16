from design.data import SCRIPTS, Script
from design.Item import Item
from design.TestJob import TestJob


class ScriptError(ValueError):
    ...


class Test:
    def __init__(self, item: Item) -> None:
        self.item = item
        self.script_answers: list[str] = []
        self.testjobs: list[TestJob] = []
        self.comment = ""
        self.final_result = ""
        self.script: Script

    @property
    def item_model(self) -> str:
        return f"{self.script.name} -> {self.item.model}"

    def _determine_script(self) -> Script:
        if self.item.description != "":
            for script in SCRIPTS.values():
                if self.item.description in script.exact_matches:
                    return script

            for script in SCRIPTS.values():
                if script.is_for(self.item.description):
                    return script

        raise ScriptError("No script found")

    def set_script(self, script: Script | None = None):
        if script is None:
            script = self._determine_script()
        self.script = script

    def add_testjob(self, testjob: TestJob):
        self.testjobs.append(testjob)

    def complete(self, comment: str, final_result: str, script_answers: list[str]):
        self.script_answers = ["" if a == " " else "N/A" if a == "" else a for a in script_answers]
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
        return f"{self.item} - {self.final_result}"
