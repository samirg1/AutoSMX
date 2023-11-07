from typing import Callable
import customtkinter as ctk
from tkinter import Misc

from db.get_problems import get_problems
from design.Problem import Problem
from popups.OptionSelectPopup import OptionSelectPopup
from popups.Popup import Popup


class ProblemEntryPopup(Popup):
    def __init__(self, master: Misc | None, callback: Callable[[Problem], None]) -> None:
        super().__init__(master, "Add Problem", height_factor=0.1, columns=2)
        self.callback = callback

        ctk.CTkLabel(self, text="Problem Number").grid(column=0, row=0)
        number = ctk.StringVar()
        entry = ctk.CTkEntry(self, textvariable=number)
        entry.grid(column=1, row=0)
        self.after(100, entry.focus)

        add_button = ctk.CTkButton(self, text="Add", command=lambda: self._get_problems(number.get()))
        add_button.grid(column=0, row=4, columnspan=2)
        entry.bind("<Return>", lambda _: self._get_problems(number.get()))
        entry.bind("<Alt-c>", lambda _: self.destroy())

    def _get_problems(self, number: str) -> None:
        problems = get_problems(number)
        if not problems:
            return
        elif len(problems) == 1:
            return self._exit(problems[0])

        OptionSelectPopup(self, problems, self._exit)

    def _exit(self, problem: Problem) -> None:
        self.callback(problem)
        self.destroy()
