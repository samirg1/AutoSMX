from tkinter import Misc
from typing import Iterable, NamedTuple

import customtkinter as ctk

from db.get_parts import get_parts
from design.Part import Part
from popups.Popup import Popup
from utils.constants import HORIZONTAL_LINE, PART_FIELDS, PART_POPUP_WIDTH


class _Field(NamedTuple):
    title: str
    name: PART_FIELDS
    variable: ctk.StringVar


class SearchPartPopup(Popup):
    def __init__(self, master: Misc | None, previous_parts: Iterable[Part], callback_var: ctk.StringVar | None = None) -> None:
        super().__init__(master, "Part Search", width=PART_POPUP_WIDTH, height_factor=0.75, columns=2)
        self.callback_var = callback_var

        self.fields: tuple[_Field, ...] = (
            _Field("Part Description", "part_desc", ctk.StringVar()),
            _Field("Manufacturer", "manufacturer", ctk.StringVar()),
            _Field("Manufacturer Part Number", "manufacturer_part_number", ctk.StringVar()),
        )

        entries: list[ctk.CTkEntry] = []
        for i, (title, _, variable) in enumerate(self.fields):
            ctk.CTkLabel(self.pop_frame, text=title).grid(row=i, column=0)
            entries.append(ctk.CTkEntry(self.pop_frame, textvariable=variable))
            entries[-1].grid(row=i, column=1)

        search_button = ctk.CTkButton(self.pop_frame, text="Search", command=lambda: self._search(self.fields))
        search_button.grid(row=len(self.fields), column=0, columnspan=2)

        for entry in entries:
            entry.bind("<Return>", lambda _: search_button.invoke())

        self.result_widgets: list[ctk.CTkLabel | ctk.CTkButton] = []
        self._display_parts(previous_parts, previous=True)

    def _search(self, fields: tuple[_Field, ...]) -> None:
        parts = get_parts({field.name: field.variable.get() for field in fields})
        self._display_parts(parts)

    def _display_parts(self, parts: Iterable[Part], *, previous: bool = False) -> None:
        start = len(self.fields) + 2
        for widget in self.result_widgets:
            widget.grid_remove()
        self.result_widgets.clear()

        row = start
        for part in parts:
            line = ctk.CTkLabel(self.pop_frame, text=HORIZONTAL_LINE)
            line.grid(row=row, column=0, sticky=ctk.EW, columnspan=2)
            label = ctk.CTkLabel(self.pop_frame, text=f"PN: {part.number} - {part.description}")
            label.grid(row=row + 1, column=0, sticky=ctk.W)
            if self.callback_var is not None:
                button = ctk.CTkButton(self.pop_frame, text="Go", command=lambda part=part: self._select_part(part, self.callback_var))  # type: ignore[misc]
                button.grid(row=row + 1, column=1)
                self.result_widgets.append(button)

            self.result_widgets.append(line)
            self.result_widgets.append(label)
            row += 2

        text = "Previously Used" if previous else f"Search Results ({(row - start) // 2})" if parts else ""
        label = ctk.CTkLabel(self.pop_frame, text=text)
        label.grid(row=start-1, column=0, columnspan=2, sticky=ctk.EW)
        self.result_widgets.append(label)

    def _select_part(self, part: Part, callback_var: ctk.StringVar) -> None:
        callback_var.set(part.number)
        self.destroy()
