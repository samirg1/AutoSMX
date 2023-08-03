from tkinter import ttk
import tkinter
from typing import cast
from design.Job import Job
from pages.Page import Page


class TestPage(Page):
    def setup(self, **kwargs: str):
        self.job = cast(Job, kwargs["job"])

        ttk.Button(self.frame, text="Back", command=lambda: self.change_page("JOB")).grid(column=0, row=0, sticky="w")
        ttk.Label(self.frame, text=f"{self.job}").grid(column=1, row=0, columnspan=3)

        ttk.Label(self.frame, text="Item Number").grid(column=0, row=1, columnspan=2)
        self.item_number = tkinter.StringVar()
        entry = ttk.Entry(self.frame, textvariable=self.item_number)
        entry.grid(column=2, row=1, sticky="w", columnspan=2)
        entry.focus()
        entry.bind("<Return>", lambda _: self.get_item())

        ttk.Button(self.frame, text="Go", command=self.get_item).grid(column=0, row=2, columnspan=4)

    def get_item(self):
        print(self.item_number.get())

    def test(self):
        self.change_page("JOB")