import customtkinter as ctk
import tkinter
from typing import Callable

from design.Job import Job
from popups.Popup import Popup


class JobPopup(Popup):
    def __init__(self, master: tkinter.Misc | None, default_dept: str, default_contact: str, save_job: Callable[[Job], None]):
        super().__init__(master, "Add Job", height_factor=0.5, columns=2)
        self.save_job = save_job

        ctk.CTkLabel(self, text="Department").grid(column=0, row=0)
        department = ctk.StringVar(value=default_dept)
        ctk.CTkEntry(self, textvariable=department).grid(column=1, row=0)

        ctk.CTkLabel(self, text="Contact Name").grid(column=0, row=1)
        contact = ctk.StringVar(value=default_contact)
        ctk.CTkEntry(self, textvariable=contact).grid(column=1, row=1)

        ctk.CTkLabel(self, text="Comment").grid(column=0, row=2)
        comment = tkinter.Text(self, height=4, width=100)
        self.after(100, comment.focus)
        comment.grid(column=0, row=3, columnspan=2)

        save_button = ctk.CTkButton(self, text="Save", command=lambda: self._save_job(department.get(), contact.get(), comment.get("1.0", ctk.END)))
        save_button.grid(column=0, row=4, columnspan=2)

        comment.bind("<Alt-s>", lambda _: save_button.invoke())
        comment.bind("<Alt-c>", lambda _: self.destroy())

    def _save_job(self, department: str, contact: str, comment: str) -> None:
        self.save_job(Job(department, contact, comment))
        self.destroy()
