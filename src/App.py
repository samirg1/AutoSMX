import tkinter
from tkinter import ttk
from typing import Any, cast

from design.Job import Job
from pages.StartPage import StartPage
from pages.JobPage import JobPage
from pages.Page import TPAGES, Page, SharedPageInfo
from pages.TestPage import TestPage


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

        self.jobs: dict[str, Job] = {}

        shared = SharedPageInfo()
        self.pages: dict[TPAGES, Page] = {
            "START": StartPage(self._frame(), self.change_page, shared),
            "JOB": JobPage(self._frame(), self.change_page, shared),
            "TEST": TestPage(self._frame(), self.change_page, shared),
        }
        self.current_page: Page | None = None

        self.change_page("START")

    def _frame(self) -> ttk.Frame:
        frame = ttk.Frame(self, padding="3 3 12 12")
        frame.columnconfigure(0, weight=1)
        frame.columnconfigure(1, weight=1)
        frame.columnconfigure(2, weight=1)
        frame.columnconfigure(3, weight=1)
        return frame

    def change_page(self, page: TPAGES, **kwargs: Any):
        if "testing_position" in kwargs:
            self.assets_position = kwargs["assets_position"]
            self.testing_position = kwargs["testing_position"]
            self.area_position = kwargs["area_position"]
            self.comments_position = kwargs["comments_position"]

        if "job" in kwargs:
            job = cast(Job, kwargs["job"])
            self.jobs[job.campus] = job

        if "jobs" not in kwargs:
            kwargs["jobs"] = self.jobs

        if self.current_page is not None:
            self.current_page.frame.grid_remove()
            for widget in self.current_page.frame.winfo_children():
                widget.grid_remove()

        self.current_page = self.pages[page]
        self.current_page.setup(**kwargs)
        self.current_page.frame.grid(row=0, column=0, sticky="nsew")

if __name__ == "__main__":
    App().mainloop()
