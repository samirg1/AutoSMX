from typing import NamedTuple

from design.data import get_all_scripts
from design.Item import Item
from design.Script import Script
from design.TestJob import TestJob


class _TEST_RESULT(NamedTuple):
    name: str
    result: str


TEST_RESULTS = [
    _TEST_RESULT("Pass", "Passed"),
    _TEST_RESULT("Defect", "Passed - needs attention to minor defect"),
    _TEST_RESULT("Repaired", "Passed after minor repairs"),
    _TEST_RESULT("Tagged", "Failed and RED Tagged"),
    _TEST_RESULT("Removed", "Failed and removed from service"),
    _TEST_RESULT("Untested", "Not Tested"),
    _TEST_RESULT("Fail-Unable", "Fail - Unable to Test"),
]


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

    def determine_script(self) -> Script:
        if self.item.description != "":
            for script in get_all_scripts().values():
                if self.item.description in script.exact_matches:
                    return script

            for script in get_all_scripts().values():
                if script.is_for(self.item.description):
                    return script

        raise ScriptError("No script found")

    def add_testjob(self, testjob: TestJob) -> None:
        self.testjobs.append(testjob)

    def complete(self, comment: str, final_result: str, script_answers: list[str]) -> None:
        self.script_answers = ["" if a == " " else "N/A" if a == "" else a for a in script_answers]
        self.comment = comment.strip()
        self.final_result = final_result

    def __str__(self) -> str:
        return f"{self.item} - {self.final_result}"
