import time
from typing import Any
import pyautogui
import pyperclip
import pytesseract  # type: ignore
from PIL import ImageGrab
from automations import FindSearch

if __name__ == "__main__":

    # time.sleep(2)
    
    # screen = ImageGrab.grab()
    # cap = screen.convert()

    # data: list[str] = pytesseract.image_to_boxes(cap).splitlines()  # type: ignore
    # all_letters = "".join(x[0] for x in data)
    # print(all_letters)

    # _, height = pyautogui.size()

    # finder_searcher = FindSearch(data, all_letters, height)

    # print(finder_searcher.get_text("Manufacturer"))
    # time.sleep(2)
    # def copy_clipboard():
    #     pyautogui.hotkey('command', 'c', interval=0.1)
    #     time.sleep(.01)  # ctrl-c is usually very fast but your program may execute faster
    #     return pyperclip.paste()

    # list = []
    # var = copy_clipboard()
    # list.append(var) 
    # print(list)

    from pynput import mouse

    def get_click_position() -> tuple[int, int]:
        position: tuple[int, int] = -1, -1 
        def on_click(x: float, y: float, button: mouse.Button, pressed: bool):
            if button == mouse.Button.left and pressed:
                nonlocal position
                position = int(x), int(y)
                print(pyautogui.position())
                return False

        listener = mouse.Listener(on_click=on_click)
        listener.start()
        listener.join()

        return position
    
    print(get_click_position())











# Model: Liko        Manufacturer: Liko
