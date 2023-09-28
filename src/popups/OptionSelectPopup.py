from tkinter import Misc, ttk
import tkinter
from typing import Callable, TypeVar, Generic
from popups.Popup import Popup

_T = TypeVar("_T")


class OptionSelectPopup(Popup, Generic[_T]):
    def __init__(self, master: Misc | None, options: list[_T], callback: Callable[[_T], None], display: Callable[[_T], str] = str) -> None:
        super().__init__(master, "Select Options", height_factor=0.75, columns=2)
        self.callback = callback

        tree = ttk.Treeview(self, show="tree")
        for row, option in enumerate(options):
            tree.insert("", tkinter.END, f"{row}", text=display(option), open=row == 0)

        scrollbar = ttk.Scrollbar(self, orient=tkinter.VERTICAL, command=tree.yview)  # type: ignore
        tree.configure(yscroll=scrollbar.set)  # type: ignore
        scrollbar.grid(row=0, column=2, sticky=tkinter.NS)
        tree.grid(row=0, column=0, columnspan=2, sticky=tkinter.EW)

        tree.bind("<Return>", lambda _: self._select(options[int(tree.focus())]))
        tree.focus_set()

    def _select(self, option: _T) -> None:
        self.callback(option)
        self.destroy()
