from tkinter import ttk
from typing import Literal, cast

from automations import get_click_position
from pages.Page import Page


class StartPage(Page):
    def setup(self):
        if cast(bool, self.shared.storage["positions_set"]):
            return self.change_page("TEST")
        self.positions_set = 0

        self.test_position = None
        self.assets_position = None
        self.area_position = None
        self.comment_position = None

        ttk.Label(self.frame, text="Start Page").grid(column=0, row=0)
        self.test_button = ttk.Button(self.frame, text="Click here then on Testing tab", command=lambda: self.click_position("TESTING"))
        self.test_button.grid(column=0, row=1)
        self.assets_button = ttk.Button(self.frame, text="Click here then on Assets tab", command=lambda: self.click_position("ASSETS"))
        self.assets_button.grid(column=0, row=2)
        self.area_button = ttk.Button(self.frame, text="Click here then on Area Script", command=lambda: self.click_position("AREA"))
        self.area_button.grid(column=0, row=3)
        self.comment_button = ttk.Button(self.frame, text="Click here then on Comments box", command=lambda: self.click_position("COMMENTS"))
        self.comment_button.grid(column=0, row=4)

    def click_position(self, area: Literal["ASSETS", "TESTING", "AREA", "COMMENTS"]) -> None:
        position = get_click_position()
        if area == "ASSETS":
            self.assets_position = position
            self.assets_button.configure(text="Done", state="disabled")
        elif area == "TESTING":
            self.test_position = position
            self.test_button.configure(text="Done", state="disabled")
        elif area == "AREA":
            self.area_position = position
            self.area_button.configure(text="Done", state="disabled")
        elif area == "COMMENTS":
            self.comment_position = position
            self.comment_button.configure(text="Done", state="disabled")

        self.positions_set += 1

        if self.positions_set == 4:
            self.shared.storage.update(
                {
                    "testing_tab_position": self.test_position,
                    "assets_tab_position": self.assets_position,
                    "area_script_position": self.area_position,
                    "comment_box_position": self.comment_position,
                    "positions_set": self.positions_set,
                }
            )
            self.change_page("TEST")
