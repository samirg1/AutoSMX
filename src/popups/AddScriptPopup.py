import tkinter

import customtkinter as ctk

from db.get_script import get_script
from design.data import CONDITION_LINES, LINE_DEFAULTS, NON_PERSISTENT_LINES, REQUIRED_FREE_TEXT_FIELDS, SCRIPT_INFOS, get_all_scripts
from design.ScriptInfo import AddedScript, ScriptInfo
from popups.Popup import Popup
from popups.Tooltip import Tooltip
from storage.Storage import Storage
from utils.constants import OFF, ON


class AddScriptPopup(Popup):
    def __init__(self, master: tkinter.Misc | None, storage: Storage):
        super().__init__(master, "Add Script", width=360 * 3, height_factor=0.75, columns=8)
        self.storage = storage

        ctk.CTkLabel(self.pop_frame, text="Script Basics").grid(column=0, row=0, columnspan=8, sticky=ctk.EW)
        number = ctk.StringVar()
        number_label = ctk.CTkLabel(self.pop_frame, text="Number")
        number_label.grid(column=0, row=1)
        Tooltip(number_label, "The script number, this is shown on the right in SMX")
        entry = ctk.CTkEntry(self.pop_frame, textvariable=number)
        entry.grid(column=1, row=1)
        tester_number = ctk.StringVar()
        tester_label = ctk.CTkLabel(self.pop_frame, text="Tester Number")
        tester_label.grid(column=2, row=1)
        Tooltip(tester_label, "Tester number to test with (e.g. 9999TEST) this shows up on the left when you select the script in SMX")
        ctk.CTkEntry(self.pop_frame, textvariable=tester_number).grid(column=3, row=1)
        nickname = ctk.StringVar()
        nickname_label = ctk.CTkLabel(self.pop_frame, text="Nickname")
        nickname_label.grid(column=4, row=1)
        Tooltip(nickname_label, "Your own nickname for the script")
        nickname_entry = ctk.CTkEntry(self.pop_frame, textvariable=nickname)
        nickname_entry.grid(column=5, row=1)
        go = ctk.CTkButton(self.pop_frame, text="Go", command=lambda: self._get_script(number.get(), tester_number.get(), nickname.get()))
        go.grid(column=6, row=1)

        nickname_entry.bind("<Return>", lambda _: go.invoke())
        self.after(100, entry.focus)

    def _get_script(self, number: str, tester_number: str, nickname: str) -> None:
        if tester_number == "":
            return self._show_error("Invalid input", "Tester number required")
        elif nickname == "":
            return self._show_error("Invalid input", "Nickname required")

        try:
            script_number = int(number)
            script_info = ScriptInfo(script_number, tester_number, nickname, [], [])
            self.script = get_script(script_info, {}, set(), set(), set())
        except ValueError:
            return self._show_error("Invalid Number", f"Invalid script number '{number}'")

        if any(info.number == script_number for info in SCRIPT_INFOS):
            return self._show_error("Invalid Number", f"Script number already present '{number}'")

        default_label = ctk.CTkLabel(self.pop_frame, text="Default values")
        default_label.grid(row=2, column=0, columnspan=3, sticky=ctk.EW)
        Tooltip(default_label, "Change the default values for the script lines that will show for this script")
        condition_label = ctk.CTkLabel(self.pop_frame, text="Condition Line?")
        condition_label.grid(row=2, column=3, sticky=ctk.W)
        Tooltip(condition_label, "Mark this field as a condition line (required) and has default value of '1'")
        required_label = ctk.CTkLabel(self.pop_frame, text="Required?")
        required_label.grid(row=2, column=4, sticky=ctk.W)
        Tooltip(required_label, "Mark this field as required")
        persistent_label = ctk.CTkLabel(self.pop_frame, text="Persistent?")
        persistent_label.grid(row=2, column=5, sticky=ctk.W)
        Tooltip(persistent_label, "If this line value changes from default for a specific item-model, persist this value as default for the item-model")

        row = 3
        self.answers = [ctk.StringVar(value=line.default) for line in self.script.lines]
        self.conditions = [ctk.StringVar(value=OFF) for _ in self.script.lines]
        self.requireds = [ctk.StringVar(value=OFF) for _ in self.script.lines]
        self.non_persistents = [ctk.StringVar(value=ON) for _ in self.script.lines]
        for i, line in enumerate(self.script.lines):
            label = ctk.CTkLabel(self.pop_frame, text=line.text, width=10)
            Tooltip(label, text=line.text)
            label.grid(column=0, row=row, sticky=ctk.W)
            if len(line.options) <= 1:
                ctk.CTkEntry(self.pop_frame, textvariable=self.answers[i]).grid(column=2, row=row, columnspan=1, sticky=ctk.W)
            else:
                ctk.CTkSegmentedButton(self.pop_frame, values=list(line.options), variable=self.answers[i]).grid(column=2, row=row, columnspan=1)

            if len(line.options) <= 1:
                ctk.CTkCheckBox(self.pop_frame, text="", variable=self.conditions[i], onvalue=ON, offvalue=OFF, width=1, command=lambda i=i: self.set_required(i)).grid(  # type: ignore[misc]
                    column=3, row=row, sticky=ctk.EW
                )
                ctk.CTkCheckBox(self.pop_frame, text="", variable=self.requireds[i], onvalue=ON, offvalue=OFF, width=1).grid(column=4, row=row, sticky=ctk.EW)
            ctk.CTkCheckBox(self.pop_frame, text="", variable=self.non_persistents[i], onvalue=ON, offvalue=OFF, width=1).grid(column=5, row=row, sticky=ctk.EW)
            row += 1

        ctk.CTkButton(self.pop_frame, text="Save Script", command=lambda: self.save_script(script_info)).grid(row=row, column=0, columnspan=8, sticky=ctk.EW)

    def set_required(self, i: int) -> None:
        self.requireds[i].set(ON)

    def save_script(self, script_info: ScriptInfo) -> None:
        ticked_conditions: list[int] = []
        requireds: list[int] = []
        non_persistents: list[int] = []
        for line, cond, req, pers in zip(self.script.lines, self.conditions, self.requireds, self.non_persistents):
            if cond.get() == ON:
                ticked_conditions.append(line.z_rv)
                if req.get() == OFF:
                    return self._show_error("Invalid response", "Condition line must be required")
            if req.get() == ON:
                requireds.append(line.z_rv)
            if pers.get() == OFF:
                non_persistents.append(line.z_rv)

        if len(ticked_conditions) > 1:
            return self._show_error("Invalid response", "Can only have one condition line")
        condition_line = None if not len(ticked_conditions) else ticked_conditions[0]

        line_defaults: dict[int, str] = {}
        for line, a in zip(self.script.lines, self.answers):
            answer = a.get()
            if line.default == answer:
                continue
            line_defaults[line.z_rv] = answer

        added = AddedScript(script_info, condition_line, line_defaults, requireds, non_persistents)
        with self.storage.edit() as storage:
            storage.added_scripts.append(added)

        get_all_scripts.cache_clear()
        SCRIPT_INFOS.append(script_info)
        if condition_line is not None:
            CONDITION_LINES.add(condition_line)
        LINE_DEFAULTS.update(line_defaults)
        REQUIRED_FREE_TEXT_FIELDS.update(requireds)
        NON_PERSISTENT_LINES.update(non_persistents)
        get_all_scripts()

        self.destroy()

    def _show_error(self, title: str, message: str) -> None:
        tkinter.messagebox.showerror(title, message)  # type: ignore
        self.focus()
