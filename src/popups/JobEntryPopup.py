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
        entry = ttk.Entry(self, textvariable=number)
        entry.grid(column=1, row=0)
        entry.focus()

        add_button = ttk.Button(self, text="Add", command=lambda: self._get_job(number.get()))
        add_button.grid(column=0, row=4, columnspan=2)
        entry.bind("<Return>", lambda _: self._get_job(number.get()))

    def _get_job(self, number: str) -> None:
        self.callback(get_job(number))
        self.destroy()
