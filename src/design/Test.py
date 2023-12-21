from datetime import datetime

from db.get_new_test_id import get_new_test_id
from db.get_user import get_user
from utils.get_available_scripts import get_available_scripts
from design.Item import Item
from design.Job import Job
from design.Script import Script
from utils.get_sysmodtime import get_sysmodtime


class ScriptError(ValueError):
    ...


class InvalidTestResultError(ValueError):
    ...


class Test:
    def __init__(self, item: Item) -> None:
        self.item = item
        self.jobs: list[Job] = []
        self.script: Script
        self.comments = ""
        self.result = ""
        self.id = ""
        self.user = ""
        self.date = ""
        self.completed = False
        self.synced = False

    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, Test):
            return __value.id == self.id
        return False

    @property
    def item_model(self) -> str:
        return f"{self.script.name} -> {self.item.model}"

    def determine_script(self) -> Script:
        if self.item.description and self.item.description != "":
            for script in get_available_scripts().values():
                if self.item.description in script.exact_matches:
                    return script

            for script in get_available_scripts().values():
                if script.is_for(self.item.description):
                    return script

        raise ScriptError(f"No script found for {self.item.number}")

    def add_job(self, job: Job) -> None:
        self.jobs.append(job)

    def complete(self, comment: str, result: str, script_answers: list[str]) -> None:
        for job in self.jobs:
            job.finalise(self.item.room or "Unknown")

        if result == "":
            raise InvalidTestResultError("Test result not selected")

        if self.jobs:
            if comment == "":
                raise InvalidTestResultError("Job raised but no overall comment present")
            elif result == "Pass":
                raise InvalidTestResultError("Job raised but overall result is 'Pass'")

        if any(answer == "Fail" for answer in script_answers):
            if comment == "":
                raise InvalidTestResultError("Failed script line but no overall comment present")
            elif result.startswith("Pass"):
                raise InvalidTestResultError("Failed script line but used a 'Pass' overall result option")

        for answer, line in zip(script_answers, self.script.lines):
            if line.required and answer in ("", " "):
                raise InvalidTestResultError(f"Required line '{line.text}' not filled")
            line.result = "" if answer == " " else "N/A" if answer == "" else answer
        self.comments = comment
        self.result = result
        if not self.completed:
            self.id = get_new_test_id()
            self.user = get_user()
        self.date = get_sysmodtime(datetime.now())
        self.completed = True

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.__dict__})"
