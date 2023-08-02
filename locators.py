from PIL import ImageGrab
import pyautogui
import pytesseract # type: ignore

# pytesseract.pytesseract.tesseract_cmd = (r"C:\...\AppData\Local\Programs\Tesseract-OCR\tesseract") # needed for Windows as OS

screen =  ImageGrab.grab() 
cap = screen.convert('L')

# BMI/Barcode

data: list[str] = pytesseract.image_to_boxes(cap).splitlines() # type: ignore
all_letters = ''.join(x[0] for x in data)

def find_text(image_data: list[str], all_letters: str, text: str) -> tuple[float, float]:
    index_start = all_letters.index(text)

    first = image_data[index_start].split(" ")
    left = int(first[1])
    bottom = int(first[2])
    right = int(image_data[index_start + len(text) - 1].split(" ")[3])
    top = int(first[4])
    for i in range(index_start + 1, index_start + len(text)):
        top = max(top, int(image_data[i].split(' ')[4]))

    mid_x, mid_y = (right + left) / 2, (top + bottom) / 2
    return convert_to_screen(mid_x, mid_y)

def convert_to_screen(x: float, y: float) -> tuple[float, float]:
    _, height = pyautogui.size()
    return x / 2, (height * 2 - y) / 2


x, y = find_text(data, all_letters, 'BMI/Barcode')
print(x, y)
pyautogui.moveTo(x, y)