import tkinter
from tkinter import ttk

from pages.Page import Page

_TUTORIAL = [
    "This is the tutorial page. It will walk you through the process of setting up the program.",
    "CALIBRATION\nThe first time you use this software, you need to calibrate it, do this on the next page by clicking the buttons, then immediately clicking on the corresponding area on the screen. You only need to do this once.",
    "FIRST ITEM\n- make sure to enter it into SMX and hit enter first, this will allow for any delay on the first search. Also make sure that the Assets Tab does not currently have an item open (Cancel or Save the asset).\n- before you enter it into the program, ensure that the BMI/Barcode text is selected, you only need to do this once each time you close and open the software.",
    "ENTER ASSET\nEnter the item into the program, then click 'Go' / press Enter. The program will then search for the item's script. Do not press 'Choose' unless the program has failed to find the script.",
    "The program will try and determine the script needed for this item, make sure this is correct before proceeding.",
    "EDIT SCRIPT\nEdit the script value, add a job by click the 'Add Job' button, add comments and anything else that is needed for the test",
    "SAVE TEST\nEnsure values of the script are correct before clicking 'Save' (or press enter straight away), the program will now input the test.",
    "The program will now wait for the test to complete, once it has, it will save the results and return to the item entry screen.",
]

_TROUBLESHOOTING = [
    "If anything goes wrong while the program is running, quickly move the mouse to any corner of the screen to activate the failsafe.",
    "If the program incorrectly selects the script, press 'Cancel' and then select 'Choose' to manually select the script.",
    "If the program fails in an unexpected way, activated the failsafe and then ensure the program is reset by following the 'FIRST ITEM' step in the tutorial.",
    "If the program it glitching or bugging and you don't believe SMX is the issue, try restarting the program. If the problem persists raise an issue using this link:\nhttps://github.com/samirg1/ALTER-SMX-Tool/issues\nPlease ensure you include any error messages as well as a description of the problem and how to reproduce it.",
    "If you need to recalibrate or see this tutorial again, navigate to the 'Jobs' page and click on the respective button."
]

_FEATURES = [
    "SCRIPT MATCHING\nThe program will use the asset description to determine the script needed for the item. It searches for text near the description and has in-built exact matches for common items.",
    "The program will automatically select the correct script for the item, if it fails to do so, you can manually select the script.",
    "SCRIPT ANSWERS\nThe program will show the default script answers for the selected script, you can edit these answers and add jobs / comments if needed.",
    "If you change the script answers from the default for a specific item model, the program will remember these answers for the next time you test that specifc item model.",
    "ADDING JOBS\nAdding a job inside a test is made easier as the program will fill in the values for contact and department. Once a job saves successfully, the program will automatically add the job's comments to the test comments.",
    "SAVE\nOnce you press save, watch as the program inputs the test into SMX for you, it will then wait for the test to complete before saving the results and returning to the item entry screen.",
    "FAILSAFE\nIf the program goes wrong, quickly move the mouse to any corner of the screen to activate the failsafe, this will show a popup confirming the failsafe activation.",
    "JOB PAGE\nWhen entering items, the location is taken into account to form the Job Page, this can be accessed by clicking the 'Jobs' button on the item entry screen.",
    "Each job you have entered while the program is open will show all the details including the assets that have been tested and any jobs raised.",
    "Click on the 'X' to remove a job or click on the '>' to add more assets to the job.",
]

_SECTIONS = {
    "Tutorial": _TUTORIAL,
    "Troubleshooting": _TROUBLESHOOTING,
    "Features": _FEATURES,
}


class TutorialPage(Page):
    def setup(self):
        if self.shared.storage.tutorial_complete:
            return self.change_page("CALIBRATION")
        self.width = 300
        self.sections = list(_SECTIONS.keys())
        self.current_section = 0
        self.setup_section(self.sections[self.current_section], _SECTIONS[self.sections[self.current_section]])

    def setup_section(self, section_name: str, *texts: list[str]):
        self.clear()
        ttk.Label(self.frame, text=section_name).grid(row=0, column=0, columnspan=3, sticky="ns")
        ttk.Button(self.frame, text="Skip", command=self.end_tutorial).grid(row=0, column=3, columnspan=1, sticky="e")

        row = 1
        for text_list in texts:
            for text in text_list:
                tkinter.Message(self.frame, width=self.width, text=text).grid(row=row, column=0, columnspan=4, sticky="w")
                row += 1

        back_present = False
        if self.current_section != 0:
            back_present = True
            ttk.Button(self.frame, text="Back", command=lambda: self.change_section(-1)).grid(row=row, column=0, columnspan=2, sticky="ns")
        ttk.Button(self.frame, text=f"{'Next' if self.current_section != len(_SECTIONS) - 1 else 'Go'}", command=self.change_section).grid(
            row=row, column=(2 if back_present else 0), columnspan=(2 if back_present else 4), sticky="ns"
        )

    def clear(self):
        for widget in self.frame.winfo_children():
            widget.destroy()

    def change_section(self, change: int = 1):
        self.current_section += change
        if self.current_section >= len(self.sections):
            self.end_tutorial()
        else:
            section = self.sections[self.current_section]
            self.setup_section(section, _SECTIONS[section])

    def end_tutorial(self):
        with self.shared.storage.edit() as storage:
            storage.tutorial_complete = True
        self.change_page("CALIBRATION")
