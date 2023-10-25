import os
from tkinter import Misc, ttk

from db.get_connection import BASE_FILE
from db.presync_check import get_double_ups
from design.Problem import Problem
from popups.Popup import Popup


class SyncPopup(Popup):
    def __init__(self, master: Misc | None, problem: Problem | None):
        super().__init__(master, "Sync", height_factor=0.8, columns=2)
        row = 0

        if problem is None:
            return self._sync()

        ttk.Label(self, text="Checking double ups...").grid(column=0, row=row, columnspan=2, sticky="W")
        row += 1
        double_ups: dict[str, list[str]] = get_double_ups(problem)
        if not double_ups:
            ttk.Label(self, text="No double ups found").grid(column=0, row=row, columnspan=2)
            row += 1
        else:
            for title, doubles in double_ups.items():
                ttk.Label(self, text=title).grid(column=0, row=row, columnspan=2)
                row += 1
                for text in doubles:
                    ttk.Label(self, text=text).grid(column=0, row=row, columnspan=2, sticky="W")
                    row += 1

        ttk.Button(self, text="Sync", command=self._sync).grid(column=0, row=row, columnspan=2)
        row += 1

    def _sync(self) -> None:
        with open(rf"{BASE_FILE}\SCMSync.log", "w"):
            ...

        os.startfile("C:\\Program Files (x86)\\SMX\\SCMSync.exe")
        self.destroy()
