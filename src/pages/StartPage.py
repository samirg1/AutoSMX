from tkinter import ttk

from automations import get_click_position
from pages.Page import Page


class StartPage(Page):
    def setup(self):
        if self.shared.storage.positions_set:
            return self.change_page("TEST")
        self.positions_set = 0

        ttk.Label(self.frame, text="Start Page").grid(column=0, row=0)

        for row, key in enumerate(self.shared.storage.positions.keys(), start=1):
            button = ttk.Button(
                self.frame,
                text=f"Click here then on {' '.join(key.split('_')).title()}",
            )
            button.grid(column=0, row=row)
            button.configure(command=lambda button=button, key=key: self.click_position(button, key))  # type: ignore[misc]

    def click_position(self, button: ttk.Button, attribute_name: str) -> None:
        position = get_click_position()
        setattr(self.shared.storage.positions, attribute_name, position)
        button.configure(text="Done", state="disabled")

        self.positions_set += 1
        if self.positions_set == len(self.shared.storage.positions.__annotations__):
            self.shared.storage.positions_set = True
            self.shared.storage.save()
            self.change_page("TEST")
