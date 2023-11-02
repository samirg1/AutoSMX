from tkinter import END, Misc, StringVar, Text, ttk
from typing import Callable

from design.Job import Job
from popups.Popup import Popup


class JobPopup(Popup):
    def __init__(self, master: Misc | None, default_dept: str, default_contact: str, save_job: Callable[[Job], None]):
        super().__init__(master, "Add Job", height_factor=0.5, columns=2)
        self.save_job = save_job

        ttk.Label(self, text="Department").grid(column=0, row=0)
        department = StringVar(value=default_dept)
        ttk.Entry(self, textvariable=department).grid(column=1, row=0)

        ttk.Label(self, text="Contact Name").grid(column=0, row=1)
        contact = StringVar(value=default_contact)
        ttk.Entry(self, textvariable=contact).grid(column=1, row=1)

        ttk.Label(self, text="Comment").grid(column=0, row=2)
        comment = Text(self, height=4, width=100)
        comment.focus()
        comment.grid(column=0, row=3, columnspan=2)

        tkinter.Button(self, text="Save", command=lambda: self._save_job(department.get(), contact.get(), comment.get("1.0", END))).grid(column=0, row=4, columnspan=2)

    def _save_job(self, department: str, contact: str, comment: str) -> None:
        self.save_job(Job(department, contact, comment))
        self.destroy()
