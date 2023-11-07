import os
import pathlib
import sys
import customtkinter as ctk

from design.JobManager import JobManager
from pages.ProblemPage import ProblemPage
from pages.Page import TPAGES, Page, SharedPageInfo
from pages.SettingsPage import SettingsPage
from pages.TestPage import TestPage
from pages.TutorialPage import TutorialPage
from storage.Storage import Storage

_APPLICATION_PATH = os.path.dirname(sys.executable)


class App(ctk.CTk):
    def __init__(self) -> None:
        super().__init__()
        self.geometry(f"1500x750+10+10")
        self.title("AutoSMX")

        self.after(201, lambda: self.iconbitmap(pathlib.Path(_APPLICATION_PATH, "autosmx.ico")))  # pyright: ignore

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        shared = SharedPageInfo(JobManager(), Storage(pathlib.Path(_APPLICATION_PATH, "store.pkl")))
        self.pages: dict[TPAGES, Page] = {
            "TUTORIAL": TutorialPage(self._frame(), self.change_page, shared),
            "SETTINGS": SettingsPage(self._frame(), self.change_page, shared),
            "PROBLEM": ProblemPage(self._frame(), self.change_page, shared),
            "TEST": TestPage(self._frame(), self.change_page, shared),
        }
        self.current_page: Page | None = None

        self.change_page("TUTORIAL")

    def _frame(self) -> ctk.CTkScrollableFrame:
        frame = ctk.CTkScrollableFrame(self)
        for i in range(20):
            frame.columnconfigure(i, weight=1)
        return frame

    def change_page(self, page: TPAGES) -> None:
        if self.current_page is not None:
            self.current_page.frame.grid_remove()
            for widget in self.current_page.frame.winfo_children():
                widget.grid_remove()

        self.current_page = self.pages[page]
        self.current_page.setup()
        self.current_page.frame.grid(row=0, column=0, sticky="nsew")


def main() -> None:
    App().mainloop()


if __name__ == "__main__":
    main()
