from tkinter import StringVar, ttk
import tkinter
# from actions import get_item_job
from design.Item import Item
from design.Job import Job
from design.Test import ScriptError, Test
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
        if not self.job:
            self.job = Job("CAMPEYN", "4812/333 Clarendon St THORNBURY", "THORNBURY")
        self.shared.job = self.job
        self.frame.focus()
        self.test = self.get_test(self.item)
        self.display_test()

    def get_test(self, item: Item) -> Test:
        try:
            return Test(item)
        except ScriptError:
            pass #TODO: Get selection from user

        return Test(item)
    
    def display_test(self):
        ttk.Label(self.frame, text=f"{self.item}").grid(column=0, row=3, columnspan=4)
        ttk.Label(self.frame, text=f"{self.job}").grid(column=0, row=4, columnspan=4)
        ttk.Label(self.frame, text=f"{'-' * 50}").grid(column=0, row=5, columnspan=4)

        script = self.test.script
        ttk.Label(self.frame, text=f"{script.name}").grid(column=0, row=6, columnspan=2)
        self.stest_answers = [StringVar(value=stest.selected) for stest in script.tests]
        for i, stest in enumerate(script.tests):
            ttk.Label(self.frame, text=f"{stest.name}").grid(column=0, row=7+i, columnspan=1, sticky="w")
            for j, option in enumerate(stest.options):
                rb = ttk.Radiobutton(self.frame, text=option, variable=self.stest_answers[i], value=option)
                rb.grid(column=1+j, row=7+i)
                if option == stest.selected:
                    rb.invoke()

        row = 7+len(script.tests)
        self.frame.rowconfigure(row, minsize=10)

        ttk.Button(self.frame, text="Add Job", command=self.add_test_job).grid(column=0, row=row+1, columnspan=4)
        ttk.Label(self.frame, text="Comment").grid(column=0, row=row+2, columnspan=4)

        self.comment = tkinter.Text(self.frame, height=4, width=100)
        self.comment.grid(column=0, row=row+3, columnspan=4)

        self.frame.rowconfigure(row+4, minsize=10)
        ttk.Label(self.frame, text="Result").grid(column=0, row=row+5, columnspan=4)
        self.result = tkinter.StringVar(value="Passed")
        passed = ttk.Radiobutton(self.frame, text="Pass", variable=self.result, value="P")
        passed.grid(column=0, row=row+6)
        passed.invoke()
        ttk.Radiobutton(self.frame, text="Repair", variable=self.result, value="Passed -").grid(column=1, row=row+6)
        ttk.Radiobutton(self.frame, text="Minor", variable=self.result, value="Passed a").grid(column=2, row=row+6)
        ttk.Radiobutton(self.frame, text="Tagged", variable=self.result, value="Faile").grid(column=3, row=row+6)
        ttk.Radiobutton(self.frame, text="Removed", variable=self.result, value="Failed and rem").grid(column=0, row=row+7)
        ttk.Radiobutton(self.frame, text="Untested", variable=self.result, value="Failed and rem").grid(column=1, row=row+7)
        ttk.Radiobutton(self.frame, text="Fail-Unable", variable=self.result, value="Failed and rem").grid(column=2, row=row+7)

        save = ttk.Button(self.frame, text="Save", command=self.save_test)
        save.grid(column=0, row=row+8, columnspan=4)
        self.frame.bind("<Return>", lambda _: save.invoke())
        

    def add_test_job(self):
        ...


    def save_test(self):
        self.test.complete(self.comment.get("1.0", tkinter.END), self.result.get())
        if self.job:
            self.job.add_test(self.test)
        self.change_page("TEST")