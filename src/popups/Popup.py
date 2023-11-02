import tkinter


class Popup(tkinter.Toplevel):
    def __init__(self, master: tkinter.Misc | None, title: str, /, *, width: int = 360, height_factor: float = 0.75, columns: int = 1):
        super().__init__(master)
        self.title(title)

        max_width = self.winfo_screenwidth()
        max_height = self.winfo_screenheight()
        height = int(max_height * height_factor)
        start_height = (max_height - height) // 2

        self.geometry(f"{width}x{height}+{(max_width - width) // 2}+{start_height}")
        self.attributes("-topmost", 2)  # pyright: ignore
        self.resizable(False, False)

        for i in range(columns):
            self.columnconfigure(i, weight=1)

    def grid_remove(self) -> None:  # ensure it gets cleaned up
        self.destroy()
