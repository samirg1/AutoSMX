import os
import sys
from tkinter import Misc

import customtkinter as ctk

from db.presync_check import get_double_ups
from design.Problem import Problem
from popups.Popup import Popup
from utils.connected_to_internet import connected_to_internet
from utils.constants import ERROR_TEXT_COLOUR_LABEL, SYNC_EXECUTABLE_PATH, SYNC_LOG_PATH


class SyncPopup(Popup):
    def __init__(self, master: Misc | None, problems: dict[str, Problem]):
        super().__init__(master, "Sync", height_factor=0.8, columns=2)
        row = 0

        for problem in problems.values():
            ctk.CTkLabel(self.pop_frame, text=f"Checking double ups for {problem.number}...").grid(column=0, row=row, columnspan=2, sticky=ctk.W)
            row += 1
            double_ups: dict[str, list[str]] = get_double_ups(problem)
            if not double_ups:
                ctk.CTkLabel(self.pop_frame, text="No double ups found").grid(column=0, row=row, columnspan=2)
                row += 1
            else:
                for title, doubles in double_ups.items():
                    ctk.CTkLabel(self.pop_frame, text=title).grid(column=0, row=row, columnspan=2)
                    row += 1
                    for text in doubles:
                        ctk.CTkLabel(self.pop_frame, text=text).grid(column=0, row=row, columnspan=2, sticky=ctk.W)
                        row += 1

        ctk.CTkButton(self.pop_frame, text="Sync", command=lambda: self._sync(problems)).grid(column=0, row=row, columnspan=2)
        row += 1

        if not connected_to_internet():
            ctk.CTkLabel(self.pop_frame, text="Not connected to internet", text_color=ERROR_TEXT_COLOUR_LABEL).grid(row=row, column=0, columnspan=2)
            row += 1

    def _sync(self, problems: dict[str, Problem]) -> None:
        if sys.platform == "win32":
            SYNC_LOG_PATH.write_text("")
            os.startfile(SYNC_EXECUTABLE_PATH)

        for problem in problems.values():
            problem.sync()

        self.destroy()
