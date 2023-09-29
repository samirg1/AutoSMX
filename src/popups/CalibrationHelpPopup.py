import os
import sys
from tkinter import Message, Misc, ttk

from PIL import Image, ImageTk

from popups.Popup import Popup

_APPLICATION_PATH = os.path.dirname(sys.executable)


class CalibrationHelpPopup(Popup):
    def __init__(self, master: Misc | None, image_name: str):
        width = 360
        super().__init__(master, "Calibration Help", width=width)

        img = Image.open(f"{_APPLICATION_PATH}/img/{image_name}.png")
        img = img.resize((width, 500), resample=Image.LANCZOS)
        img = ImageTk.PhotoImage(img)
        panel = ttk.Label(self, image=img)
        panel.image = img  # type: ignore
        panel.grid(column=0, row=0, sticky="nsew")

        Message(self, text="Click the button on the previous page, then click on the highlighted area in the image above", width=width).grid(column=0, row=1)
        ttk.Button(self, text="OK", command=self.destroy).grid(column=0, row=2)
