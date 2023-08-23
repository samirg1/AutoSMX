from tkinter import Misc, ttk
from typing import Callable

from design.data import SCRIPTS
from design.Script import Script
from popups.Popup import Popup


class ScriptSelectionPopup(Popup):
    def __init__(self, master: Misc | None, master_select_script: Callable[[Script], None]):
        super().__init__(master, "Select Script", columns=2)
        self.master_select_script = master_select_script
        for i, script in enumerate(SCRIPTS.values()):
            ttk.Button(self, text=script.name, command=lambda script=script: self._select_script(script)).grid(column=0, row=i, columnspan=2, sticky="w")  # type: ignore[misc]

    def _select_script(self, script: Script):
        self.master_select_script(script)
        self.destroy()
