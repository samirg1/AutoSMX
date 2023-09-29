import tkinter
from tkinter import ttk

from gui.automations import get_click_position
from popups.CalibrationHelpPopup import CalibrationHelpPopup
from pages.Page import Page


class CalibrationPage(Page):
    def setup(self) -> None:
        if self.shared.storage.calibrated:
            return self.change_page("JOB")
        self.positions_set = 0

        ttk.Label(self.frame, text="Calibration").grid(column=0, row=0, sticky="nsew")

        tkinter.Message(
            self.frame,
            width=300,
            text="Please click on the following buttons, then on the corresponding area to set the positions of the GUI elements so that the software knows where to click to navigate SMX.",
        ).grid(column=0, row=1, columnspan=4)

        for row, key in enumerate(self.shared.storage.positions.keys(), start=2):
            button = ttk.Button(
                self.frame,
                text=f"Click here then on {' '.join(key.split('_')).title()}",
            )
            button.grid(column=0, row=row, columnspan=3, sticky="w")
            button.configure(command=lambda button=button, key=key: self.click_position(button, key))  # type: ignore[misc]
            ttk.Button(self.frame, text="?", width=1, command=lambda key=key: self.show_help(key)).grid(column=3, row=row, columnspan=1, sticky="e")  # type: ignore[misc]

    def click_position(self, button: ttk.Button, attribute_name: str) -> None:
        position = get_click_position()
        setattr(self.shared.storage.positions, attribute_name, position)
        button.configure(text="Done", state="disabled")

        self.positions_set += 1
        if self.positions_set == len(self.shared.storage.positions.__annotations__):
            with self.shared.storage.edit() as storage:
                storage.calibrated = True
            self.change_page("TEST")

    def show_help(self, name: str) -> None:
        CalibrationHelpPopup(self.frame, name).mainloop()
