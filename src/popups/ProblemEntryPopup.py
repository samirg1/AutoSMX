from tkinter import Misc
from typing import Callable

import customtkinter as ctk

from db.get_problems import get_problems
from design.Problem import Problem
from popups.OptionSelectPopup import OptionSelectPopup
from popups.Popup import Popup
from utils.tkinter.show_error import show_error


class ProblemEntryPopup(Popup):
    def __init__(self, master: Misc | None, callback: Callable[[Problem], None]) -> None:
        super().__init__(master, "Add Problem", height_factor=0.1, columns=2)
        self.callback = callback

        ctk.CTkLabel(self.pop_frame, text="Problem Number").grid(column=0, row=0)
        number = ctk.StringVar()
        self.entry = ctk.CTkEntry(self.pop_frame, textvariable=number)
        self.entry.grid(column=1, row=0)
        self.after(100, self.entry.focus)

        add_button = ctk.CTkButton(self.pop_frame, text="Add", command=lambda: self._get_problems(number.get()))
        add_button.grid(column=0, row=4, columnspan=2)
        self.entry.bind("<Return>", lambda _: self._get_problems(number.get()))
        self.entry.bind("<Alt-c>", lambda _: self.destroy())

    def _get_problems(self, number: str) -> None:
        problems = get_problems(number)
        if not problems:
            show_error("Invalid number", "No problems found for this PM number")
            self.after(100, self.lift)
            self.after(200, self.entry.focus)
            return
        elif len(problems) == 1:
            return self._exit(problems[0])

        OptionSelectPopup(self, problems, self._exit)

    def _exit(self, problem: Problem) -> None:
        self.callback(problem)
        self.destroy()
