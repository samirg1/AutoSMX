import tkinter

import customtkinter as ctk

from utils.constants import APP_HEIGHT, APP_WIDTH
from utils.set_icon import set_icon


class Popup(ctk.CTkToplevel):
    def __init__(self, master: tkinter.Misc | None, title: str, /, *, width: int = APP_WIDTH // 4, height_factor: float = 0.75, columns: int = 1) -> None:
        super().__init__(master)
        self.title(title)
        set_icon(self)

        height = int(APP_HEIGHT * height_factor)
        self.geometry(f"{width}x{height}+{(APP_WIDTH - width) // 2}+{(APP_HEIGHT - height) // 2}")

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.pop_frame = ctk.CTkScrollableFrame(self)
        for i in range(columns):
            self.pop_frame.columnconfigure(i, weight=1)

        self.pop_frame.grid(row=0, column=0, sticky=ctk.NSEW)

        self.after(100, self.lift)

    def grid_remove(self) -> None:  # ensure it gets cleaned up
        self.destroy()
