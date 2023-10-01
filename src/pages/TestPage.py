import tkinter
from tkinter import StringVar, messagebox, ttk
from typing import cast

from pyautogui import FailSafeException

from design.Item import Item
from design.Job import Job
from design.Script import Script
from design.Test import TEST_RESULTS, ScriptError, Test
from design.TestJob import TestJob
from gui.actions import complete_test, turn_off_capslock
from db.get_items_jobs import get_items
from pages.Page import Page
from popups.ScriptSelectionPopup import ScriptSelectionPopup
from popups.TestJobPopup import TestJobPopup
from popups.OptionSelectPopup import OptionSelectPopup


class TestPage(Page):
    def setup(self) -> None:
        ttk.Button(self.frame, text="< Jobs", command=lambda: self.change_page("JOB")).grid(column=0, row=0, sticky="w")

        ttk.Label(self.frame, text="Item Number").grid(column=0, row=1, columnspan=2)
        item_number = StringVar(value=self.shared.previous_item_number)
        item_entry = ttk.Entry(self.frame, textvariable=item_number)
        item_entry.grid(column=2, row=1, sticky="w", columnspan=2)
        item_entry.focus()
        item_entry.icursor(tkinter.END)
        self.go_button = ttk.Button(self.frame, text="Go", command=lambda: self.get_items(item_number.get(), item_entry))
        item_entry.bind("<Return>", lambda _: self.go_button.invoke())
        self.go_button.grid(column=0, row=2, columnspan=2)
        self.choose_button = ttk.Button(self.frame, text="Choose", command=lambda: self.get_items(item_number.get(), item_entry, choose_script=True))
        self.choose_button.grid(column=2, row=2)
        button_state = "normal" if item_number.get() in self.shared.item_number_to_description else "disabled"
        self.edit_button = ttk.Button(self.frame, text="Edit Test", command=lambda: self.get_items(item_number.get(), item_entry, editing=True), state=button_state)
        self.edit_button.grid(column=3, row=2)

        item_number.trace_add("write", lambda _, __, ___: self.edit_button_reconfigure(item_number))

    def edit_button_reconfigure(self, item_number: StringVar) -> None:
        tested = item_number.get() in self.shared.item_number_to_description
        self.edit_button.configure(state=("normal" if tested else "disabled"))

    def get_items(self, item_number: str, item_entry: ttk.Entry, /, *, choose_script: bool = False, editing: bool = False) -> None:
        item_entry.state(["disabled"])  # pyright: ignore
        self.frame.focus()
        assert self.shared.job

        if editing and item_number not in self.shared.item_number_to_description:
            return self.item_not_found(item_number)

        items = get_items(item_number)
        if not items:
            return self.reset_page(item_number)
        self.is_editing = editing
        if len(items) == 1:
            return self.get_test(items[0], choose_script=choose_script)

        OptionSelectPopup(self.frame, items, lambda item: self.get_test(item, choose_script=choose_script))

    def get_test(self, item: Item, *, choose_script: bool = False) -> None:
        self.shared.item_number_to_description[item.number] = item.description
        if self.is_editing:
            assert self.shared.job
            try:
                test = next(test for test in reversed(self.shared.job.tests) if test.item.number == item.number)
            except StopIteration:
                return self.item_not_found(item.number)

        else:
            test = Test(item)

        try:
            if choose_script:
                raise ScriptError
            script = test.determine_script()
            self.display_test(script, test)
        except ScriptError:
            script_popup = ScriptSelectionPopup(self.frame, lambda s: self.display_test(s, test))
            script_popup.protocol("WM_DELETE_WINDOW", lambda: self.reset_page(item.number))
            script_popup.mainloop()

    def display_test(self, script: Script, test: Test) -> None:
        test.script = script
        self.test = test
        self.choose_button.destroy()
        self.edit_button.destroy()
        self.go_button.configure(text="Cancel", command=lambda: self.reset_page(test.item.number))
        self.go_button.grid(column=0, row=2, columnspan=4)

        # displaying the item and job
        ttk.Label(self.frame, text=f"{test.item}").grid(column=0, row=3, columnspan=4)
        ttk.Label(self.frame, text=f"{cast(Job, self.shared.job).campus}").grid(column=0, row=4, columnspan=4)
        ttk.Label(self.frame, text=f"{'-' * 50}").grid(column=0, row=5, columnspan=4)

        # displaying the script
        row = 6
        script = self.test.script
        ttk.Label(self.frame, text=f"{script.name}").grid(column=0, row=row, columnspan=4)
        row += 1

        if test.script_answers:
            self.saved_script_answers = test.script_answers
        else:
            stored_answers = self.shared.storage.item_model_to_script_answers.get(self.test.item_model)
            self.saved_script_answers = stored_answers or [stest.selected for stest in script.lines]
        actual_answers = [StringVar(value=ans) for ans in self.saved_script_answers]
        for i, line in enumerate(script.lines):
            ttk.Label(self.frame, text=f"{line.name}").grid(column=0, row=row, columnspan=1, sticky="w")
            if len(line.options) <= 1:
                ttk.Entry(self.frame, textvariable=actual_answers[i]).grid(column=1, row=row, columnspan=3, sticky="w")
            else:
                for j, option in enumerate(line.options):
                    rb = ttk.Radiobutton(self.frame, text=option, variable=actual_answers[i], value=option)
                    rb.grid(column=1 + j, row=row)
                    if option == self.saved_script_answers[i]:
                        rb.invoke()
            row += 1
        self.frame.rowconfigure(row, minsize=10)
        ttk.Label(self.frame, text=f"{'-' * 50}").grid(column=0, row=row, columnspan=4)
        row += 1

        # adding testjobs
        self.add_job_button = ttk.Button(self.frame, text="Add Job", command=self.add_testjob)
        self.delete_job_button = ttk.Button(self.frame, text="X", width=1, command=self.delete_test_job)
        self.add_job_button.grid(column=0, row=row, columnspan=4)
        if len(self.test.testjobs):
            self.add_job_button.configure(text=f"Add Job ({len(self.test.testjobs)})")
            self.delete_job_button.grid(column=3, row=self.add_job_button.grid_info()["row"], sticky="e")
        row += 1

        # test comment
        ttk.Label(self.frame, text="Comment").grid(column=0, row=row, columnspan=4)
        row += 1
        self.comment = tkinter.Text(self.frame, height=4, width=100)
        if self.test.comment:
            self.comment.insert(tkinter.END, self.test.comment + "\n\n")
        self.comment.grid(column=0, row=row, columnspan=4)
        row += 1
        self.frame.rowconfigure(row, minsize=10)
        row += 1

        # final results
        ttk.Label(self.frame, text="Result").grid(column=0, row=row, columnspan=4)
        row += 1
        result = tkinter.StringVar(value=self.test.final_result or TEST_RESULTS[0].result)
        for i, (name, test_result) in enumerate(TEST_RESULTS):
            button = ttk.Radiobutton(self.frame, text=name, variable=result, value=test_result)
            button.grid(column=i % 4, row=row)
            row = row + 1 if i % 4 == 3 else row
        row += 1

        save = ttk.Button(self.frame, text="Save", command=lambda: self.save_test([s.get() for s in actual_answers], result.get()))
        save.grid(column=0, row=row, columnspan=4)
        save.focus()
        save.bind("<Return>", lambda _: self.save_test([s.get() for s in actual_answers], result.get()))
        row += 1

    def add_testjob(self) -> None:
        assert self.shared.job is not None
        testjob_popup = TestJobPopup(self.frame, self.shared.job.department, self.shared.job.company, self.save_testjob)
        testjob_popup.mainloop()

    def save_testjob(self, testjob: TestJob) -> None:
        self.comment.insert(tkinter.END, testjob.test_comment + "\n\n")
        self.test.add_testjob(testjob)
        self.shared.testjob_manager.add_testjob(self.test.item, cast(Job, self.shared.job), testjob)
        self.add_job_button.configure(text=f"Add Job ({len(self.test.testjobs)})")
        self.delete_job_button.grid(column=3, row=self.add_job_button.grid_info()["row"], sticky="e")

    def delete_test_job(self) -> None:
        testjob = self.test.testjobs.pop()
        self.shared.testjob_manager.delete_testjob(cast(Job, self.shared.job), testjob)
        current_comment = self.comment.get("1.0", tkinter.END).strip()
        self.comment.delete("1.0", tkinter.END)
        self.comment.insert(tkinter.END, current_comment.replace(testjob.test_comment, ""))

        add_job_text = "Add Job"
        if not self.test.testjobs:
            self.delete_job_button.grid_forget()
        else:
            add_job_text += f" ({len(self.test.testjobs)})"
        self.add_job_button.configure(text=add_job_text)

    def save_test(self, script_answers: list[str], result: str) -> None:
        assert self.shared.job  # must have created a job by now
        turn_off_capslock()
        comment = self.comment.get("1.0", tkinter.END)
        self.test.complete(comment, result, script_answers)
        if self.is_editing:
            self.shared.job.remove_test(self.test)
        self.shared.job.add_test(self.test)

        try:
            complete_test(self.test, self.shared.storage.positions, self.is_editing)
        except FailSafeException:
            test = self.shared.job.tests.pop()
            self.shared.job.test_breakdown[test.script.nickname] -= 1
            for _ in test.testjobs:
                self.shared.testjob_manager.job_to_testjobs[self.shared.job].pop()
            return self.failsafe(self.test.item.number)

        with self.shared.storage.edit() as storage:
            storage.total_tests += 1
            storage.test_breakdown[self.test.script.nickname] = storage.test_breakdown.get(self.test.script.nickname, 0) + 1

        if self.test.item.model not in (".", " ", "", "-", self.test.item.description, self.test.script.nickname):
            self.update_storage(script_answers)

        self.reset_page(self.test.item.number)

    def reset_page(self, item_number: str) -> None:
        self.shared.previous_item_number = item_number
        self.change_page("TEST")

    def update_storage(self, actual_script_answers: list[str]) -> None:
        if self.saved_script_answers == actual_script_answers:
            return

        default = [stest.selected for stest in self.test.script.lines]
        with self.shared.storage.edit() as storage:
            if actual_script_answers == default:
                del storage.item_model_to_script_answers[self.test.item_model]
            else:
                storage.item_model_to_script_answers[self.test.item_model] = actual_script_answers

    def failsafe(self, current_item_number: str) -> None:
        messagebox.showerror("Process Aborted", "Fail safe activated")  # pyright: ignore
        self.reset_page(current_item_number)

    def item_not_found(self, current_item_number: str) -> None:
        messagebox.showerror("Not Found", f"Item number '{current_item_number}' not tested yet")  # pyright: ignore
        self.reset_page(current_item_number)
