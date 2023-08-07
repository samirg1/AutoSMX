import functools
import os
from typing import Any, Callable

import pyautogui
import pyperclip  # type: ignore
from pynput import mouse

_RUN = False
_PRINT = False


def _print(default: Any | None = None) -> Callable[[Callable[..., Any]], Any]:
    def decorator(func: Callable[..., Any]):
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any):
            if _PRINT:
                print(func.__name__, args, kwargs, end=" ")
                if not _RUN:
                    print("->", default)
                    return default
            if not _RUN:
                return default
            res = func(*args, **kwargs)
            if _PRINT:
                print("->", res)
            return res

        return wrapper

    return decorator


@_print()
def click_key(*keys: str, times: int = 1):
    for _ in range(times):
        pyautogui.hotkey(*keys, interval=0.1)
        pyautogui.sleep(0.1)


@_print()
def type(text: str):
    pyautogui.typewrite(text, interval=0.1)


@_print()
def click(position: tuple[int, int] | None = None, /, *, times: int = 1):
    if position is None:  # click middle if no position given
        x, y = pyautogui.size()
        position = x // 2, y // 2
    for _ in range(times):
        pyautogui.click(position)
        pyautogui.sleep(0.1)


@_print((0, 0))
def get_click_position() -> tuple[int, int]:
    position: tuple[int, int] = -1, -1

    def on_click(x: float, y: float, button: mouse.Button, pressed: bool):
        if button == mouse.Button.left and pressed:
            nonlocal position
            position = int(x), int(y)
            return False

    listener = mouse.Listener(on_click=on_click)
    listener.start()
    listener.join()

    return position


@_print("selected text")
def get_selected_text():
    click_key("ctrl" if os.name == "nt" else "command", "c")
    pyautogui.sleep(0.01)
    return pyperclip.paste()
