from tkinter import END, Misc, Text
from typing import Any

from utils.constants import CTK_TEXT_START


class UppercaseText(Text):
    def __init__(self, master: Misc | None, *args: Any, **kwargs: Any) -> None:
        super().__init__(master, *args, **kwargs)
        self.bind("<FocusOut>", lambda _: self.set_uppercase())

    def set_uppercase(self) -> None:
        old = self.get(CTK_TEXT_START, END)
        self.delete(CTK_TEXT_START, END)
        self.insert(CTK_TEXT_START, old.upper())
