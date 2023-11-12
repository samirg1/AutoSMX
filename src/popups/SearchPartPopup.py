from tkinter import Misc
from db.get_parts import get_parts
from design.Part import Part
from popups.Popup import Popup
import customtkinter as ctk


class SearchPartPopup(Popup):
    def __init__(self, master: Misc | None, callback_var: ctk.StringVar) -> None:
        super().__init__(master, "Part Search", width=360*3, height_factor=0.75, columns=2)
        self.callback_var = callback_var

        self.labels: list[ctk.CTkLabel] = []
        self.buttons: list[ctk.CTkButton] = []

        description = ctk.StringVar()
        ctk.CTkLabel(self, text="Part Description").grid(row=0, column=0)
        ctk.CTkEntry(self, textvariable=description).grid(row=0, column=1)
        manufacturer = ctk.StringVar()
        ctk.CTkLabel(self, text="Manufacturer").grid(row=1, column=0)
        ctk.CTkEntry(self, textvariable=manufacturer).grid(row=1, column=1)
        part_number = ctk.StringVar()
        ctk.CTkLabel(self, text="Manufacturer Part Number").grid(row=2, column=0)
        ctk.CTkEntry(self, textvariable=part_number).grid(row=2, column=1)

        ctk.CTkButton(self, text="Search", command=lambda: self._search(description.get(), manufacturer.get(), part_number.get())).grid(row=3,column=0, columnspan=2)

    def _search(self, description: str, manufacturer: str, part_number: str) -> None:
        parts = get_parts({"part_desc": description, "manufacturer": manufacturer, "manufacturer_part_number": part_number})
        
        for label, button in zip(self.labels, self.buttons):
            label.grid_remove()
            button.grid_remove()

        for row, part in enumerate(parts, start=4):
            label = ctk.CTkLabel(self, text=f"PN: {part.number} - {part.description}")
            label.grid(row=row, column=0, sticky=ctk.W)
            button = ctk.CTkButton(self, text="Go", command=lambda part=part: self._select_part(part))
            button.grid(row=row, column=1)

            self.labels.append(label)
            self.buttons.append(button)

    def _select_part(self, part: Part) -> None:
        self.callback_var.set(part.number)
        self.destroy()