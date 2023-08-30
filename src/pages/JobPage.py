import tkinter
from tkinter import ttk

from design.Job import Job
from pages.Page import Page


class JobPage(Page):
    def setup(self):
        # top row
        ttk.Label(self.frame, text="Jobs").grid(column=0, row=0, columnspan=1)
        ttk.Button(self.frame, text="+", width=1, command=lambda: self.add_tests(add_new_job=True)).grid(column=1, row=0, columnspan=1)
        ttk.Button(self.frame, text="Tutorial", command=self.tutorial).grid(column=2, row=0, columnspan=1)
        ttk.Button(self.frame, text="Calibrate", command=self.calibrate).grid(column=3, row=0, columnspan=1)
        ttk.Label(self.frame, text=f"{'-' * 50}").grid(column=0, row=1, columnspan=4)
        row = 2

        self.tree = ttk.Treeview(self.frame, columns=("text", "number"), show="tree headings", height=10, selectmode="browse")
        style = ttk.Style(self.frame)
        style.configure("Treeview", rowheight=50)  # type: ignore
        self.tree.column("#0", width=0)
        self.tree.column("text", anchor=tkinter.W)
        self.tree.column("number", width=10, anchor=tkinter.CENTER)
        self.tree.heading("text", text="Jobs")
        self.tree.heading("number", text="#")

        for campus, job in self.shared.jobs.items():
            job_node = self.tree.insert("", tkinter.END, campus, values=(f"{job}",))

            job_testjobs = self.shared.testjob_manager.job_to_testjobs.get(job, [])
            if job_testjobs:
                testjob_node = self.tree.insert(job_node, tkinter.END, values=("Jobs Raised", len(job_testjobs)))
                for testjob in job_testjobs:
                    item = self.shared.testjob_manager.testjob_to_item[testjob]
                    first_line = str(testjob).split("\n")[0]
                    self.tree.insert(testjob_node, tkinter.END, values=(f"{first_line}", item.number))

            if job.tests:
                test_node = self.tree.insert(job_node, tkinter.END, values=("Tests", f"{len(job.tests)}"))
                for script_name, value in job.test_breakdown.items():
                    self.tree.insert(test_node, tkinter.END, values=(f"{script_name}", value))

        scrollbar = ttk.Scrollbar(self.frame, orient=tkinter.VERTICAL, command=self.tree.yview)  # type: ignore
        self.tree.configure(yscroll=scrollbar.set)  # type: ignore
        scrollbar.grid(row=row, column=4, sticky=tkinter.NS)
        self.tree.grid(row=row, column=0, columnspan=4, sticky=tkinter.EW)
        row += 1

        ttk.Button(self.frame, text=">", command=self.add_tests, width=1).grid(row=row, column=0)
        ttk.Button(self.frame, text="X", command=self.delete_job, width=1).grid(row=row, column=1)

    def get_selected_job(self) -> Job | None:
        item = self.tree.focus()
        possible_parent1 = self.tree.parent(item)
        parent1 = possible_parent1 if possible_parent1 else item
        possible_parent2 = self.tree.parent(parent1)
        parent2 = possible_parent2 if possible_parent2 else parent1

        return self.shared.jobs[parent2] if parent2 else None

    def delete_job(self) -> None:
        job = self.get_selected_job()
        if job is None:
            return
        del self.shared.jobs[job.campus]
        self.change_page("JOB")

    def add_tests(self, /, *, add_new_job: bool = False) -> None:
        self.shared.job = None if add_new_job else self.get_selected_job()
        self.change_page("TEST")

    def calibrate(self):
        with self.shared.storage.edit() as storage:
            storage.calibrated = False
        self.change_page("CALIBRATION")

    def tutorial(self):
        with self.shared.storage.edit() as storage:
            storage.tutorial_complete = False
        self.change_page("TUTORIAL")
