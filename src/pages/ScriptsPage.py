import customtkinter as ctk
from design.Script import Script

from pages.Page import Page
from popups.AddScriptPopup import AddScriptPopup
from utils.remove_from_mapping import remove_from_mapping
from utils.tkinter import ask_for_confirmation
from utils.constants import HORIZONTAL_LINE
from utils.get_available_scripts import get_available_scripts


class ScriptsPage(Page):
    def setup(self):
        self.scripts = get_available_scripts()

        ctk.CTkLabel(self.frame, text="All Scripts").grid(column=1, row=0, columnspan=16)
        ctk.CTkButton(self.frame, text="<", command=lambda: self.change_page("SETTINGS")).grid(column=0, row=0, columnspan=1)
        ctk.CTkButton(self.frame, text="Reset", command=self.reset_scripts).grid(column=17, row=0, columnspan=2)
        ctk.CTkButton(self.frame, text="+", command=self.add_script).grid(column=19, row=0, columnspan=1)

        for i, script in enumerate(self.scripts.values(), start=1):
            ctk.CTkLabel(self.frame, text=HORIZONTAL_LINE).grid(column=0, row=i * 2 - 1, columnspan=20)
            ctk.CTkLabel(self.frame, text=f"{script.name} ({script.nickname}) - #{script.number} / {script.tester_number}").grid(column=0, row=i * 2, columnspan=16, sticky=ctk.W)
            ctk.CTkButton(self.frame, text="Edit", command=lambda script=script: self.add_script(editing=script)).grid(column=15, row=i * 2, columnspan=2)
            ctk.CTkButton(self.frame, text="Delete", command=lambda number=script.number: self.delete_script(number)).grid(column=17, row=i * 2, columnspan=2)

    def add_script(self, *, editing: Script | None = None) -> None:
        AddScriptPopup(self.frame, self.storage, editing, self.reset_page)

    def delete_script(self, number: int) -> None:
        if not ask_for_confirmation("Are you sure?", "If you delete this script you will lose any edits you've made and if you created it, you will lose it forever"):
            return

        with self.storage.edit() as storage:
            storage.deleted_script_numbers.add(number)
            deleted_name = next(s.name for _, s in self.scripts.items() if s.number == number)
            remove_from_mapping(storage.model_defaults, key_condition=lambda key: key.script_name == deleted_name)
        get_available_scripts(self.storage.added_script_infos, self.storage.deleted_script_numbers)
        self.reset_page()

    def reset_scripts(self) -> None:
        if not ask_for_confirmation("Are you sure?", "Resetting the scripts to factory will cause you to lose all the edits, addtitions and deletions that you have made"):
            return

        with self.storage.edit() as storage:
            storage.deleted_script_numbers = set()
        get_available_scripts(deleteds=self.storage.deleted_script_numbers)
        self.reset_page()

    def reset_page(self) -> None:
        self.change_page("SCRIPTS")
