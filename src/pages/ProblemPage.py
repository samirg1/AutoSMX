import customtkinter as ctk

from design.Problem import Problem
from pages.Page import Page
from popups.ProblemEntryPopup import ProblemEntryPopup
from popups.SyncPopup import SyncPopup


class ProblemPage(Page):
    def setup(self) -> None:
        self.problems = self.storage.problems

        # top row
        ctk.CTkLabel(self.frame, text="Problems").grid(column=0, row=0, columnspan=17)
        add_button = ctk.CTkButton(self.frame, text="+", command=self.add_tests)
        add_button.grid(column=17, row=0, columnspan=1)
        add_button.bind("<FocusIn>", lambda _: add_button.configure(text_color="black"))
        add_button.bind("<FocusOut>", lambda _: add_button.configure(text_color="white"))
        add_button.bind("<Return>", lambda _: add_button.invoke())
        for i, campus in enumerate(self.problems.keys(), start=1):
            add_button.bind(f"{i}", lambda _, campus=campus: self.add_tests(campus))  # type: ignore[misc]
            add_button.bind(f"<Alt-Key-{i}>", lambda _, campus=campus: self.delete_problem(campus))  # type: ignore[misc]
        ctk.CTkButton(self.frame, text="Settings", command=lambda: self.change_page("SETTINGS")).grid(column=18, row=0, columnspan=1)
        ctk.CTkButton(self.frame, text="Sync", command=self.sync).grid(row=0, column=19, columnspan=1)
        ctk.CTkLabel(self.frame, text=f"{'-' * 600}").grid(column=0, row=1, columnspan=20)
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
                ctk.CTkLabel(self.frame, text=f"Jobs Raised ({len(problem_jobs)})").grid(row=row, column=1, sticky=ctk.W, columnspan=19)
                row += 1
                for job in problem_jobs:
                    item = self.storage.job_manager.job_to_item[job]
                    comment = job.comment.replace("\n", " | ")
                    ctk.CTkLabel(self.frame, text=f"- {item.description} ({item.number}): {comment}").grid(row=row, column=2, sticky=ctk.W, columnspan=18)
                    row += 1

            if problem.tests:
                ctk.CTkLabel(self.frame, text=f"Tests ({len(problem.tests)})").grid(row=row, column=1, sticky=ctk.W, columnspan=19)
                row += 1
                for script_name, value in problem.test_breakdown.items():
                    ctk.CTkLabel(self.frame, text=f"- {script_name} ({value})").grid(row=row, column=2, sticky=ctk.W, columnspan=18)
                    row += 1

            self.frame.rowconfigure(row, minsize=20)
            row += 1

            self.frame.after(201, add_button.focus)

    def delete_problem(self, campus: str) -> None:
        with self.storage.edit() as storage:
            problem = self.problems[campus]
            del storage.problems[problem.campus]
        if problem in self.storage.job_manager.problem_to_jobs:
            del self.storage.job_manager.problem_to_jobs[problem]
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
        SyncPopup(self.frame, self.storage.problems).mainloop()
