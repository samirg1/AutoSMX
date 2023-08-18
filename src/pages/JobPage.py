from tkinter import ttk
from typing import Optional

from design.Job import Job
from pages.Page import Page


class JobPage(Page):
    def setup(self):
        ttk.Label(self.frame, text="Jobs").grid(column=0, row=0, columnspan=2)
        ttk.Button(self.frame, text="+", command=lambda: self.add_tests()).grid(column=2, row=0, columnspan=1)
        ttk.Button(self.frame, text="Calibrate", command=self.calibrate).grid(column=3, row=0, columnspan=1)
        ttk.Label(self.frame, text=f"{'-' * 50}").grid(column=0, row=1, columnspan=4)

        row = 2
        for job in self.shared.jobs.values():
            job_testjobs = self.shared.testjob_manager.job_to_testjobs.get(job, [])
            ttk.Label(self.frame, text=f"{job}").grid(column=0, row=row, columnspan=3, sticky="w")
            ttk.Button(self.frame, text=">", command=lambda j=job: self.add_tests(j)).grid(column=3, row=row, sticky="e")  # type: ignore[misc]
            ttk.Button(self.frame, text="X", command=lambda j=job: self.delete_job(j)).grid(column=3, row=row + 1, sticky="e")  # type: ignore[misc]

            row += 2
            if job_testjobs:
                ttk.Label(self.frame, text="Jobs Raised:").grid(column=0, row=row, columnspan=4)
                row += 1
            for testjob in job_testjobs:
                item = self.shared.testjob_manager.testjob_to_item[testjob]
                first_line = str(testjob).split("\n")[0]
                ttk.Label(
                    self.frame,
                    text=f"-> {item.description} ({item.number}): {first_line}",
                ).grid(column=0, row=row, columnspan=4, sticky="w")
                row += 1

            if job.tests:
                ttk.Label(self.frame, text=f"Tests ({len(job.tests)})").grid(column=0, row=row, columnspan=4)
                row += 1
            for script_name, value in job.test_breakdown.items():
                ttk.Label(self.frame, text=f"-> {script_name}: {value}").grid(column=0, row=row, columnspan=4, sticky="w")
                row += 1

    def delete_job(self, job: Job) -> None:
        del self.shared.jobs[job.campus]
        self.change_page("JOB")

    def add_tests(self, job: Optional[Job] = None) -> None:
        self.shared.job = job
        self.change_page("TEST")

    def calibrate(self):
        with self.shared.storage.edit() as storage:
            storage.positions_set = False
        self.change_page("START")
