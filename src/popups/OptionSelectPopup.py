from tkinter import Misc, ttk, W
from typing import Callable, TypeVar, Generic
from popups.Popup import Popup

_T = TypeVar("_T")


class OptionSelectPopup(Popup, Generic[_T]):
    def __init__(self, master: Misc | None, options: list[_T], callback: Callable[[_T], None], display: Callable[[_T], str] = str) -> None:
        super().__init__(master, "Select Options", height_factor=0.5, columns=2)
        self.callback = callback

        for row, option in enumerate(options):
            ttk.Label(self, text=display(option)).grid(column=0, row=row, sticky=W)
            ttk.Button(self, text="Select", command=lambda option=option: self._select(option)).grid(column=1, row=row)

    def _select(self, option: _T) -> None:
        self.callback(option)
        self.destroy()
