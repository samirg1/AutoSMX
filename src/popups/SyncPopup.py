import os
import sys
import customtkinter as ctk
from tkinter import Misc

from utils.constants import BASE_FILE
from db.presync_check import get_double_ups
from design.Problem import Problem
from popups.Popup import Popup
from utils.connected_to_internet import connected_to_internet
from utils.constants import ERROR_TEXT_COLOUR_LABEL


class SyncPopup(Popup):
    def __init__(self, master: Misc | None, problems: dict[str, Problem]):
        super().__init__(master, "Sync", height_factor=0.8, columns=2)
        row = 0

        for problem in problems.values():
            ctk.CTkLabel(self, text=f"Checking double ups for {problem.number}...").grid(column=0, row=row, columnspan=2, sticky=ctk.W)
            row += 1
            double_ups: dict[str, list[str]] = get_double_ups(problem)
            if not double_ups:
                ctk.CTkLabel(self, text="No double ups found").grid(column=0, row=row, columnspan=2)
                row += 1
            else:
                for title, doubles in double_ups.items():
                    ctk.CTkLabel(self, text=title).grid(column=0, row=row, columnspan=2)
                    row += 1
                    for text in doubles:
                        ctk.CTkLabel(self, text=text).grid(column=0, row=row, columnspan=2, sticky=ctk.W)
                        row += 1

        ctk.CTkButton(self, text="Sync", command=lambda: self._sync(problems)).grid(column=0, row=row, columnspan=2)
        row += 1

        if not connected_to_internet():
            ctk.CTkLabel(self, text="Not connected to internet", text_color=ERROR_TEXT_COLOUR_LABEL).grid(row=row, column=0, columnspan=2)
            row += 1

    def _sync(self, problems: dict[str, Problem]) -> None:
        if sys.platform == "win32":
            with open(rf"{BASE_FILE}\SCMSync.log", "w"):
                ...

            os.startfile("C:\\Program Files (x86)\\SMX\\SCMSync.exe")

        for problem in problems.values():
            problem.sync()

        self.destroy()
