import tkinter
from tkinter import Tk, Toplevel, Misc, Variable, _TakeFocusValue, _ImageSpec  # pyright: ignore[reportPrivateUsage]
from tkinter.constants import *
from tkinter.ttk import Frame, Label, Button, Entry, Radiobutton
from typing import Any, Literal, overload

class CTk(Tk): ...
class CTkFrame(Frame): ...
class CTkScrollableFrame(Frame): ...
class CTkLabel(Label): ...

class CTkButton(Button):
    @overload
    def configure(
        self,
        cnf: dict[str, Any] | None = None,
        *,
        command: Any = ...,
        compound: Any = ...,
        cursor: Any = ...,
        default: Literal["normal", "active", "disabled"] = ...,
        image: _ImageSpec = ...,
        padding: str = ...,
        state: str = ...,
        style: str = ...,
        takefocus: _TakeFocusValue = ...,
        text: float | str = ...,
        textvariable: Variable = ...,
        underline: int = ...,
        width: int | Literal[""] = ...,
        text_color: str = ...
    ) -> dict[str, tuple[str, str, str, Any, Any]] | None: ...
    @overload
    def configure(self, cnf: str) -> tuple[str, str, str, Any, Any]: ...

class CTkEntry(Entry): ...
class CTkRadioButton(Radiobutton): ...
class CTkToplevel(Toplevel): ...

class CTkSegmentedButton:
    def __init__(self, master: Misc, *, values: list[str], variable: StringVar) -> None: ...
    def grid(self, *, row: int = 0, column: int = 0, columnspan: int = 1, sticky: str = "NESW") -> None: ...

class StringVar(tkinter.StringVar): ...
