from tkinter import Misc, StringVar, ttk
from typing import Callable
from design.Job import Job
from gui.db_functions import get_job
from popups.Popup import Popup


class JobEntryPopup(Popup):
    def __init__(self, master: Misc | None, callback: Callable[[Job], None]) -> None:
        super().__init__(master, "Add Job", height_factor=0.5, columns=2)
        self.callback = callback

        ttk.Label(self, text="Job Number").grid(column=0, row=0)
        number = StringVar()
        ttk.Entry(self, textvariable=number).grid(column=1, row=0)

        ttk.Button(self, text="Add", command=lambda: self._get_job(number.get())).grid(column=0, row=4, columnspan=2)

    def _get_job(self, number: str) -> None:
        self.callback(get_job(number))
        self.destroy()
