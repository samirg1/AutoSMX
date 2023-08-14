import tkinter
from tkinter import Misc, ttk
from typing import Callable

from design.data import SCRIPTS, Script


class ScriptSelectionPopup(tkinter.Toplevel):
    def __init__(self, master: Misc | None, master_select_script: Callable[[Script], None]):
        super().__init__(master)
        self.master_select_script = master_select_script
        self.title("Select Script")
        maxWidth = self.winfo_screenwidth()
        width = 360
        height = self.winfo_screenheight()
        self.geometry(f"{width}x{height // 4 * 3}+{maxWidth - width}+{height // 8}")
        self.attributes("-topmost", 2)  # type: ignore
        self.resizable(False, False)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        for i, script in enumerate(SCRIPTS.values()):
            ttk.Button(self, text=script.name, command=lambda script=script: self._select_script(script)).grid(column=0, row=i, columnspan=2, sticky="w")  # type: ignore[misc]

    def _select_script(self, script: Script):
        self.master_select_script(script)
        self.destroy()
