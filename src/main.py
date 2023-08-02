import pyautogui
import pytesseract  # type: ignore
from PIL import ImageGrab

from src.locators import find_text

if __name__ == "__main__":
    screen = ImageGrab.grab()
    cap = screen.convert("L")

    data: list[str] = pytesseract.image_to_boxes(cap).splitlines()  # type: ignore
    all_letters = "".join(x[0] for x in data)

    _, height = pyautogui.size()
    x, y = find_text(data, all_letters, "BMI/Barcode", height)
    print(x, y)
    pyautogui.moveTo(x, y)
