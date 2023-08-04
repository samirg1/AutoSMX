def _pytesseract_to_pyautogui_coords(x: float, y: float, window_height: int) -> tuple[float, float]:
    return x / 2, (window_height * 2 - y) / 2

class FindSearch:
    def __init__(self, image_string_lines: list[str], all_letters: str, window_height: int) -> None:
        self.image_string_lines = image_string_lines
        self.all_letters = all_letters
        self.window_height = window_height

    def get_start_index(self, text: str) -> int:
        try:
            return self.all_letters.index(text)
        except ValueError:
            raise ValueError(f"Could not find text '{text}' in image string.") from None

    def find_text(self, text: str) -> tuple[float, float]:
        index_start = self.get_start_index(text)
        start_coords = self.image_string_lines[index_start].split(" ")

        left = int(start_coords[1])
        bottom = int(start_coords[2])
        right = int(self.image_string_lines[index_start + len(text) - 1].split(" ")[3])
        top = int(start_coords[4])
        for i in range(index_start + 1, index_start + len(text)):
            top = max(top, int(self.image_string_lines[i].split(" ")[4]))

        mid_x, mid_y = (right + left) / 2, (top + bottom) / 2
        return _pytesseract_to_pyautogui_coords(mid_x, mid_y, self.window_height)
    
    def get_text(self, starting: str):
        index_start = self.get_start_index(starting)
        start_coords = self.image_string_lines[index_start].split(" ")
        bottom = int(start_coords[2])
        
        i = index_start + len(starting)
        string_line = self.image_string_lines[i].split(" ")
        while abs(int(string_line[2]) - bottom) <= 10:
            starting += self.image_string_lines[i][0]
            i += 1
            string_line = self.image_string_lines[i].split(" ")

        return starting