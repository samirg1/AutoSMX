import tkinter
from tkinter import ttk
from PIL import Image, ImageTk



class StartHelpPopup(tkinter.Toplevel):
    def __init__(self, master: tkinter.Misc | None, image_name: str):
        super().__init__(master)
        self.title("Help")
        maxWidth = self.winfo_screenwidth()
        width = 360
        height = self.winfo_screenheight()
        self.geometry(f"{width}x{height // 4 * 3}+{maxWidth - width}+{height // 8}")
        self.attributes("-topmost", 2)  # type: ignore
        self.resizable(False, False)

        self.columnconfigure(0, weight=1)

        img = Image.open(f"src/img/{image_name}.png")
        img = img.resize((360, 500), resample=Image.LANCZOS)
        img = ImageTk.PhotoImage(img)
        panel = ttk.Label(self, image=img)
        panel.image = img # type: ignore
        panel.grid(column=0, row=0, sticky="nsew")

        tkinter.Message(self, text="Click the button on the previous page, then click on the highlighted area in the image above").grid(column=0, row=1)
        ttk.Button(self, text="OK", command=self.destroy).grid(column=0, row=2)

        