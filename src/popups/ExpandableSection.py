from tkinter import Misc
from typing import Any
import customtkinter as ctk


class ExpandableSection(ctk.CTkFrame):
    def __init__(self, parent: Misc | None, title: str, *args: Any, open: bool = False, **options: Any):
        super().__init__(parent, *args, **options)
        self.is_open = open

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)

        self.label = ctk.CTkLabel(self, text=title, cursor=self._get_cursor_type())
        self.label.grid(row=0, column=0, sticky=ctk.W)

        self.toggle_button = ctk.CTkButton(self, width=2, text=self._get_button_text(), command=self.toggle)
        self.toggle_button.grid(row=0, column=1)

        self.label.bind("<1>", lambda _: self.toggle_button.invoke())

        self.sub_frame = ctk.CTkFrame(self)

    def _get_button_text(self) -> str:
        return "-" if self.is_open else "+"
    
    def _get_cursor_type(self) -> str:
        return "top_side" if self.is_open else "bottom_side"

    def toggle(self):
        self.is_open = not self.is_open
        self.label.configure(cursor=self._get_cursor_type())
        self.toggle_button.configure(text=self._get_button_text())
        if self.is_open:
            self.sub_frame.grid(row=1, column=0, columnspan=20, sticky=ctk.NSEW)
        else:
            self.sub_frame.grid_forget()
