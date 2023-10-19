import tkinter
from io import StringIO
from itertools import zip_longest
from tkinter import ttk
from tkinter.font import Font

from pages.Page import Page

_TUTORIAL = {
    "Quick Start": "After this tutorial you will be taken to the Job Page. \
        This is the first and main page of the application. \
            To add a job, click the '+' button on the top row, enter in the job number and then press Enter or hit 'Add' \
                This will take you to the item entry screen where you can input item numbers.",
    "Enter Asset": "Enter the item into the program, then click 'Go' / press Enter. \
        The program will then search for the item's script. \
            Do not press 'Choose' unless the program has failed to find the script or unless you need to choose a script different from normal.\
                The program will try and determine the script needed for this item, make sure this is correct before proceeding. \
                    The program will also determine the location information to keep as context to the tests.",
    "Edit Script": "Edit the script values, add a test-job by click the 'Add Job' button, add comments and anything else that is needed for the test. \
        The defaulted script values are those deemed to be the most common for the specific script. \
            If you change the script values from the default for a specifc item-model, the program will remember this next time you test that item-model.",
    "Adding a Test-Job": "Adding a test-job is made easier as the job information is used to fill in the contact and department fields. \
        Saving a job also pastes the comments from that job into the overall comments for the test (without any part numbers it can find). \
            If you accidentally add a job, press the 'X' button to delete the most recently added job. ",
    "Save Test": "Ensure values of the script are correct before clicking 'Save' (or press Enter straight away), this will save the test. \
        The program will wait for the test to complete, once it has, it will save the results and return to the item entry screen.",
    "Edit Test": "If you need to edit a test, enter the item number before clicking the 'Edit Test' button. \
        The program will ensure that you cannot edit a test that you have not completed. \
            Once you select edit, the script values will show as normal and you can edit and save them just like you would normally.",
    "Job Page": "Each job you have entered while the program is open will show all the details including the amount of tests, with a breakdown by script, and any jobs raised. \
        Select a job (or anything inside of it) and press the 'Enter Job' button to keep adding items into that job. \
            Select a job and press the 'Delete Job' button to remove the job from view. \
                To start add new job, press the '+' button, enter a job number and press 'Add'. \
                    These jobs that are displayed serve only as helpers to show test breakdowns and job's raised at each site, as well as help fill in test-job fields in the tests. ",
    "Troubleshooting": "If the program incorrectly selects the script, press 'Cancel' and then select 'Choose' to manually select the script. \
        If the program is glitching or bugging and you don't believe SMX is the issue, try restarting the program. \
            If the problem persists raise an issue by sending an email to the developer. \
                Please ensure you include any error messages as well as a description of the problem and how to reproduce it. \
                      If you need see this tutorial again, navigate to the 'Jobs' page and click on the Settings button to access it.",
}


class TutorialPage(Page):
    def setup(self) -> None:
        if self.shared.storage.tutorial_complete:
            return self.change_page("CALIBRATION")

        ttk.Label(self.frame, text="Tutorial Page").grid(row=0, column=0, sticky=tkinter.EW)
        ttk.Button(self.frame, text="Skip", command=self.end_tutorial).grid(row=0, column=3)

        self.frame.rowconfigure(1, minsize=20)

        # tree setup
        tree = ttk.Treeview(self.frame, columns=("#1"), show="tree", height=15, selectmode=tkinter.NONE)
        style = ttk.Style(self.frame)
        style.configure("Treeview", rowheight=60)  # pyright: ignore[reportUnknownMemberType]
        tree.column("#0", width=0)
        column = tree.column(tree["columns"][0])
        assert column

        for section_name, section in _TUTORIAL.items():
            section_node = tree.insert("", tkinter.END, values=(section_name,), open=True)
            text_lines = self.adjust_newlines(section, column["width"])
            for group in zip_longest(*(iter(text_lines),) * 3, fillvalue=" "):
                text = StringIO()
                for i, line in enumerate(group):
                    text.write(line + ("\n" if i != len(group) - 1 else ""))
                tree.insert(section_node, tkinter.END, values=(text.getvalue(),))

        scrollbar_y = ttk.Scrollbar(self.frame, orient=tkinter.VERTICAL, command=tree.yview)  # pyright: ignore
        tree.configure(yscroll=scrollbar_y.set)  # type: ignore
        scrollbar_y.grid(row=2, column=4, sticky=tkinter.NS)
        tree.grid(row=2, column=0, columnspan=4, sticky=tkinter.EW)

    def adjust_newlines(self, val: str, width: int) -> list[str]:
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

    def end_tutorial(self) -> None:
        with self.shared.storage.edit() as storage:
            storage.tutorial_complete = True
        self.change_page("CALIBRATION")
