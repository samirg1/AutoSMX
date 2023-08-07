from tkinter import ttk
from typing import Literal

from automations import get_click_position
from pages.Page import Page


class StartPage(Page):
    def setup(self):
        ttk.Label(self.frame, text="Start Page").grid(column=0, row=0)
        self.test_button = ttk.Button(self.frame, text="Click here then on Testing tab", command=lambda: self.click_position("TESTING"))
        self.test_button.grid(column=0, row=1)

        self.assets_button = ttk.Button(self.frame, text="Click here then on Assets tab", command=lambda: self.click_position("ASSETS"))
        self.assets_button.grid(column=0, row=2)

        self.area_button = ttk.Button(self.frame, text="Click here then on Area Script", command=lambda: self.click_position("AREA"))
        self.area_button.grid(column=0, row=3)

        self.comments_button = ttk.Button(self.frame, text="Click here then on Comments box", command=lambda: self.click_position("COMMENTS"))
        self.comments_button.grid(column=0, row=4)

    def click_position(self, area: Literal["ASSETS", "TESTING", "AREA", "COMMENTS"]) -> None:
        position = get_click_position()
        if area == "ASSETS":
            self.shared.assets_position = position
            self.assets_button.configure(text="Done", state="disabled")
        elif area == "TESTING":
            self.shared.testing_position = position
            self.test_button.configure(text="Done", state="disabled")
        elif area == "AREA":
            self.shared.area_position = position
            self.area_button.configure(text="Done", state="disabled")
        elif area == "COMMENTS":
            self.shared.comments_position = position
            self.comments_button.configure(text="Done", state="disabled")

        self.shared.position_set += 1

        if self.shared.position_set == 4:
            self.change_page("TEST")
