import functools
import os
from typing import Any, Callable, Optional

import pyautogui
import pyperclip  # type: ignore
from pynput import mouse

_RUN = True
_PRINT = False


def _automation_wrapper(
    default: Optional[Any] = None,
) -> Callable[[Callable[..., Any]], Any]:  # pragma: no cover
    def decorator(func: Callable[..., Any]):
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any):
            if _PRINT:
                print(func.__name__, args, kwargs, end=" ")
                if not _RUN:
                    print("->", default, "(default)")
                    return default
            if not _RUN:
                return default
            res = func(*args, **kwargs)
            if _PRINT:
                print("->", res)
            return res

        return wrapper

    return decorator


@_automation_wrapper()
def click_key(*keys: str, times: int = 1):
    for _ in range(times):
        pyautogui.hotkey(*keys)


@_automation_wrapper()
def wait(seconds: float):
    pyautogui.sleep(seconds)


@_automation_wrapper()
def type(text: str):
    pyautogui.typewrite(text)


@_automation_wrapper()
def click(position: Optional[tuple[int, int]] = None, /, *, times: int = 1):
    if position is None:  # click middle if no position given
        x, y = pyautogui.size()
        position = x // 2, y // 2
    for _ in range(times):
        pyautogui.click(position)


@_automation_wrapper((0, 0))
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


@_automation_wrapper("selected text")
def get_selected_text():
    click_key("ctrl" if os.name == "nt" else "command", "c")
    pyautogui.sleep(0.01)
    return pyperclip.paste()
