from customtkinter import CTkButton
from utils.add_focus_bindings import add_focus_bindings


def test_add_focus_bindings() -> None:
    button = CTkButton(None)
    add_focus_bindings(button)
    