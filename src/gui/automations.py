import functools
import os
from typing import Any, Callable

try:
    import pyautogui
    import pyperclip  # type: ignore
    from pynput import mouse
except KeyError:
    pyautogui = None
    pyperclip = None
    mouse = None


_RUN = True  # actually run the automations or get default value (for testing)
_PRINT = False  # print the automations (for testing)
_DELAY = 0  # delay between automations (for testing)


def _automation_wrapper(default: Any | None = None) -> Callable[[Callable[..., Any]], Any]:  # testing decorator for printing, delaying, and returning default values
    def decorator(func: Callable[..., Any]):
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any):
            if _DELAY:
                pyautogui.sleep(_DELAY)  # pyright: ignore[reportOptionalMemberAccess]

            result = default if not _RUN else func(*args, **kwargs)
            if _PRINT:
                print(func.__name__, args, kwargs, "->", result, "(default)" if not _RUN else "")

            return result

        return wrapper

    return decorator


@_automation_wrapper()
def click_key(*keys: str, times: int = 1):
    for _ in range(times):
        pyautogui.hotkey(*keys)  # pyright: ignore[reportOptionalMemberAccess]


@_automation_wrapper()
def wait(seconds: float):
    pyautogui.sleep(seconds)  # pyright: ignore[reportOptionalMemberAccess]


@_automation_wrapper()
def type(text: str):
    pyautogui.typewrite(text)  # pyright: ignore[reportOptionalMemberAccess]


@_automation_wrapper()
def click(position: tuple[int, int], /, *, times: int = 1):
    for _ in range(times):
        pyautogui.click(position)  # pyright: ignore[reportOptionalMemberAccess]


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
    old = pyperclip.paste()
    pyautogui.hotkey("ctrl" if os.name == "nt" else "command", "c", interval=0.05)  # pyright: ignore[reportOptionalMemberAccess]
    pyautogui.sleep(0.01)  # pyright: ignore[reportOptionalMemberAccess]
    selected = pyperclip.paste()
    pyperclip.copy(old)  # type: ignore
    return selected
