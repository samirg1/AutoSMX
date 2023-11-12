import tkinter
import customtkinter as ctk
import pathlib

from utils.constants import APPLICATION_PATH


class Popup(ctk.CTkToplevel):
    def __init__(self, master: tkinter.Misc | None, title: str, /, *, width: int = 360, height_factor: float = 0.75, columns: int = 1):
        super().__init__(master)
        self.title(title)
        self.after(201, lambda: self.iconbitmap(pathlib.Path(APPLICATION_PATH, "autosmx.ico")))  # pyright: ignore

        height = int(750 * height_factor)
        start_height = (750 - height) // 2 + 10

        self.geometry(f"{width}x{height}+{(1500 - width) // 2 + 10}+{start_height}")

        for i in range(columns):
            self.columnconfigure(i, weight=1)

        self.after(100, self.lift)

    def grid_remove(self) -> None:  # ensure it gets cleaned up
        self.destroy()
