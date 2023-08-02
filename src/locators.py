import os

import pytesseract  # type: ignore

if os.name == "nt":  # TODO specify path
    pytesseract.pytesseract.tesseract_cmd = r"C:\...\AppData\Local\Programs\Tesseract-OCR\tesseract"  # needed for Windows as OS


def find_text(image_string_lines: list[str], all_letters: str, text: str, window_height: int) -> tuple[float, float]:
    """
    Find the x, y coordinates of text in a pytesseract image string.
    - Input:
        - image_string_lines (list[str]): The image string lines from pytesseract.image_to_boxes.splitlines function.
        - all_letters (str): The list of all characters in the image string.
        - text (str): The text to find.
        - window_height (int): The height of the window.
    - Returns (tuple[float, float]): The x, y coordinates.
    """
    index_start = -1
    try:
        index_start = all_letters.index(text)
    except ValueError:
        raise ValueError(f"Could not find text '{text}' in image string.")

    start_coords = image_string_lines[index_start].split(" ")
    left = int(start_coords[1])
    bottom = int(start_coords[2])
    right = int(image_string_lines[index_start + len(text) - 1].split(" ")[3])
    top = int(start_coords[4])
    for i in range(index_start + 1, index_start + len(text)):
        top = max(top, int(image_string_lines[i].split(" ")[4]))

    mid_x, mid_y = (right + left) / 2, (top + bottom) / 2
    return _pytesseract_to_pyautogui_coords(mid_x, mid_y, window_height)


def _pytesseract_to_pyautogui_coords(x: float, y: float, window_height: int) -> tuple[float, float]:
    return x / 2, (window_height * 2 - y) / 2


if __name__ == "__main__":
    pass
