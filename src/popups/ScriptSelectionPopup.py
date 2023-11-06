from typing import Callable
import customtkinter as ctk
from tkinter import Misc

from design.data import get_all_scripts
from design.Script import Script
from popups.Popup import Popup


class ScriptSelectionPopup(Popup):
    def __init__(self, master: Misc | None, master_select_script: Callable[[Script], None]) -> None:
        super().__init__(master, "Select Script", columns=2, height_factor=0.2)
        self.focus()
        self.master_select_script = master_select_script
        for i, script in enumerate(get_all_scripts().values()):
            ctk.CTkButton(self, text=script.name, command=lambda script=script: self._select_script(script)).grid(column=0, row=i, columnspan=2, sticky="w")  # type: ignore[misc]

    def _select_script(self, script: Script) -> None:
        self.master_select_script(script)
        self.destroy()
