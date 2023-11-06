import tkinter
import customtkinter as ctk

from db.add_test import add_test
from db.edit_item import edit_item
from db.edit_test import edit_test
from db.get_items import get_items
from db.get_overall_results import get_overall_results
from design.Item import Item
from design.Job import Job
from design.Problem import Problem
from design.Script import Script
from design.Test import ScriptError, Test
from pages.Page import Page
from popups.JobPopup import JobPopup
from popups.OptionSelectPopup import OptionSelectPopup
from popups.ScriptSelectionPopup import ScriptSelectionPopup
from popups.Tooltip import Tooltip


class TestPage(Page):
    def setup(self) -> None:
        assert self.shared.problem
        self.test_problem: Problem = self.shared.problem

        problems_button = ctk.CTkButton(self.frame, text="< Problems", command=lambda: self.change_page("PROBLEM"))
        problems_button.grid(column=0, row=0, sticky="w")

        ctk.CTkLabel(self.frame, text="Item Number").grid(column=0, row=1, columnspan=2)
        item_number = ctk.StringVar(value=self.test_problem.previous_item_number)
        item_entry = ctk.CTkEntry(self.frame, textvariable=item_number)
        item_entry.grid(column=2, row=1, sticky="w", columnspan=2)
        item_entry.focus()
        item_entry.icursor(ctk.END)

        self.go_button = ctk.CTkButton(self.frame, text="Go", command=lambda: self.get_items(item_number.get(), item_entry))
        self.go_button.grid(column=0, row=2, columnspan=1)
        self.choose_button = ctk.CTkButton(self.frame, text="Choose", command=lambda: self.get_items(item_number.get(), item_entry, choose_script=True))
        self.choose_button.grid(column=1, row=2, columnspan=1)

        button_state = "normal" if self.is_tested(item_number.get()) else "disabled"
        self.edit_button = ctk.CTkButton(self.frame, text="Edit Test", command=lambda: self.get_items(item_number.get(), item_entry, editing=True), state=button_state)
        self.edit_button.grid(column=2, row=2)

        item_entry.bind("<Return>", lambda _: self.go_button.invoke())
        item_entry.bind("<Alt-c>", lambda _: self.choose_button.invoke())
        item_entry.bind("<Alt-e>", lambda _: self.edit_button.invoke())
        item_entry.bind("<Alt-b>", lambda _: problems_button.invoke())
        item_number.trace_add("write", lambda _, __, ___: self.edit_button_reconfigure(item_number))

    def is_tested(self, item_number: str):
        return len(self.test_problem.item_number_to_tests.get(item_number, [])) != 0

    def edit_button_reconfigure(self, item_number: ctk.StringVar) -> None:
        if self.is_tested(item_number.get()):
            self.edit_button.configure(state="normal")
        else:
            self.edit_button.configure(state="disabled")

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
        script_popup.mainloop()

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
        ctk.CTkEntry(self.frame, textvariable=self.item_room).grid(column=9, row=4)
        ctk.CTkButton(self.frame, text="Save", command=self.edit_item_room).grid(column=10, row=4)

        ctk.CTkLabel(self.frame, text=f"{self.test_problem}").grid(column=0, row=5, columnspan=20)
        ctk.CTkLabel(self.frame, text=f"{'-' * 600}").grid(column=0, row=6, columnspan=20)
        self.frame.rowconfigure(7, minsize=20)

        # displaying the script
        row = 8
        script = self.test.script
        ctk.CTkLabel(self.frame, text=f"{script.name} ({script.number}/{script.tester_number})").grid(column=0, row=row, columnspan=8)
        label_row = row + 1
        row += 1

        if test.completed:
            self.saved_script_answers = [line.result for line in test.script.lines]
        else:
            stored_answers = self.shared.storage.item_model_to_script_answers.get(self.test.item_model)
            self.saved_script_answers = stored_answers or [stest.default for stest in script.lines]
        actual_answers = [ctk.StringVar(value=ans) for ans in self.saved_script_answers]
        for i, line in enumerate(script.lines):
            label = ctk.CTkLabel(self.frame, text=line.text, width=10)
            Tooltip(label, text=line.text)
            label.grid(column=0, row=row, sticky=ctk.W)
            if len(line.options) <= 1:
                ctk.CTkEntry(self.frame, textvariable=actual_answers[i]).grid(column=2, row=row, columnspan=1, sticky="w")
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
            self.delete_job_button.grid(column=17, row=label_row, sticky=ctk.E)
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
        result = ctk.StringVar(value=self.test.result or overall_results[0].nickname)
        for i, (nickname, fullname) in enumerate(overall_results):
            button = ctk.CTkRadioButton(self.frame, text=nickname, variable=result, value=nickname)
            Tooltip(button, fullname)
            button.grid(column=i + 9, row=label_row, columnspan=1)
        self.frame.rowconfigure(label_row + 1, minsize=20)
        label_row += 2

        save = ctk.CTkButton(self.frame, text="Save", command=lambda: self.save_test([s.get() for s in actual_answers], result.get()))
        save.grid(column=9, row=label_row, columnspan=8)
        save.bind("<FocusIn>", lambda _: save.configure(text_color="black"))
        save.bind("<FocusOut>", lambda _: save.configure(text_color="white"))
        save.bind("<Return>", lambda _: self.save_test([s.get() for s in actual_answers], result.get()))
        save.bind("c", lambda _: self.go_button.invoke())
        if self.is_editing:
            remove_button = ctk.CTkButton(self.frame, text="Remove", command=self.remove_test)
            remove_button.grid(column=5, row=1, columnspan=1)
            save.bind("r", lambda _: remove_button.invoke())

        save.focus()
        label_row += 1

    def edit_item_room(self) -> None:
        item_room = self.item_room.get()
        if item_room != self.test.item.room:
            room = self.item_room.get() or None
            edit_item(self.test.item.number, {"room": room})
            self.test.item.set_room(room)

    def remove_test(self) -> None:
        self.test_problem.remove_test(self.test)
        for job in self.test.jobs:
            self.shared.job_manager.delete_job(self.test_problem, job)
        edit_test(self.test, self.test_problem, remove_only=True)
        return self.reset_page(self.test.item.number)

    def add_job(self) -> None:
        job_popup = JobPopup(self.frame, self.test_problem.department, self.test_problem.company, self.save_job)
        job_popup.mainloop()

    def save_job(self, job: Job) -> None:
        self.comment.insert(ctk.END, job.test_comment + "\n\n")
        self.test.add_job(job)
        self.shared.job_manager.add_job(self.test.item, self.test_problem, job)
        self.add_job_button.configure(text=f"Add Job ({len(self.test.jobs)})")
        self.delete_job_button.grid(column=3, row=self.add_job_button.grid_info()["row"], sticky="e")

    def delete_job(self) -> None:
        job = self.test.jobs.pop()
        self.shared.job_manager.delete_job(self.test_problem, job)
        current_comment = self.comment.get("1.0", ctk.END).strip()
        self.comment.delete("1.0", ctk.END)
        self.comment.insert(ctk.END, current_comment.replace(job.test_comment, ""))

        add_job_text = "Add Job"
        if not self.test.jobs:
            self.delete_job_button.grid_forget()
        else:
            add_job_text += f" ({len(self.test.jobs)})"
        self.add_job_button.configure(text=add_job_text)

    def save_test(self, script_answers: list[str], result: str) -> None:
        comment = self.comment.get("1.0", ctk.END)
        self.test.complete(comment, result, script_answers)
        if self.is_editing:
            self.test_problem.remove_test(self.test)
        self.test_problem.add_test(self.test)

        if self.is_editing:
            edit_test(self.test, self.test_problem)
        else:
            add_test(self.test, self.test_problem)

        self.edit_item_room()

        with self.shared.storage.edit() as storage:
            storage.total_tests += 1
            storage.test_breakdown[self.test.script.nickname] = storage.test_breakdown.get(self.test.script.nickname, 0) + 1

        if self.test.item.model not in (".", " ", "", "-", self.test.item.description, self.test.script.nickname) and self.test.script.nickname != "CLASS II":
            self.update_storage(script_answers)

        self.reset_page(self.test.item.number)

    def reset_page(self, item_number: str) -> None:
        self.test_problem.set_previous_item_number(item_number)
        self.change_page("TEST")

    def update_storage(self, actual_script_answers: list[str]) -> None:
        if self.saved_script_answers == actual_script_answers:
            return

        default = [stest.default for stest in self.test.script.lines]
        with self.shared.storage.edit() as storage:
            if actual_script_answers == default:
                del storage.item_model_to_script_answers[self.test.item_model]
            else:
                storage.item_model_to_script_answers[self.test.item_model] = actual_script_answers

    def item_not_found(self, current_item_number: str) -> None:
        tkinter.messagebox.showerror("Not Found", f"Item number '{current_item_number}'")  # type: ignore
        self.reset_page(current_item_number)
