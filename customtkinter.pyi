import tkinter
from tkinter import _Anchor, _Cursor, _Relief, _ScreenUnits, Checkbutton, Tk, Toplevel, Misc, Variable, _TakeFocusValue, _ImageSpec  # pyright: ignore[reportPrivateUsage]
from tkinter.constants import *
from tkinter.font import _FontDescription  # pyright: ignore[reportPrivateUsage]
from tkinter.ttk import _Padding, _TtkCompound, Frame, Label, Button, Entry, Radiobutton  # pyright: ignore[reportPrivateUsage]
from typing import Any, Literal, overload

class CTk(Tk): ...
class CTkFrame(Frame): ...
class CTkScrollableFrame(Frame): ...

class CTkLabel(Label):
    def __init__(
        self,
        master: Misc | None = ...,
        *,
        anchor: _Anchor = ...,
        background: str = ...,
        border: _ScreenUnits = ...,
        borderwidth: _ScreenUnits = ...,
        class_: str = ...,
        compound: _TtkCompound = ...,
        cursor: _Cursor = ...,
        font: _FontDescription = ...,
        foreground: str = ...,
        image: _ImageSpec = ...,
        justify: Literal["left", "center", "right"] = ...,
        name: str = ...,
        padding: _Padding = ...,
        relief: _Relief = ...,
        state: str = ...,
        style: str = ...,
        takefocus: _TakeFocusValue = ...,
        text: float | str = ...,
        textvariable: Variable = ...,
        underline: int = ...,
        width: int | Literal[""] = ...,
        wraplength: _ScreenUnits = ...,
        text_color: str = ...,
    ) -> None: ...

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
        text_color: str = ...,
    ) -> dict[str, tuple[str, str, str, Any, Any]] | None: ...
    @overload
    def configure(self, cnf: str) -> tuple[str, str, str, Any, Any]: ...

class CTkEntry(Entry): ...
class CTkRadioButton(Radiobutton): ...
class CTkCheckBox(Checkbutton): ...
class CTkToplevel(Toplevel): ...


class CTkSegmentedButton:
    def __init__(self, master: Misc, *, values: list[str], variable: StringVar) -> None: ...
    def grid(self, *, row: int = 0, column: int = 0, columnspan: int = 1, sticky: str = "NESW") -> None: ...

class StringVar(tkinter.StringVar): ...
