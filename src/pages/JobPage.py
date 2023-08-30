import tkinter
from tkinter import ttk

from design.Job import Job
from pages.Page import Page


class JobPage(Page):
    def setup(self):
        # top row
        ttk.Label(self.frame, text="Jobs").grid(column=0, row=0, columnspan=1)
        ttk.Button(self.frame, text="+", width=1, command=self.add_tests).grid(column=1, row=0, columnspan=1)
        ttk.Button(self.frame, text="Tutorial", command=self.tutorial).grid(column=2, row=0, columnspan=1)
        ttk.Button(self.frame, text="Calibrate", command=self.calibrate).grid(column=3, row=0, columnspan=1)
        ttk.Label(self.frame, text=f"{'-' * 50}").grid(column=0, row=1, columnspan=4)

        # job infos
        row = 2
        for job in self.shared.jobs.values():
            # display job
            job_testjobs = self.shared.testjob_manager.job_to_testjobs.get(job, [])
            ttk.Label(self.frame, text=f"{job}").grid(column=0, row=row, columnspan=3, sticky="w")
            ttk.Button(self.frame, text=">", command=lambda j=job: self.add_tests(j)).grid(column=3, row=row, sticky="e")  # type: ignore[misc]
            ttk.Button(self.frame, text="X", command=lambda j=job: self.delete_job(j)).grid(column=3, row=row + 1, sticky="e")  # type: ignore[misc]

            # display job's raised testjobs
            row += 2
            if job_testjobs:
                ttk.Label(self.frame, text="Jobs Raised:").grid(column=0, row=row, columnspan=4)
                row += 1
            for testjob in job_testjobs:
                item = self.shared.testjob_manager.testjob_to_item[testjob]
                first_line = str(testjob).split("\n")[0]
                ttk.Label(
                    self.frame,
                    text=f"-> {item.description.split(' ')[0]} ({item.number}): {first_line}",
                ).grid(column=0, row=row, columnspan=4, sticky="w")
                row += 1

            # display job's tests
            if job.tests:
                columns = (f"Tests ({len(job.tests)})", "#")
                column_names = [f"#{i+1}" for i in range(len(columns))]
                tree = ttk.Treeview(self.frame, columns=column_names, height=3, selectmode=tkinter.NONE, show="headings")
                for i, column in enumerate(columns, start=1):
                    if i == 1:
                        tree.column(f"#{i}", anchor=tkinter.W)
                    else:
                        tree.column(f"#{i}", width=100, anchor=tkinter.CENTER)
                    tree.heading(f"#{i}", text=column)

                for script_name, value in job.test_breakdown.items():
                    tree.insert("", tkinter.END, values=(script_name, value))

                scrollbar = ttk.Scrollbar(self.frame, orient=tkinter.VERTICAL, command=tree.yview)  # type: ignore
                tree.configure(yscroll=scrollbar.set)  # type: ignore
                scrollbar.grid(row=row, column=4, sticky=tkinter.NS)

                tree.grid(column=0, row=row, columnspan=4)
                row += 1

            #     ttk.Label(self.frame, text=f"Tests ({len(job.tests)})").grid(column=0, row=row, columnspan=4)
            #     row += 1
            # for script_name, value in job.test_breakdown.items():
            #     ttk.Label(self.frame, text=f"-> {script_name}: {value}").grid(column=0, row=row, columnspan=4, sticky="w")
            #     row += 1

            ttk.Label(self.frame, text=f"{'-' * 60}").grid(column=0, row=row, columnspan=4)
            row += 1

    def delete_job(self, job: Job) -> None:
        del self.shared.jobs[job.campus]
        self.change_page("JOB")

    def add_tests(self, job: Job | None = None) -> None:
        self.shared.job = job
        self.change_page("TEST")

    def calibrate(self):
        with self.shared.storage.edit() as storage:
            storage.calibrated = False
        self.change_page("CALIBRATION")

    def tutorial(self):
        with self.shared.storage.edit() as storage:
            storage.tutorial_complete = False
        self.change_page("TUTORIAL")
