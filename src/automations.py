import os
import pyautogui
from pynput import mouse
import pyperclip # type: ignore

def click_key(*keys: str, times: int = 1):
    for _ in range(times):
        pyautogui.hotkey(*keys, interval=0.1)
        pyautogui.sleep(0.1)

def type(text: str):
        pyautogui.typewrite(text, interval=0.1)

def click(position: tuple[int, int] | None = None, /, *, times: int = 1):
    if position is None: # click middle if no position given
        x, y = pyautogui.size()
        position = x // 2, y // 2

    for _ in range(times):
        pyautogui.click(position)
        pyautogui.sleep(0.1)

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

def get_selected_text():
    click_key("ctrl" if os.name == "nt" else "command", "c", times=1)
    pyautogui.sleep(0.01)
    return pyperclip.paste()