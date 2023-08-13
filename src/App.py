import tkinter
from tkinter import ttk

from design import TestJobManager
<<<<<<< HEAD
from pages import Page, JobPage, TPAGES, SharedPageInfo, StartPage, TestPage
=======
from pages import JobPage, TPAGES, Page, SharedPageInfo, StartPage, TestPage
>>>>>>> 0d417b205ec7807a2130fd9bbc0533c67e4efb7c
from Storage import Storage


class App(tkinter.Tk):
    def __init__(self):
        super().__init__()
        maxWidth = self.winfo_screenwidth()
        width = 360
        height = self.winfo_screenheight()
        self.geometry(f"{width}x{height}+{maxWidth - width}+0")
        self.title("ALTER SMX Tool")
        self.attributes("-topmost", 1)  # type: ignore

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        shared = SharedPageInfo({}, TestJobManager(), Storage.from_json_file("src/store.json"))
        self.pages: dict[TPAGES, Page] = {
            "START": StartPage(self._frame(), self.change_page, shared),
            "JOB": JobPage(self._frame(), self.change_page, shared),
            "TEST": TestPage(self._frame(), self.change_page, shared),
        }
        self.current_page: Page | None = None

        self.change_page("START")

    def _frame(self) -> ttk.Frame:
        frame = ttk.Frame(self, padding=10)
        frame.columnconfigure(0, weight=1)
        frame.columnconfigure(1, weight=1)
        frame.columnconfigure(2, weight=1)
        frame.columnconfigure(3, weight=1)
        return frame

    def change_page(self, page: TPAGES):
        if self.current_page is not None:
            self.current_page.frame.grid_remove()
            for widget in self.current_page.frame.winfo_children():
                widget.grid_remove()

        self.current_page = self.pages[page]
        self.current_page.setup()
        self.current_page.frame.grid(row=0, column=0, sticky="nsew")


if __name__ == "__main__":
    App().mainloop()
