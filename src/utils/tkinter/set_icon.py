import customtkinter as ctk
from utils.constants import ICON_PATH


def set_icon(tk_or_toplevel: ctk.CTk | ctk.CTkToplevel) -> None:
    tk_or_toplevel.after(201, lambda: tk_or_toplevel.iconbitmap(ICON_PATH))  # type: ignore
