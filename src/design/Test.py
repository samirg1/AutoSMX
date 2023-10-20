from design.data import get_all_scripts
from design.Item import Item
from design.Job import Job
from design.Script import Script


class ScriptError(ValueError):
    ...


class Test:
    def __init__(self, item: Item) -> None:
        self.item = item
        self.jobs: list[Job] = []
        self.comments = ""
        self.result = ""
        self.script: Script
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
        self.completed = True

    def __str__(self) -> str:
        return f"{self.item} - {self.result}"
