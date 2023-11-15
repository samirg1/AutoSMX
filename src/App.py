import customtkinter as ctk

from design.data import CONDITION_LINES, LINE_DEFAULTS, NON_PERSISTENT_LINES, REQUIRED_FREE_TEXT_FIELDS, SCRIPT_INFOS
from pages.Page import Page
from pages.ProblemPage import ProblemPage
from pages.SettingsPage import SettingsPage
from pages.TestPage import TestPage
from pages.TutorialPage import TutorialPage
from storage.Storage import Storage
from utils.constants import ICON_PATH, PAGE_NAMES


class App(ctk.CTk):
    def __init__(self) -> None:
        super().__init__()
        self.geometry(f"1500x750+10+10")
        self.title("AutoSMX")

        self.after(201, lambda: self.iconbitmap(ICON_PATH))  # pyright: ignore

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        storage = Storage()
        for info, condition, defaults, requireds, non_persistents in storage.added_scripts:
            SCRIPT_INFOS.append(info)
            if condition is not None:
                CONDITION_LINES.add(condition)
            LINE_DEFAULTS.update(defaults)
            REQUIRED_FREE_TEXT_FIELDS.update(requireds)
            NON_PERSISTENT_LINES.update(non_persistents)

        self.pages: dict[PAGE_NAMES, Page] = {
            "TUTORIAL": TutorialPage(self._frame(), self.change_page, storage),
            "SETTINGS": SettingsPage(self._frame(), self.change_page, storage),
            "PROBLEM": ProblemPage(self._frame(), self.change_page, storage),
            "TEST": TestPage(self._frame(), self.change_page, storage),
        }
        self.current_page: Page | None = None

        self.change_page("TUTORIAL")

    def _frame(self) -> ctk.CTkScrollableFrame:
        frame = ctk.CTkScrollableFrame(self)
        for i in range(20):
            frame.columnconfigure(i, weight=1)
        return frame

    def change_page(self, page: PAGE_NAMES) -> None:
        if self.current_page is not None:
            self.current_page.frame.grid_remove()
            for widget in self.current_page.frame.winfo_children():
                widget.grid_remove()

        self.current_page = self.pages[page]
        self.current_page.setup()
        self.current_page.frame.grid(row=0, column=0, sticky=ctk.NSEW)


def main() -> None:
    App().mainloop()


if __name__ == "__main__":
    main()
