from tkinter import Misc
from typing import Callable, Generic, TypeVar

import customtkinter as ctk

from popups.Popup import Popup
from utils.constants import OPTION_SELECT_POPUP_WIDTH

_T = TypeVar("_T")


class OptionSelectPopup(Popup, Generic[_T]):
    def __init__(self, master: Misc | None, options: list[_T], callback: Callable[[_T], None], display: Callable[[_T], str] = str, *, width: int = OPTION_SELECT_POPUP_WIDTH) -> None:
        super().__init__(master, "Select Options", height_factor=0.75, columns=4, width=width)
        self._callback = callback

        for row, option in enumerate(options):
            ctk.CTkButton(self.pop_frame, text=display(option), command=lambda option=option: self._select(option)).grid(row=row, column=0, sticky=ctk.W)  # type: ignore[misc]

    def _select(self, option: _T) -> None:
        self._callback(option)
        self.destroy()
