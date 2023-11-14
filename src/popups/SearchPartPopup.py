from tkinter import Misc
from typing import Iterable
from db.get_parts import get_parts
from design.Part import Part
from popups.Popup import Popup
import customtkinter as ctk


class SearchPartPopup(Popup):
    def __init__(self, master: Misc | None, callback_var: ctk.StringVar, previous_parts: Iterable[Part]) -> None:
        super().__init__(master, "Part Search", width=360*3, height_factor=0.75, columns=2)
        self.callback_var = callback_var

        self.labels: list[ctk.CTkLabel] = []
        self.buttons: list[ctk.CTkButton] = []

        description = ctk.StringVar()
        ctk.CTkLabel(self.frame, text="Part Description").grid(row=0, column=0)
        ctk.CTkEntry(self.frame, textvariable=description).grid(row=0, column=1)
        manufacturer = ctk.StringVar()
        ctk.CTkLabel(self.frame, text="Manufacturer").grid(row=1, column=0)
        ctk.CTkEntry(self.frame, textvariable=manufacturer).grid(row=1, column=1)
        part_number = ctk.StringVar()
        ctk.CTkLabel(self.frame, text="Manufacturer Part Number").grid(row=2, column=0)
        ctk.CTkEntry(self.frame, textvariable=part_number).grid(row=2, column=1)

        ctk.CTkButton(self.frame, text="Search", command=lambda: self._search(description.get(), manufacturer.get(), part_number.get())).grid(row=3,column=0, columnspan=2)

        self._display_parts(previous_parts, previous=True)

    def _search(self, description: str, manufacturer: str, part_number: str) -> None:
        parts = get_parts({"part_desc": description, "manufacturer": manufacturer, "manufacturer_part_number": part_number})
        self._display_parts(parts)

    def _display_parts(self, parts: Iterable[Part], *, previous: bool = False) -> None:
        start = 4
        for label in self.labels:
            label.grid_remove()
        
        for button in self.buttons:
            button.grid_remove()

        if previous:
            label = ctk.CTkLabel(self.frame, text="Previously Used")
            label.grid(row=start, column=0, columnspan=2, sticky=ctk.EW)
            self.labels.append(label)
            start += 1

        for row, part in enumerate(parts, start=start):
            label = ctk.CTkLabel(self.frame, text=f"PN: {part.number} - {part.description}")
            label.grid(row=row, column=0, sticky=ctk.W)
            button = ctk.CTkButton(self.frame, text="Go", command=lambda part=part: self._select_part(part))
            button.grid(row=row, column=1)

            self.labels.append(label)
            self.buttons.append(button)

    def _select_part(self, part: Part) -> None:
        self.callback_var.set(part.number)
        self.destroy()