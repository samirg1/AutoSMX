import customtkinter as ctk
from utils.constants import DEFAULT_TEXT_COLOUR_BUTTON, FOCUSED_TEXT_COLOUR_BUTTON


def add_focus_bindings(button: ctk.CTkButton) -> None:
    button.bind("<FocusIn>", lambda _: button.configure(text_color=FOCUSED_TEXT_COLOUR_BUTTON))
    button.bind("<FocusOut>", lambda _: button.configure(text_color=DEFAULT_TEXT_COLOUR_BUTTON))