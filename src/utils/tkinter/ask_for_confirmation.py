import tkinter


def ask_for_confirmation(title: str, message: str) -> bool:
    return tkinter.messagebox.askokcancel(title, message)  # type: ignore
