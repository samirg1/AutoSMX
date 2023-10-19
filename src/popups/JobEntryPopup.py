from tkinter import Misc, StringVar, ttk
from typing import Callable

from db.get_items_jobs import get_jobs
from design.Job import Job
from popups.OptionSelectPopup import OptionSelectPopup
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

        add_button = ttk.Button(self, text="Add", command=lambda: self._get_jobs(number.get()))
        add_button.grid(column=0, row=4, columnspan=2)
        entry.bind("<Return>", lambda _: self._get_jobs(number.get()))

    def _get_jobs(self, number: str) -> None:
        jobs = get_jobs(number)
        if not jobs:
            return
        elif len(jobs) == 1:
            return self._exit(jobs[0])

        OptionSelectPopup(self, jobs, self._exit)

    def _exit(self, job: Job) -> None:
        self.callback(job)
        self.destroy()
