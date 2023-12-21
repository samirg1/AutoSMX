import customtkinter as ctk

from pages.Page import Page
from pages.ProblemPage import ProblemPage
from pages.ScriptsPage import ScriptsPage
from pages.SettingsPage import SettingsPage
from pages.TestPage import TestPage
from pages.TutorialPage import TutorialPage
from storage.Storage import Storage
from utils.constants import APP_GEOMETRY, APP_NAME, PAGE_NAMES, ImmutableDict
from utils.get_available_scripts import get_available_scripts
from utils.tkinter import set_icon


class App(ctk.CTk):
    def __init__(self) -> None:
        super().__init__()

        self.geometry(APP_GEOMETRY)
        self.title(APP_NAME)
        set_icon(self)

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        storage = Storage()
        with storage.edit():
            for info in storage.added_script_infos:
                if info.number in storage.deleted_script_numbers:
                    storage.added_script_infos.remove(info)
        get_available_scripts(storage.added_script_infos, storage.deleted_script_numbers)

        self.frame = ctk.CTkScrollableFrame(self)
        for i in range(20):
            self.frame.columnconfigure(i, weight=1)
        self.frame.grid(row=0, column=0, sticky=ctk.NSEW)

        pages: set[tuple[PAGE_NAMES, type[Page]]] = {
            ("TUTORIAL", TutorialPage),
            ("SETTINGS", SettingsPage),
            ("SCRIPTS", ScriptsPage),
            ("PROBLEM", ProblemPage),
            ("TEST", TestPage),
        }
        self.pages: ImmutableDict[PAGE_NAMES, Page] = {name: page(self.frame, self.change_page, storage) for name, page in pages}
        self.current_page: Page | None = None

        self.change_page("TUTORIAL")

    def change_page(self, page: PAGE_NAMES) -> None:
        if self.current_page is not None:
            for widget in self.current_page.frame.winfo_children():
                widget.destroy()

        self.current_page = self.pages[page]
        self.current_page.setup()


def main() -> None:
    App().mainloop()


if __name__ == "__main__":
    main()
