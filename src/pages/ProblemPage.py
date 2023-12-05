from collections import Counter

import customtkinter as ctk

from design.Problem import Problem
from pages.Page import Page
from popups.ProblemEntryPopup import ProblemEntryPopup
from popups.SyncPopup import SyncPopup
from utils.add_focus_bindings import add_focus_bindings
from utils.ask_for_confirmation import ask_for_confirmation
from utils.constants import DEFAULT_TEXT_COLOUR_LABEL, HORIZONTAL_LINE, UNSYNCED_TEXT_COLOUR_LABEL


class ProblemPage(Page):
    def setup(self) -> None:
        self.problems = self.storage.problems

        # top row
        ctk.CTkLabel(self.frame, text="Problems").grid(column=0, row=0, columnspan=17)
        add_button = ctk.CTkButton(self.frame, text="+", command=self.add_tests)
        add_button.grid(column=17, row=0, columnspan=1)
        add_focus_bindings(add_button)
        add_button.bind("<Return>", lambda _: add_button.invoke())
        for i, campus in enumerate(self.problems.keys(), start=1):
            add_button.bind(f"{i}", lambda _, campus=campus: self.add_tests(campus))  # type: ignore[misc]
            add_button.bind(f"<Alt-Key-{i}>", lambda _, campus=campus: self.delete_problem(campus))  # type: ignore[misc]
        settings_button = ctk.CTkButton(self.frame, text="Settings", command=lambda: self.change_page("SETTINGS"))
        settings_button.grid(column=18, row=0, columnspan=1)
        add_button.bind("s", lambda _: settings_button.invoke())
        ctk.CTkButton(self.frame, text="Sync", command=self.sync).grid(row=0, column=19, columnspan=1)
        ctk.CTkLabel(self.frame, text=HORIZONTAL_LINE).grid(column=0, row=1, columnspan=20)
        row = 2

        if not self.problems:
            ctk.CTkLabel(self.frame, text="No problems yet, click '+' to add").grid(row=row, column=0, sticky=ctk.EW, columnspan=20)

        for campus, problem in self.problems.items():
            ctk.CTkLabel(self.frame, text=f"{problem}").grid(row=row, column=0, sticky=ctk.W, columnspan=18)
            ctk.CTkButton(self.frame, text="Enter", command=lambda campus=campus: self.add_tests(campus)).grid(row=row, column=18, columnspan=1)  # type: ignore[misc]
            ctk.CTkButton(self.frame, text="Delete", command=lambda campus=campus: self.delete_problem(campus)).grid(row=row, column=19, columnspan=1)  # type: ignore[misc]
            row += 1

            if problem.open_problems:
                ctk.CTkLabel(self.frame, text=f"Open Problems ({len(problem.open_problems)})").grid(row=row, column=1, sticky=ctk.W, columnspan=19)
                row += 1
                for open_problem in problem.open_problems:
                    ctk.CTkLabel(self.frame, text=f"- {open_problem}").grid(row=row, column=2, sticky=ctk.W, columnspan=18)
                    row += 1

            problem_jobs = self.storage.job_manager.problem_to_jobs.get(problem, [])
            if problem_jobs:
                synced = sum(1 for job in problem_jobs if job.synced)
                ctk.CTkLabel(self.frame, text=f"Jobs Raised ({synced})").grid(row=row, column=1, sticky=ctk.W, columnspan=19)
                if synced != len(problem_jobs):
                    ctk.CTkLabel(self.frame, text=f" (+{len(problem_jobs) - synced})", text_color=UNSYNCED_TEXT_COLOUR_LABEL).grid(row=row, column=3, sticky=ctk.W, columnspan=19)
                row += 1

                for job in problem_jobs:
                    colour = DEFAULT_TEXT_COLOUR_LABEL if job.synced else UNSYNCED_TEXT_COLOUR_LABEL
                    item = self.storage.job_manager.job_to_item[job]
                    comment = job.comment.replace("\n", " | ")
                    ctk.CTkLabel(self.frame, text=f"- {item.description} ({item.number}): {comment}", text_color=colour).grid(row=row, column=2, sticky=ctk.W, columnspan=18)
                    row += 1

            if problem.tests:
                synced = sum(1 for test in problem.tests if test.synced)
                ctk.CTkLabel(self.frame, text=f"Tests ({synced})").grid(row=row, column=1, sticky=ctk.W, columnspan=19)
                if synced != len(problem.tests):
                    ctk.CTkLabel(self.frame, text=f" (+{len(problem.tests) - synced})", text_color=UNSYNCED_TEXT_COLOUR_LABEL).grid(row=row, column=3, sticky=ctk.W, columnspan=19)
                row += 1

                unsynced_counter = Counter(test.script.nickname for test in problem.tests if not test.synced)
                for script_name, value in problem.test_breakdown.items():
                    unsynced = unsynced_counter[script_name]
                    ctk.CTkLabel(self.frame, text=f"- {script_name} ({value - unsynced})").grid(row=row, column=2, sticky=ctk.W, columnspan=18)
                    if unsynced != 0:
                        ctk.CTkLabel(self.frame, text=f" (+{unsynced})", text_color=UNSYNCED_TEXT_COLOUR_LABEL).grid(row=row, column=4, sticky=ctk.W, columnspan=18)
                    row += 1

            self.frame.rowconfigure(row, minsize=20)
            row += 1

            self.frame.after(201, add_button.focus)

    def delete_problem(self, campus: str) -> None:
        if not ask_for_confirmation("Are you sure?", "If you delete this problem the data stored within this application will be lost and you won't be able to make any more edits"):
            return

        with self.storage.edit() as storage:
            problem = self.problems[campus]
            del storage.problems[problem.campus]
            if problem in self.storage.job_manager.problem_to_jobs:
                del self.storage.job_manager.problem_to_jobs[problem]
                for test in problem.tests:
                    for job in test.jobs:
                        del self.storage.job_manager.job_to_item[job]
        self.change_page("PROBLEM")

    def add_tests(self, campus: str | None = None) -> None:
        if campus is None:
            ProblemEntryPopup(self.frame, lambda problem: self.add_problem(problem))
        else:
            self.add_problem(self.problems[campus], go_to_tests=True)

    def add_problem(self, problem: Problem, *, go_to_tests: bool = False) -> None:
        self.storage.problem = problem
        with self.storage.edit() as storage:
            storage.problems[problem.campus] = problem
        self.change_page("TEST" if go_to_tests else "PROBLEM")

    def sync(self) -> None:
        SyncPopup(self.frame, self.storage.problems)
