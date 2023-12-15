from tkinter import Misc
from typing import Any

import customtkinter as ctk 


class UppercaseEntry(ctk.CTkEntry):
    def __init__(self, master: Misc | None, *args: Any, textvariable: ctk.StringVar, **kwargs: Any) -> None:
        super().__init__(master, *args, textvariable=textvariable, **kwargs)
        textvariable.trace_add("write", lambda _, __, ___: textvariable.set(textvariable.get().upper()))
