from tkinter.font import Font
import webbrowser

import customtkinter as ctk

from pages.Page import Page
from utils.constants import APP_WIDTH, HORIZONTAL_LINE, TUTORIAL_PATH


class TutorialPage(Page):
    def setup(self) -> None:
        # if self.storage.tutorial_complete:
        #     return self.change_page("PROBLEM")

        ctk.CTkLabel(self.frame, text="Tutorial Page").grid(row=0, column=0, sticky=ctk.EW, columnspan=16)
        ctk.CTkButton(self.frame, text="View File", command=lambda: webbrowser.open(str(TUTORIAL_PATH))).grid(row=0, column=17)
        ctk.CTkButton(self.frame, text="Skip", command=self._end_tutorial).grid(row=0, column=19)

        with open(TUTORIAL_PATH) as f:
            tutorial = f.readlines()

        lines: list[str] = []
        for line in tutorial:
            new_lines = self._adjust_newlines(line, APP_WIDTH)
            lines.extend(line for line in new_lines if line)

        row = 1
        for line in lines:
            if line.startswith("# "):
                ctk.CTkLabel(self.frame, text=HORIZONTAL_LINE).grid(row=row, column=0, sticky=ctk.EW, columnspan=20)
                ctk.CTkLabel(self.frame, text=line[2:], font=("Helvetica", 18, "bold")).grid(row=row + 1, column=0, columnspan=20)
                ctk.CTkLabel(self.frame, text=HORIZONTAL_LINE).grid(row=row + 2, column=0, sticky=ctk.EW, columnspan=20)
                row += 2
            elif line.startswith("### "):
                ctk.CTkLabel(self.frame, text="").grid(row=row, column=0, sticky=ctk.EW, columnspan=20)
                ctk.CTkLabel(self.frame, text=line[4:], font=("Helvetica", 16)).grid(row=row + 1, column=0, columnspan=20)
                row += 1
            else:
                line = line if not line.startswith("- ") else "\t" + line
                ctk.CTkLabel(self.frame, text=line).grid(row=row, column=0, sticky=ctk.W, columnspan=20)
            row += 1

    def _adjust_newlines(self, val: str, width: int) -> list[str]:
        font = Font(font="TkDefaultFont")
        words = val.split()
        lines: list[str] = [""]
        for word in words:
            line = lines[-1] + word
            if font.measure(line) < width:
                lines[-1] = line + " "
            else:
                lines.append(word + " ")

        return lines

    def _end_tutorial(self) -> None:
        with self.storage.edit() as storage:
            storage.tutorial_complete = True
        self.change_page("PROBLEM")
