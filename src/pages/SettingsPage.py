import tkinter
from tkinter import ttk

from pages.Page import Page


class SettingsPage(Page):
    def setup(self) -> None:
        ttk.Button(self.frame, text="<", command=lambda: self.change_page("PROBLEM")).grid(column=0, row=0, columnspan=1)
        ttk.Label(self.frame, text="Settings").grid(column=1, row=0, columnspan=3, sticky=tkinter.NSEW)
        ttk.Label(self.frame, text=f"{'-' * 50}").grid(column=0, row=1, columnspan=4)
        ttk.Button(self.frame, text="View Tutorial >", command=self.tutorial).grid(column=0, row=2, sticky=tkinter.W)
        ttk.Button(self.frame, text="Recalibrate >", command=self.calibrate).grid(column=0, row=3, sticky=tkinter.W)

    def calibrate(self) -> None:
        with self.shared.storage.edit() as storage:
            storage.calibrated = False
        self.change_page("CALIBRATION")

    def tutorial(self) -> None:
        with self.shared.storage.edit() as storage:
            storage.tutorial_complete = False
        self.change_page("TUTORIAL")
