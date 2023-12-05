import tkinter

import customtkinter as ctk

from db.add_test import add_test
from db.edit_item import edit_item
from db.edit_test import edit_test
from db.get_items import get_items
from db.get_new_test_id import NoTestIDsError
from db.get_overall_results import get_overall_results
from design.Item import Item
from design.Job import Job
from design.Script import InvalidTesterNumberError, Script
from design.Test import InvalidTestResultError, ScriptError, Test
from pages.Page import Page
from popups.JobPopup import JobPopup
from popups.OptionSelectPopup import OptionSelectPopup
from popups.ScriptSelectionPopup import ScriptSelectionPopup
from popups.Tooltip import Tooltip
from utils.add_focus_bindings import add_focus_bindings
from utils.constants import CTK_TEXT_START, DEFAULT_TEXT_COLOUR_LABEL, ERROR_TEXT_COLOUR_LABEL, HORIZONTAL_LINE
from utils.show_error import show_error


class TestPage(Page):
    def setup(self) -> None:
        assert self.storage.problem
        self.test_problem = self.storage.problem

        problems_button = ctk.CTkButton(self.frame, text="< Problems", command=lambda: self.change_page("PROBLEM"))
        problems_button.grid(column=0, row=0, sticky=ctk.W)

        ctk.CTkLabel(self.frame, text="Item Number").grid(column=0, row=1, columnspan=2)
        item_number = ctk.StringVar(value=self.test_problem.previous_item_number)
        item_entry = ctk.CTkEntry(self.frame, textvariable=item_number)
        item_entry.grid(column=2, row=1, sticky=ctk.W, columnspan=2)
        item_entry.focus()
        item_entry.icursor(ctk.END)

        self.go_button = ctk.CTkButton(self.frame, text="Go", command=lambda: self.get_items(item_number.get(), item_entry))
        self.go_button.grid(column=0, row=2, columnspan=1)
        self.choose_button = ctk.CTkButton(self.frame, text="Choose", command=lambda: self.get_items(item_number.get(), item_entry, choose_script=True))
        self.choose_button.grid(column=1, row=2, columnspan=1)

        self.tooltip: Tooltip | None = None
        self.edit_button = ctk.CTkButton(self.frame, text="Edit Test", command=lambda: self.get_items(item_number.get(), item_entry, editing=True))
        self.edit_button.grid(column=2, row=2)
        self.edit_button_reconfigure(item_number)

        item_entry.bind("<Return>", lambda _: self.go_button.invoke())
        item_entry.bind("<Alt-c>", lambda _: self.choose_button.invoke())
        item_entry.bind("<Alt-e>", lambda _: self.edit_button.invoke())
        item_entry.bind("<Alt-b>", lambda _: problems_button.invoke())
        item_number.trace_add("write", lambda _, __, ___: self.edit_button_reconfigure(item_number))

    def is_tested(self, item_number: str) -> bool:
        return len(self.test_problem.item_number_to_tests.get(item_number, [])) != 0

    def edit_button_reconfigure(self, item_number: ctk.StringVar) -> None:
        if self.tooltip:
            self.tooltip.remove()
        if self.is_tested(item_number.get()):
            self.edit_button.configure(state="normal")
            self.tooltip = None
        else:
            self.edit_button.configure(state="disabled")
            possibles = [number for number, lst in self.test_problem.item_number_to_tests.items() if number.startswith(item_number.get()) and len(lst)]
            if len(possibles) == 1:
                self.tooltip = Tooltip(self.edit_button, f"Did you mean '{possibles[0]}'")

    def get_items(self, item_number: str, item_entry: ctk.CTkEntry, /, *, choose_script: bool = False, editing: bool = False) -> None:
        item_entry.configure(state="disabled")
        self.frame.focus()

        if editing and item_number not in self.test_problem.item_number_to_tests:
            return self.item_not_found(item_number)

        items = get_items(item_number)
        if not items:
            return self.item_not_found(item_number)
        self.is_editing = editing
        if len(items) == 1:
            return self.get_test(items[0], choose_script=choose_script)

        popup = OptionSelectPopup(self.frame, items, lambda item: self.get_test(item, choose_script=choose_script), width=360)
        popup.protocol("WM_DELETE_WINDOW", lambda: self.reset_page(item_number))

    def get_test(self, item: Item, *, choose_script: bool = False) -> None:
        if not self.is_editing:
            return self.get_script(Test(item), choose_script)

        possible_tests = self.test_problem.item_number_to_tests.get(item.number, None)
        if possible_tests is None:
            return self.item_not_found(item.number)

        if len(possible_tests) == 1:
            return self.get_script(possible_tests[0], choose_script)

        popup = OptionSelectPopup(self.frame, possible_tests, lambda test: self.get_script(test, choose_script), display=lambda test: f"{test.script.nickname} - {test.date}")
        popup.protocol("WM_DELETE_WINDOW", lambda: self.reset_page(item.number))

    def get_script(self, test: Test, choose_script: bool) -> None:
        try:
            if not hasattr(test, "script"):
                if choose_script:
                    raise ScriptError
                test.script = test.determine_script()
            return self.display_test(test)
        except ScriptError:
            pass

        script_popup = ScriptSelectionPopup(self.frame, lambda s: self.display_test(test, s))
        script_popup.protocol("WM_DELETE_WINDOW", lambda: self.reset_page(test.item.number))

    def display_test(self, test: Test, script: Script | None = None) -> None:
        if script is not None:
            test.script = script
        self.test = test
        self.choose_button.destroy()
        self.edit_button.destroy()
        self.go_button.configure(text="Cancel", command=lambda: self.reset_page(test.item.number))
        self.go_button.grid(column=4, row=1)

        # displaying the item and problem
        item_label = ctk.CTkLabel(self.frame, text=f"{test.item.full_info}")
        item_label.grid(column=0, row=3, columnspan=20)
        ctk.CTkLabel(self.frame, text="Room: ").grid(column=8, row=4)
        self.item_room = ctk.StringVar(value=test.item.room)
        room_entry = ctk.CTkEntry(self.frame, textvariable=self.item_room)
        room_entry.grid(column=9, row=4)
        ctk.CTkButton(self.frame, text="Save", command=self.edit_item_room).grid(column=10, row=4)

        ctk.CTkLabel(self.frame, text=f"{self.test_problem}").grid(column=0, row=5, columnspan=20)
        ctk.CTkLabel(self.frame, text=HORIZONTAL_LINE).grid(column=0, row=6, columnspan=20)
        self.frame.rowconfigure(7, minsize=20)

        # displaying the script
        row = 8
        script = self.test.script
        ctk.CTkLabel(self.frame, text=f"{script.name} #{script.number}").grid(column=0, row=row, columnspan=8)
        self.tester_number = ctk.StringVar(value=script.tester_number)
        ctk.CTkEntry(self.frame, textvariable=self.tester_number).grid(column=9, row=row)
        label_row = row + 1
        row += 1

        if script.nickname == "CEILING" and test.item.manufacturer == "MOLIFT":
            line = next(line for line in script.lines if line.number == 19)
            line.required = True
            line.default = ""

        if test.completed:
            self.saved_script_answers = [line.result for line in test.script.lines]
        else:
            stored_answers = self.storage.item_model_to_script_answers.get(self.test.item_model)
            self.saved_script_answers = stored_answers or [stest.default for stest in script.lines]

        actual_answers = [ctk.StringVar(value=ans) for ans in self.saved_script_answers]
        for i, line in enumerate(script.lines):
            label = ctk.CTkLabel(self.frame, text=line.text, width=10, text_color=(ERROR_TEXT_COLOUR_LABEL if line.required else DEFAULT_TEXT_COLOUR_LABEL))
            Tooltip(label, text=line.text)
            label.grid(column=0, row=row, sticky=ctk.W)
            if len(line.options) <= 1:
                ctk.CTkEntry(self.frame, textvariable=actual_answers[i]).grid(column=2, row=row, columnspan=1, sticky=ctk.W)
            else:
                ctk.CTkSegmentedButton(self.frame, values=list(line.options), variable=actual_answers[i]).grid(column=2, row=row, columnspan=1)
            row += 1

        self.frame.rowconfigure(row, minsize=20)
        row += 3

        # adding jobs
        self.add_job_button = ctk.CTkButton(self.frame, text="Add Job", command=self.add_job)
        self.delete_job_button = ctk.CTkButton(self.frame, text="X", width=1, command=self.delete_job)
        self.add_job_button.grid(column=9, row=label_row, columnspan=8)
        if len(self.test.jobs):
            self.add_job_button.configure(text=f"Add Job ({len(self.test.jobs)})")
            self.delete_job_button.grid(column=15, row=label_row, sticky=ctk.E)
        self.frame.rowconfigure(label_row + 1, minsize=20)
        label_row += 2

        # test comment
        ctk.CTkLabel(self.frame, text="Comment").grid(column=9, row=label_row, columnspan=8)
        label_row += 1
        self.comment = tkinter.Text(self.frame, height=4)
        if self.test.comments:
            self.comment.insert(ctk.END, self.test.comments + "\n\n")
        self.comment.grid(column=9, row=label_row, columnspan=8, rowspan=3)
        label_row += 3
        self.frame.rowconfigure(label_row, minsize=20)
        label_row += 1

        # final results
        ctk.CTkLabel(self.frame, text="Result").grid(column=9, row=label_row, columnspan=8)
        label_row += 1
        overall_results = get_overall_results(int(self.test_problem.customer_number))
        value = self.test.result or (overall_results[0].nickname if self.storage.skip_overall_result_check else "")
        result = ctk.StringVar(value=value)
        for i, (nickname, fullname) in enumerate(overall_results):
            button = ctk.CTkRadioButton(self.frame, text=nickname, variable=result, value=nickname)
            Tooltip(button, fullname)
            button.grid(column=i + 9, row=label_row, columnspan=1)
        self.frame.rowconfigure(label_row + 1, minsize=20)
        label_row += 2

        save = ctk.CTkButton(self.frame, text="Save", command=lambda: self.save_test([s.get() for s in actual_answers], result.get()))
        save.grid(column=9, row=label_row, columnspan=8)
        room_entry.bind("<Return>", lambda _: save.invoke())
        add_focus_bindings(save)
        save.bind("<Return>", lambda _: save.invoke())
        save.bind("c", lambda _: self.go_button.invoke())
        save.bind("j", lambda _: self.add_job_button.invoke())
        save.bind("d", lambda _: self.delete_job_button.invoke())
        if self.is_editing:
            remove_button = ctk.CTkButton(self.frame, text="Remove", command=self.remove_test)
            remove_button.grid(column=5, row=1, columnspan=10, sticky=ctk.W)
            save.bind("r", lambda _: remove_button.invoke())
        for i, (nickname, _) in enumerate(overall_results, start=1):
            save.bind(f"{i}", lambda _, nickname=nickname: result.set(nickname))  # type: ignore[misc]

        save.focus()
        label_row += 1

    def edit_item_room(self) -> None:
        with self.storage.edit():
            item_room = self.item_room.get()
            if item_room != self.test.item.room:
                room = item_room or None
                edit_item(self.test.item.number, {"room": room})
                self.test.item.set_room(room)

    def remove_test(self) -> None:
        with self.storage.edit() as storage:
            self.test_problem.remove_test(self.test)

            for job in self.test.jobs:
                storage.job_manager.delete_job(self.test_problem, job)
        edit_test(self.test, self.test_problem, remove_only=True)
        return self.reset_page(self.test.item.number)

    def add_job(self) -> None:
        JobPopup(self.frame, self.test_problem.department or "", self.test_problem.company, self.save_job, self.storage.previous_parts)

    def save_job(self, job: Job) -> None:
        self.comment.insert(ctk.END, job.test_comment + "\n\n")
        with self.storage.edit() as storage:
            self.test.add_job(job)
            storage.job_manager.add_job(self.test.item, self.test_problem, job)
            for part, _ in job.part_quantities:
                storage.previous_parts.add(part)
        self.add_job_button.configure(text=f"Add Job ({len(self.test.jobs)})")
        self.delete_job_button.grid(column=15, row=self.add_job_button.grid_info()["row"], sticky=ctk.E)

    def delete_job(self) -> None:
        if len(self.test.jobs) == 0:
            return
        with self.storage.edit() as storage:
            job = self.test.jobs.pop()
            storage.job_manager.delete_job(self.test_problem, job)
        current_comment = self.comment.get(CTK_TEXT_START, ctk.END).strip()
        self.comment.delete(CTK_TEXT_START, ctk.END)
        self.comment.insert(ctk.END, current_comment.replace(job.test_comment, ""))

        add_job_text = "Add Job"
        if not self.test.jobs:
            self.delete_job_button.grid_forget()
        else:
            add_job_text += f" ({len(self.test.jobs)})"
        self.add_job_button.configure(text=add_job_text)

    def save_test(self, script_answers: list[str], result: str) -> None:
        try:
            self.test.script.set_tester_number(self.tester_number.get())
        except InvalidTesterNumberError as e:
            return show_error("Invalid tester number", f"{e}")
        
        self.test.script.set_tester_number(self.tester_number.get())
        comment = self.comment.get(CTK_TEXT_START, ctk.END)
        with self.storage.edit():
            try:
                self.test.complete(comment, result, script_answers)
            except InvalidTestResultError as e:
                return show_error("Invalid Answers", f"{e}") 
            except NoTestIDsError:
                return show_error("Error occured", "No test IDs left, perform a manual sync")
            if self.is_editing:
                self.test_problem.remove_test(self.test)
            self.test_problem.add_test(self.test)

        if self.is_editing:
            edit_test(self.test, self.test_problem)
        else:
            add_test(self.test, self.test_problem)

        self.edit_item_room()

        with self.storage.edit() as storage:
            storage.total_tests += 1
            storage.test_breakdown[self.test.script.nickname] = storage.test_breakdown.get(self.test.script.nickname, 0) + 1

        if self.test.item.model not in (".", " ", "", "-", self.test.item.description, self.test.script.nickname) and self.test.script.nickname != "CLASS II":
            self.update_storage(script_answers)

        self.reset_page(self.test.item.number)

    def reset_page(self, item_number: str) -> None:
        with self.storage.edit():
            self.test_problem.set_previous_item_number(item_number)
        self.change_page("TEST")

    def update_storage(self, actual_script_answers: list[str]) -> None:
        for i, (line, answer) in enumerate(zip(self.test.script.lines, actual_script_answers)):
            if not line.use_saved or answer == "Fail":
                actual_script_answers[i] = line.default

        if self.saved_script_answers == actual_script_answers:
            return

        default = [stest.default for stest in self.test.script.lines]
        with self.storage.edit() as storage:
            if actual_script_answers == default:
                storage.item_model_to_script_answers.pop(self.test.item_model, None)
            else:
                storage.item_model_to_script_answers[self.test.item_model] = actual_script_answers

    def item_not_found(self, current_item_number: str) -> None:
        show_error("Not Found", f"Item number '{current_item_number}'")
        self.reset_page(current_item_number)
