from tkinter import Misc
from typing import Callable

import customtkinter as ctk

from utils.get_all_scripts import get_all_scripts
from design.Script import Script
from popups.Popup import Popup
from utils.tkinter import add_focus_bindings


class ScriptSelectionPopup(Popup):
    def __init__(self, master: Misc | None, master_select_script: Callable[[Script], None]) -> None:
        super().__init__(master, "Select Script", columns=2, height_factor=0.5)
        self.focus()
        self.master_select_script = master_select_script
        self.buttons: list[ctk.CTkButton] = []
        for i, script in enumerate(get_all_scripts().values()):
            button = ctk.CTkButton(self.pop_frame, text=script.name, command=lambda script=script: self._select_script(script))  # type: ignore[misc]
            button.grid(column=0, row=i, columnspan=2, sticky=ctk.W)
            add_focus_bindings(button)
            button.bind("<Return>", lambda _, button=button: button.invoke())  # type: ignore[misc]
            self.buttons.append(button)

        if self.buttons:
            self._set_button_focus(0)
        else:
            ctk.CTkLabel(self.pop_frame, text="No scripts added to be used, add some from the settings page.").grid(row=0, column=0)

    def _set_button_focus(self, current: int):
        self.buttons[current - 1].unbind("<Down>")
        self.after(100, self.buttons[current].focus)
        self.buttons[current].bind("<Down>", lambda _: self._set_button_focus((current + 1) % len(self.buttons)))

    def _select_script(self, script: Script) -> None:
        self.master_select_script(script)
        self.destroy()
