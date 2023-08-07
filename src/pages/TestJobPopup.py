import tkinter
from tkinter import Misc, ttk
from typing import Callable

from design.TestJob import TestJob

class TestJobPopup(tkinter.Toplevel):
    def __init__(self, master: Misc | None, default_dept: str, default_contact: str, master_save_testjob: Callable[[TestJob], None]):
        super().__init__(master)
        self.master_save_testjob = master_save_testjob
        self.title("Add Job")
        maxWidth = self.winfo_screenwidth()
        width = 360
        height = self.winfo_screenheight()
        self.geometry(f"{width}x{height // 2}+{maxWidth - width}+{height // 4}")
        self.attributes("-topmost", 2)  # type: ignore
        self.resizable(False, False)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        ttk.Label(self, text="Department").grid(column=0, row=0)
        self.department = tkinter.StringVar(value=default_dept)
        ttk.Entry(self, textvariable=self.department).grid(column=1, row=0)

        ttk.Label(self, text="Contact Name").grid(column=0, row=1)
        self.contact = tkinter.StringVar(value=default_contact)
        ttk.Entry(self, textvariable=self.contact).grid(column=1, row=1)

        ttk.Label(self, text="Comment").grid(column=0, row=2)
        self.comment = tkinter.Text(self, height=4, width=100)
        self.comment.focus()
        self.comment.grid(column=0, row=3, columnspan=2)

        ttk.Button(self, text="Save", command=self._save_testjob).grid(column=0, row=4, columnspan=2)

    def _save_testjob(self):
        testjob = TestJob(self.department.get(), self.contact.get(), self.comment.get("1.0", tkinter.END))
        self.master_save_testjob(testjob)
        self.destroy()

    