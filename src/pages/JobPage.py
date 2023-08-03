from tkinter import ttk
from typing import cast
from design.Job import Job
from pages.Page import Page

class JobPage(Page):
    def setup(self):
        self.jobs = cast(list[Job], self.kwargs["jobs"])

        ttk.Label(self.frame, text="Jobs").grid(column=0, row=0, columnspan=3)
        ttk.Button(self.frame, text="+", command=self.add_job).grid(column=3, row=0)
        ttk.Label(self.frame, text=f"{'-' * 50}").grid(column=0, row=1, columnspan=4)

        self.jobs.append(Job("1234562445", "THORNBURY", "333 Clarendon St", "CAMPEYN"))
        self.jobs.append(Job("1305135091", "BOX HILL", "8 Clota Ave", "BENETAS"))
        self.jobs.append(Job("2838103810", "DONVALE", "9 Deed St", "CAMPEYN"))

        row = 2
        for job in self.jobs:
            ttk.Label(self.frame, text=f"{job}").grid(column=0, row=row, columnspan=3, sticky="w")
            ttk.Button(self.frame, text=">", command=lambda j=job: self.add_tests(j)).grid(column=3, row=row, sticky="e")
            ttk.Button(self.frame, text="X", command=lambda j=job: self.delete_job(j)).grid(column=3, row=row+1, sticky="e")
            row += 2

    def add_job(self):
        ...

    def delete_job(self, job: Job):
        self.jobs.remove(job)
        self.change_page("JOB")

    def add_tests(self, job: Job):
        self.change_page("TEST", job=job)

