from design.data import get_all_scripts
from design.Item import Item
from design.Job import Job
from design.Script import Script


class ScriptError(ValueError):
    ...


class Test:
    def __init__(self, item: Item) -> None:
        self.item = item
        self.script_answers: list[str] = []
        self.jobs: list[Job] = []
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

        raise ScriptError(f"No script found for {self.item.number}")

    def add_job(self, job: Job) -> None:
        self.jobs.append(job)

    def complete(self, comment: str, final_result: str, script_answers: list[str]) -> None:
        self.script_answers = ["" if a == " " else "N/A" if a == "" else a for a in script_answers]
        self.comment = comment.strip()
        self.final_result = final_result

    def __str__(self) -> str:
        return f"{self.item} - {self.final_result}"
