import tkinter
from tkinter import Widget, ttk
from typing import Any


class Tooltip:
    def __init__(self, widget: Widget, text: str, *, delay: int = 400, wraplength: int = 250) -> None:
        self._delay = delay
        self._wraplength = wraplength
        self._widget = widget
        self._text = text
        self._widget.bind("<Enter>", self._onEnter)
        self._widget.bind("<Leave>", self._onLeave)
        self._widget.bind("<ButtonPress>", self._onLeave)
        self._padding = (5, 3, 5, 3)
        self._after_id: str | None = None
        self._tooltip: tkinter.Toplevel | None = None

    def _onEnter(self, _: Any) -> None:
        self._unschedule()
        self._after_id = self._widget.after(self._delay, self._show)

    def _onLeave(self, _: Any) -> None:
        self._unschedule()
        if self._tooltip is not None:
            self._tooltip.destroy()
        self._tooltip = None

    def _unschedule(self) -> None:
        if self._after_id is not None:
            self._widget.after_cancel(self._after_id)
        self._after_id = None

    def _calculate_position(self, label: ttk.Label) -> tuple[int, int]:
        s_width, s_height = self._widget.winfo_screenwidth(), self._widget.winfo_screenheight()
        width, height = (self._padding[0] + label.winfo_reqwidth() + self._padding[2], self._padding[1] + label.winfo_reqheight() + self._padding[3])
        mouse_x, mouse_y = self._widget.winfo_pointerxy()

        x1, y1 = mouse_x + 10, mouse_y + 5
        x_delta = max(x1 + width - s_width, 0)
        y_delta = max(y1 + height - s_height, 0)
        if x_delta == 0 and y_delta == 0:
            if x_delta:
                x1 = mouse_x - 10 - width

            if y_delta:
                y1 = mouse_y - 5 - height

        if x1 + self._wraplength > s_width:
            x1 = s_width - self._wraplength

        return x1, max(y1, 0)

    def _show(self) -> None:
        self._tooltip = tkinter.Toplevel(self._widget)
        self._tooltip.attributes("-topmost", 2)  # pyright: ignore
        self._tooltip.wm_overrideredirect(True)

        win = tkinter.Frame(self._tooltip, borderwidth=0)
        label = ttk.Label(win, text=self._text, justify=tkinter.LEFT, wraplength=self._wraplength)

        label.grid(padx=(self._padding[0], self._padding[2]), pady=(self._padding[1], self._padding[3]), sticky=tkinter.NSEW)
        win.grid()

        x, y = self._calculate_position(label)
        self._tooltip.wm_geometry(f"+{x}+{y}")
