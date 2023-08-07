import tkinter
from tkinter import StringVar, ttk
from typing import cast

from actions import complete_test, get_item_job
from design.Item import Item
from design.data import Script
from design.Job import Job
from design.Test import ScriptError, Test
from design.TestJob import TestJob
from pages.Page import Page
from pages.ScriptSelectionPopup import ScriptSelectionPopup
from pages.TestJobPopup import TestJobPopup


class TestPage(Page):
    def setup(self):
        ttk.Button(self.frame, text="Back", command=lambda: self.change_page("JOB")).grid(column=0, row=0, sticky="w")

        ttk.Label(self.frame, text="Item Number").grid(column=0, row=1, columnspan=2)
        item_number = tkinter.StringVar()
        item_entry = ttk.Entry(self.frame, textvariable=item_number)
        item_entry.grid(column=2, row=1, sticky="w", columnspan=2)
        item_entry.focus()
        item_entry.bind("<Return>", lambda _: self.get_item(item_number, item_entry))
        self.go_button = ttk.Button(self.frame, text="Go", command=lambda: self.get_item(item_number, item_entry))
        self.go_button.grid(column=0, row=2, columnspan=4)

    def get_item(self, item_number: StringVar, item_entry: ttk.Entry) -> None:
        item_entry.state(["disabled"])  # type: ignore
        self.frame.focus()
        item, self.shared.job = get_item_job(item_number.get(), self.shared.assets_position, self.shared.testing_position, self.shared.jobs, self.shared.job)
        self.shared.jobs[self.shared.job.campus] = self.shared.job
        self.get_test(item)

    def get_test(self, item: Item):
        test = Test(item)
        try:
            test.set_script()
            self.display_test(test)
        except ScriptError:
            ScriptSelectionPopup(self.frame, lambda s: self.set_script(s, test)).mainloop()

    def set_script(self, script: Script, test: Test):
        test.set_script(script)
        self.display_test(test)

    def display_test(self, test: Test):
        self.test = test
        self.go_button.configure(text="Cancel", command=lambda: self.change_page("TEST"))
        ttk.Label(self.frame, text=f"{test.item}").grid(column=0, row=3, columnspan=4)
        ttk.Label(self.frame, text=f"{cast(Job, self.shared.job).campus}").grid(column=0, row=4, columnspan=4)
        ttk.Label(self.frame, text=f"{'-' * 50}").grid(column=0, row=5, columnspan=4)

        row, script_answers = self.display_script(test.script, 6)

        self.add_job_button = ttk.Button(self.frame, text="Add Job", command=self.add_testjob)
        self.add_job_button.grid(column=0, row=row, columnspan=4)
        row += 1

        ttk.Label(self.frame, text="Comment").grid(column=0, row=row, columnspan=4)
        row += 1
        self.comment = tkinter.Text(self.frame, height=4, width=100)
        self.comment.grid(column=0, row=row, columnspan=4)
        row += 1
        self.frame.rowconfigure(row, minsize=10)

        row += 1
        ttk.Label(self.frame, text="Result").grid(column=0, row=row, columnspan=4)
        row += 1
        result = tkinter.StringVar(value="Passed")
        passed = ttk.Radiobutton(self.frame, text="Pass", variable=result, value="P")
        passed.grid(column=0, row=row)
        passed.invoke()
        ttk.Radiobutton(self.frame, text="Defect", variable=result, value="Passed -").grid(column=1, row=row)
        ttk.Radiobutton(self.frame, text="Repaired", variable=result, value="Passed a").grid(column=2, row=row)
        ttk.Radiobutton(self.frame, text="Tagged", variable=result, value="Faile").grid(column=3, row=row)
        row += 1
        ttk.Radiobutton(self.frame, text="Removed", variable=result, value="Failed and rem").grid(column=0, row=row)
        ttk.Radiobutton(self.frame, text="Untested", variable=result, value="N").grid(column=1, row=row)
        ttk.Radiobutton(self.frame, text="Fail-Unable", variable=result, value="F").grid(column=2, row=row)
        row += 1

        save = ttk.Button(self.frame, text="Save", command=lambda: self.save_test([s.get() for s in script_answers], result.get()))
        save.grid(column=0, row=row, columnspan=4)
        row += 1

        self.frame.master.bind("<Return>", lambda _: save.invoke())
        self.comment.bind("<FocusIn>", lambda _: self.frame.master.unbind("<Return>"))
        self.comment.bind("<FocusOut>", lambda _: self.frame.master.bind("<Return>", lambda _: save.invoke()))

    def display_script(self, script: Script, row: int):
        row = 6
        script = self.test.script
        ttk.Label(self.frame, text=f"{script.name}").grid(column=0, row=row, columnspan=4)
        row += 1
        script_answers = [StringVar(value=stest.selected) for stest in script.tests]
        for i, stest in enumerate(script.tests):
            ttk.Label(self.frame, text=f"{stest.name}").grid(column=0, row=row, columnspan=1, sticky="w")
            if not stest.options:
                ttk.Entry(self.frame, textvariable=script_answers[i]).grid(column=1, row=row, columnspan=3, sticky="w")
            for j, option in enumerate(stest.options):
                rb = ttk.Radiobutton(self.frame, text=option, variable=script_answers[i], value=option)
                rb.grid(column=1 + j, row=row)
                if option == stest.selected:
                    rb.invoke()
            row += 1
        self.frame.rowconfigure(row, minsize=10)
        ttk.Label(self.frame, text=f"{'-' * 50}").grid(column=0, row=row, columnspan=4)
        row += 1
        return row, script_answers

    def add_testjob(self):
        assert self.shared.job is not None
        testjob_popup = TestJobPopup(self.frame, self.shared.job.department, self.shared.job.company, self.save_testjob)
        testjob_popup.mainloop()

    def save_testjob(self, testjob: TestJob):
        self.comment.insert(tkinter.END, ("\n" if self.test.testjobs else "") + testjob.comment)
        self.test.add_testjob(testjob)
        self.shared.testjob_manager.add_testjob(self.test.item, cast(Job, self.shared.job), testjob)
        self.add_job_button.configure(text=f"Add Job ({len(self.test.testjobs)})")

    def save_test(self, script_answers: list[str], result: str):
        comment = self.comment.get("1.0", tkinter.END)
        self.test.complete(comment if comment != "\n" else "", result, script_answers)
        if self.shared.job:
            self.shared.job.add_test(self.test)

        complete_test(self.test, self.shared.area_position, self.shared.comments_position)
        self.change_page("TEST")
