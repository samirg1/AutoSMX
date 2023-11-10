import pathlib
import customtkinter as ctk

from pages.ProblemPage import ProblemPage
from pages.Page import Page
from pages.SettingsPage import SettingsPage
from pages.TestPage import TestPage
from pages.TutorialPage import TutorialPage
from storage.Storage import Storage
from utils.constants import PAGE_NAMES
from utils.constants import APPLICATION_PATH

class App(ctk.CTk):
    def __init__(self) -> None:
        super().__init__()
        self.geometry(f"1500x750+10+10")
        self.title("AutoSMX")

        self.after(201, lambda: self.iconbitmap(pathlib.Path(APPLICATION_PATH, "autosmx.ico")))  # pyright: ignore

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        storage = Storage()
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
