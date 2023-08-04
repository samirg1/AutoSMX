import tkinter
from tkinter import StringVar, ttk
from typing import cast

# from actions import complete_test, get_item_job
from design.Item import Item
from design.Job import Job
from design.Test import ScriptError, Test
from design.TestJob import TestJob
from pages.Page import Page


class TestPage(Page):
    def setup(self):
        ttk.Button(self.frame, text="Back", command=lambda: self.change_page("JOB")).grid(column=0, row=0, sticky="w")

        ttk.Label(self.frame, text="Item Number").grid(column=0, row=1, columnspan=2)
        self.item_number = tkinter.StringVar()
        self.entry = ttk.Entry(self.frame, textvariable=self.item_number)
        self.entry.grid(column=2, row=1, sticky="w", columnspan=2)
        self.entry.focus()
        self.entry.bind("<Return>", lambda _: self.get_item())
        ttk.Button(self.frame, text="Go", command=self.get_item).grid(column=0, row=2, columnspan=4)

    def get_item(self):
        # self.item, self.job = get_item_job(self.item_number.get(), self.assets_position, self.testing_position, self.job)
        self.item = Item(self.item_number.get(), "BED", "Model", "Manufacturer", "None", "None", "123456")
        if not self.shared.job:
            self.shared.job = Job("CAMPEYN", "4812/333 Clarendon St THORNBURY", "THORNBURY")

        self.shared.jobs[self.shared.job.campus] = self.shared.job
        self.frame.focus()
        self.test = self.get_test(self.item)
        self.display_test()

    def get_test(self, item: Item) -> Test:
        try:
            return Test(item)
        except ScriptError:
            pass  # TODO: Get selection from user

        return Test(item)

    def display_test(self):
        ttk.Label(self.frame, text=f"{self.item}").grid(column=0, row=3, columnspan=4)
        ttk.Label(self.frame, text=f"{self.shared.job}").grid(column=0, row=4, columnspan=4)
        ttk.Label(self.frame, text=f"{'-' * 50}").grid(column=0, row=5, columnspan=4)

        script = self.test.script
        ttk.Label(self.frame, text=f"{script.name}").grid(column=0, row=6, columnspan=2)
        self.stest_answers = [StringVar(value=stest.selected) for stest in script.tests]
        for i, stest in enumerate(script.tests):
            ttk.Label(self.frame, text=f"{stest.name}").grid(column=0, row=7 + i, columnspan=1, sticky="w")
            for j, option in enumerate(stest.options):
                rb = ttk.Radiobutton(self.frame, text=option, variable=self.stest_answers[i], value=option)
                rb.grid(column=1 + j, row=7 + i)
                if option == stest.selected:
                    rb.invoke()

        row = 7 + len(script.tests)
        self.frame.rowconfigure(row, minsize=10)

        ttk.Button(self.frame, text="Add Job", command=self.add_testjob).grid(column=0, row=row + 1, columnspan=4)
        row += 1
        self.job_start_row = row + 1
        row += 9
        ttk.Label(self.frame, text="Comment").grid(column=0, row=row, columnspan=4)
        row += 1

        self.comment = tkinter.Text(self.frame, height=4, width=100)
        self.comment.grid(column=0, row=row, columnspan=4)
        row += 1

        self.frame.rowconfigure(row, minsize=10)
        row += 1
        ttk.Label(self.frame, text="Result").grid(column=0, row=row, columnspan=4)
        row += 1
        self.result = tkinter.StringVar(value="Passed")
        passed = ttk.Radiobutton(self.frame, text="Pass", variable=self.result, value="P")
        passed.grid(column=0, row=row)
        passed.invoke()
        ttk.Radiobutton(self.frame, text="Repair", variable=self.result, value="Passed -").grid(column=1, row=row)
        ttk.Radiobutton(self.frame, text="Minor", variable=self.result, value="Passed a").grid(column=2, row=row)
        ttk.Radiobutton(self.frame, text="Tagged", variable=self.result, value="Faile").grid(column=3, row=row)
        row += 1
        ttk.Radiobutton(self.frame, text="Removed", variable=self.result, value="Failed and rem").grid(column=0, row=row)
        ttk.Radiobutton(self.frame, text="Untested", variable=self.result, value="Failed and rem").grid(column=1, row=row)
        ttk.Radiobutton(self.frame, text="Fail-Unable", variable=self.result, value="Failed and rem").grid(column=2, row=row)
        row += 1

        save = ttk.Button(self.frame, text="Save", command=self.save_test)
        save.grid(column=0, row=row, columnspan=4)
        row += 1
        self.frame.bind("<Return>", lambda _: save.invoke())

    def add_testjob(self):
        assert self.shared.job is not None

        window = tkinter.Toplevel(self.frame)
        window.title("Add Job")
        maxWidth = window.winfo_screenwidth()
        width = 360
        height = window.winfo_screenheight()
        window.geometry(f"{width}x{height // 2}+{maxWidth - width}+{height // 4}")
        window.attributes("-topmost", 2)  # type: ignore
        window.resizable(False, False)

        window.columnconfigure(0, weight=1)
        window.columnconfigure(1, weight=1)

        ttk.Label(window, text="Department").grid(column=0, row=0)
        department = tkinter.StringVar(value=self.shared.job.department)
        ttk.Entry(window, textvariable=department).grid(column=1, row=0)

        ttk.Label(window, text="Contact Name").grid(column=0, row=1)
        contact = tkinter.StringVar(value=self.shared.job.company)
        ttk.Entry(window, textvariable=contact).grid(column=1, row=1)

        ttk.Label(window, text="Comment").grid(column=0, row=2)
        comment = tkinter.Text(window, height=4, width=100)
        comment.focus()
        comment.grid(column=0, row=3, columnspan=2)

        ttk.Button(window, text="Save", command=lambda: self.save_testjob(window, department.get(), contact.get(), comment.get("1.0", tkinter.END))).grid(column=0, row=4, columnspan=2)

        window.mainloop()

    def save_testjob(self, window: tkinter.Toplevel, department: str, contact: str, comment: str):
        self.comment.insert(tkinter.END, ("\n" if self.test.testjobs else "") + comment)
        testjob = TestJob(department, contact, comment)
        self.test.add_testjob(testjob)
        self.shared.testjob_manager.add_testjob(self.item, cast(Job, self.shared.job), testjob)
        window.destroy()

        if len(self.test.testjobs) == 1:
            ttk.Label(self.frame, text=f"Jobs").grid(column=0, row=self.job_start_row, columnspan=4)
            self.job_start_row += 1

        ttk.Label(self.frame, text=f"{len(self.test.testjobs)}").grid(column=0, row=self.job_start_row, rowspan=3)
        ttk.Label(self.frame, text=f"{testjob}").grid(column=1, row=self.job_start_row, columnspan=3, rowspan=3)
        self.job_start_row += 3

    def save_test(self):
        self.test.complete(self.comment.get("1.0", tkinter.END), self.result.get(), [s.get() for s in self.stest_answers])
        if self.shared.job:
            self.shared.job.add_test(self.test)

        # complete_test(self.test, self.shared.area_position, self.shared.comments_position)
        self.change_page("TEST")
