from tkinter import ttk
from typing import Literal, cast

from automations import get_click_position
from pages.Page import Page


class StartPage(Page):
    def setup(self):
        self.positions_set = cast(int, self.shared.storage["positions_set"])
        if self.positions_set == 4:
            self.change_page("TEST")
            return

        storage_test = cast(tuple[int, int] | None, self.shared.storage["testing_tab_position"])
        storage_assets = cast(tuple[int, int] | None, self.shared.storage["assets_tab_position"])
        storage_area = cast(tuple[int, int] | None, self.shared.storage["area_script_position"])
        storage_comments = cast(tuple[int, int] | None, self.shared.storage["comment_box_position"])

        ttk.Label(self.frame, text="Start Page").grid(column=0, row=0)
        r = 1

        if storage_test is None:
            self.test_button = ttk.Button(self.frame, text="Click here then on Testing tab", command=lambda: self.click_position("TESTING"))
            self.test_button.grid(column=0, row=r)
            r += 1

        if storage_assets is None:
            self.assets_button = ttk.Button(self.frame, text="Click here then on Assets tab", command=lambda: self.click_position("ASSETS"))
            self.assets_button.grid(column=0, row=r)
            r += 1

        if storage_area is None:
            self.area_button = ttk.Button(self.frame, text="Click here then on Area Script", command=lambda: self.click_position("AREA"))
            self.area_button.grid(column=0, row=r)
            r += 1

        if storage_comments is None:
            self.comments_button = ttk.Button(self.frame, text="Click here then on Comments box", command=lambda: self.click_position("COMMENTS"))
            self.comments_button.grid(column=0, row=r)
            r += 1

    def click_position(self, area: Literal["ASSETS", "TESTING", "AREA", "COMMENTS"]) -> None:
        position = get_click_position()
        if area == "ASSETS":
            self.shared.storage["assets_tab_position"] = position
            self.assets_button.configure(text="Done", state="disabled")
        elif area == "TESTING":
            self.shared.storage["testing_tab_position"] = position
            self.test_button.configure(text="Done", state="disabled")
        elif area == "AREA":
            self.shared.storage["area_script_position"] = position
            self.area_button.configure(text="Done", state="disabled")
        elif area == "COMMENTS":
            self.shared.storage["comment_box_position"] = position
            self.comments_button.configure(text="Done", state="disabled")

        self.positions_set += 1

        if self.positions_set == 4:
            self.shared.storage["positions_set"] = self.positions_set
            self.change_page("TEST")
