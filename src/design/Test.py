from datetime import datetime
from db.get_user import get_user
from design.data import get_all_scripts
from design.Item import Item
from design.Job import Job
from design.Script import Script
from db.get_new_test_id import get_new_test_id


class ScriptError(ValueError):
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

        raise ScriptError(f"No script found for {self.item.number}")

    def add_job(self, job: Job) -> None:
        self.jobs.append(job)

    def complete(self, comment: str, result: str, script_answers: list[str]) -> None:
        for answer, line in zip(script_answers, self.script.lines):
            line.result = "" if answer == " " else "N/A" if answer == "" else answer
        self.comments = comment.strip()
        self.result = result
        if not self.completed:
            self.id = get_new_test_id()
            self.user = get_user()
        self.date = datetime.now().strftime(r"%Y-%m-%d %H:%M:%S.%f")[:-3]
        self.completed = True
