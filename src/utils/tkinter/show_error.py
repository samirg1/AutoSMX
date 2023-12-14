import tkinter


def show_error(title: str, message: str) -> None:
    tkinter.messagebox.showerror(title, message)  # type: ignore
