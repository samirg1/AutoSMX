import tkinter

import customtkinter as ctk

from utils.constants import ICON_PATH


class Popup(ctk.CTkToplevel):
    def __init__(self, master: tkinter.Misc | None, title: str, /, *, width: int = 360, height_factor: float = 0.75, columns: int = 1) -> None:
        super().__init__(master)
        self.title(title)
        self.after(201, lambda: self.iconbitmap(ICON_PATH))  # pyright: ignore

        height = int(750 * height_factor)
        start_height = (750 - height) // 2 + 10

        self.geometry(f"{width}x{height}+{(1500 - width) // 2 + 10}+{start_height}")

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.pop_frame = ctk.CTkScrollableFrame(self)
        for i in range(columns):
            self.pop_frame.columnconfigure(i, weight=1)

        self.pop_frame.grid(row=0, column=0, sticky=ctk.NSEW)

        self.after(100, self.lift)

    def grid_remove(self) -> None:  # ensure it gets cleaned up
        self.destroy()
