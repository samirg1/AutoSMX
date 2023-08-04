from tkinter import ttk

from design.Job import Job
from pages.Page import Page


class JobPage(Page):
    def setup(self):
        ttk.Label(self.frame, text="Jobs").grid(column=0, row=0, columnspan=3)
        ttk.Label(self.frame, text=f"{'-' * 50}").grid(column=0, row=1, columnspan=4)

        row = 2
        for job in self.shared.jobs.values():
            ttk.Label(self.frame, text=f"{job}").grid(column=0, row=row, columnspan=3, sticky="w")
            ttk.Button(self.frame, text=">", command=lambda j=job: self.add_tests(j)).grid(column=3, row=row, sticky="e")
            ttk.Button(self.frame, text="X", command=lambda j=job: self.delete_job(j)).grid(column=3, row=row + 1, sticky="e")
            row += 2

    def delete_job(self, job: Job):
        del self.shared.jobs[job.campus]
        self.change_page("JOB")

    def add_tests(self, job: Job):
        self.shared.job = job
        self.change_page("TEST")
