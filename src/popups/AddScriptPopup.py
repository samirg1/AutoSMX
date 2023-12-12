import tkinter
from typing import Callable

import customtkinter as ctk

from db.get_script import get_script
from db.get_tester_numbers import get_tester_numbers
from design.Script import Script
from design.data import SCRIPT_INFOS
from design.ScriptInfo import ScriptInfo
from popups.Popup import Popup
from popups.Tooltip import Tooltip
from storage.Storage import Storage
from utils.get_all_scripts import get_all_scripts
from utils.tkinter import show_error
from utils.constants import ADD_SCRIPT_POPUP_WIDTH, OFF, ON


class AddScriptPopup(Popup):
    def __init__(self, master: tkinter.Misc | None, storage: Storage, script: Script | None, callback: Callable[[], None] | None = None) -> None:
        super().__init__(master, "Add Script", width=ADD_SCRIPT_POPUP_WIDTH, height_factor=0.75, columns=8)
        self.storage = storage
        self.saved_script = script
        self.callback = callback

        ctk.CTkLabel(self.pop_frame, text="Script Basics").grid(column=0, row=0, columnspan=8, sticky=ctk.EW)
        number = ctk.StringVar(value=str(script.number) if script else "")
        number_label = ctk.CTkLabel(self.pop_frame, text="Number")
        number_label.grid(column=0, row=1)
        Tooltip(number_label, "The script number, this is shown on the right in SMX when viewing scripts")
        self.entry = ctk.CTkEntry(self.pop_frame, textvariable=number)
        self.entry.grid(column=1, row=1)

        self.tester_number = ctk.StringVar(value=script.tester_number if script else "")
        tester_label = ctk.CTkLabel(self.pop_frame, text="Tester Number")
        tester_label.grid(column=2, row=1)
        Tooltip(
            tester_label,
            "The default tester number to test with (e.g. 9999TEST, 11083TEST etc.) this shows up on the right in red when you select the script in SMX, you can edit this during testing.",
        )
        ctk.CTkEntry(self.pop_frame, textvariable=self.tester_number).grid(column=3, row=1)

        self.nickname = ctk.StringVar(value=script.nickname if script else "")
        nickname_label = ctk.CTkLabel(self.pop_frame, text="Nickname")
        nickname_label.grid(column=4, row=1)
        Tooltip(nickname_label, "Your own nickname for the script")
        nickname_entry = ctk.CTkEntry(self.pop_frame, textvariable=self.nickname)
        nickname_entry.grid(column=5, row=1)

        self.go = ctk.CTkButton(self.pop_frame, text="Go", command=lambda: self._get_script(number.get(), self.tester_number.get(), self.nickname.get()))
        self.go.grid(column=6, row=1)

        nickname_entry.bind("<Return>", lambda _: self.go.invoke())
        self.after(100, self.entry.focus)

        if self.saved_script:
            self.go.invoke()

    def _get_script(self, number: str, tester_number: str, nickname: str) -> None:
        self.entry.configure(state="disabled")
        self.go.configure(state="disabled")

        if tester_number == "":
            return self._show_error("Invalid input", "Tester number required")
        elif nickname == "":
            return self._show_error("Invalid input", "Nickname required")

        if tester_number not in get_tester_numbers():
            return self._show_error("Invalid tester number", f"Tester number '{tester_number}' not found for use for any user")

        if self.saved_script:
            self.script = self.saved_script
            script_info = ScriptInfo(self.saved_script.number, self.saved_script.tester_number, self.saved_script.nickname, {})
        else:
            try:
                script_number = int(number)
                script_info = ScriptInfo(script_number, tester_number, nickname, {})
                self.script = get_script(script_info)
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
        self.answers = tuple(ctk.StringVar(value=line.default) for line in self.script.lines)
        self.conditions = tuple(ctk.StringVar(value=ON if line.default == "1" else OFF) for line in self.script.lines)
        self.requireds = tuple(ctk.StringVar(value=ON if line.required else OFF) for line in self.script.lines)
        self.non_persistents = tuple(ctk.StringVar(value=ON if line.use_saved else OFF) for line in self.script.lines)
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
        self.non_persistents[i].set(OFF)

    def save_script(self, script_info: ScriptInfo) -> None:
        ticked_conditions: list[int] = []
        requireds: list[int] = []
        non_persistents: list[int] = []
        for line, cond, req, pers in zip(self.script.lines, self.conditions, self.requireds, self.non_persistents):
            if cond.get() == ON:
                ticked_conditions.append(line.z_rv)
                if req.get() == OFF:
                    return self._show_error("Invalid response", "Condition line must be required")
                if pers.get() == ON:
                    return self._show_error("Invalid response", "Condition line cannot be persistent")
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
            if line.options and line.options[0] == answer:
                continue
            line_defaults[line.z_rv] = answer

        added = ScriptInfo(
            script_info.number, self.tester_number.get(), self.nickname.get(), line_defaults, condition_line=condition_line, required_fields=requireds, non_persistent_fields=non_persistents
        )
        with self.storage.edit() as storage:
            is_editing_existing_script = self.saved_script is not None
            if not is_editing_existing_script:
                storage.added_script_infos.append(added)
            else:
                assert self.saved_script
                try:
                    old_script_index = next(i for i, info in enumerate(storage.added_script_infos) if info.number == self.saved_script.number)
                    storage.added_script_infos[old_script_index] = added
                except StopIteration:
                    storage.added_script_infos.append(added)

            storage.deleted_script_numbers.discard(added.number)

        get_all_scripts(self.storage.added_script_infos, self.storage.deleted_script_numbers)
        if self.callback:
            self.callback()
        self.destroy()

    def _show_error(self, title: str, message: str) -> None:
        show_error(title, message)
        self.focus()
