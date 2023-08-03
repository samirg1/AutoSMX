from tkinter import ttk
from pages import Page


class JobPage(Page):
    def setup(self):
        self.button = ttk.Button(self.frame, text="JobPage", command=self.test)
        self.button.grid(column=0, row=0)

    def test(self):
        self.parent.change_page("TEST")