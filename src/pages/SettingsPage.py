import customtkinter as ctk

from pages.Page import Page
from popups.AddScriptPopup import AddScriptPopup
from utils.constants import HORIZONTAL_LINE


class SettingsPage(Page):
    def setup(self) -> None:
        ctk.CTkButton(self.frame, text="<", command=lambda: self.change_page("PROBLEM")).grid(column=0, row=0, columnspan=1)
        ctk.CTkLabel(self.frame, text="Settings").grid(column=1, row=0, columnspan=3, sticky=ctk.NSEW)
        ctk.CTkLabel(self.frame, text=HORIZONTAL_LINE).grid(column=0, row=1, columnspan=4)
        ctk.CTkButton(self.frame, text="View Tutorial >", command=self.tutorial).grid(column=0, row=2, sticky=ctk.W)
        ctk.CTkButton(self.frame, text="Add Script >", command=self.add_script).grid(column=0, row=3, sticky=ctk.W)

    def tutorial(self) -> None:
        with self.storage.edit() as storage:
            storage.tutorial_complete = False
        self.change_page("TUTORIAL")

    def add_script(self) -> None:
        AddScriptPopup(self.frame, self.storage).mainloop()