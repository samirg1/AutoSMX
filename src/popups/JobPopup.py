import tkinter
from typing import Callable, Iterable

import customtkinter as ctk

from db.get_parts import get_parts
from design.Job import Job
from design.Part import Part
from popups.Popup import Popup
from popups.SearchPartPopup import SearchPartPopup
from utils.constants import CTK_TEXT_START
from utils.tkinter import show_error


class JobPopup(Popup):
    def __init__(self, master: tkinter.Misc | None, default_dept: str, default_contact: str, room: str | None, save_job: Callable[[Job], None], previous_parts: Iterable[Part]) -> None:
        super().__init__(master, "Add Job", height_factor=0.5, columns=2)
        self.save_job = save_job
        self.room = room or "Not found"
        self.previous_parts = previous_parts

        ctk.CTkLabel(self.pop_frame, text="Department").grid(column=0, row=0)
        department = ctk.StringVar(value=default_dept)
        ctk.CTkEntry(self.pop_frame, textvariable=department).grid(column=1, row=0)

        ctk.CTkLabel(self.pop_frame, text="Contact Name").grid(column=0, row=1)
        contact = ctk.StringVar(value=default_contact)
        ctk.CTkEntry(self.pop_frame, textvariable=contact).grid(column=1, row=1)

        ctk.CTkLabel(self.pop_frame, text="Comment").grid(column=0, row=2, columnspan=2, sticky=ctk.EW)
        comment = tkinter.Text(self.pop_frame, height=4, width=100)
        self.after(100, comment.focus)
        comment.grid(column=0, row=3, columnspan=2)

        self.add_button = ctk.CTkButton(self.pop_frame, text="+", command=self._add_line)
        self.search_button = ctk.CTkButton(self.pop_frame, text="Search")
        self.save_button = ctk.CTkButton(self.pop_frame, text="Save", command=lambda: self._save_job(department.get(), contact.get(), comment.get(CTK_TEXT_START, ctk.END)))

        self.part_entries: list[tuple[ctk.StringVar, ctk.StringVar]] = []
        self.row = 6
        self._add_line()

        comment.bind("<Alt-s>", lambda _: self.save_button.invoke())
        comment.bind("<Alt-c>", lambda _: self.destroy())

    def _add_line(self) -> None:
        part_var = ctk.StringVar()
        self.part_entries.append((part_var, ctk.StringVar()))
        ctk.CTkLabel(self.pop_frame, text="Part Number").grid(column=0, row=self.row)
        ctk.CTkLabel(self.pop_frame, text="Quantity").grid(column=1, row=self.row)

        part_number = ctk.CTkEntry(self.pop_frame, textvariable=self.part_entries[len(self.part_entries) - 1][0])
        part_number.grid(column=0, row=self.row + 1)
        ctk.CTkEntry(self.pop_frame, textvariable=self.part_entries[len(self.part_entries) - 1][1]).grid(column=1, row=self.row + 1)
        part_label = ctk.CTkLabel(self.pop_frame, text="")
        part_label.grid(column=0, row=self.row + 2, columnspan=2)
        part_number.bind("<FocusOut>", lambda _: self._get_part(part_var, part_label))

        self.add_button.grid(column=0, row=self.row + 3)
        self.search_button.grid(column=1, row=self.row + 3)
        self.search_button.configure(command=lambda: self._search(part_var))

        self.save_button.grid(column=0, row=self.row + 4, columnspan=2)
        self.row += 4

    def _get_part(self, part_var: ctk.StringVar, part_label: ctk.CTkLabel) -> None:
        part = get_parts(part_var.get())
        part_label.configure(text="Part not found" if part is None else part.description)

    def _search(self, part_var: ctk.StringVar) -> None:
        SearchPartPopup(self, part_var, self.previous_parts)

    def _save_job(self, department: str, contact: str, comment: str) -> None:
        part_quantities: list[tuple[Part, int]] = []
        for pn, q in self.part_entries:
            part_number = pn.get()
            quantity = q.get()

            if part_number == "" and quantity == "":
                continue
            elif part_number == "":
                return self._show_error("Invalid Input", f"Part number required")
            elif quantity == "":
                return self._show_error("Invalid Input", f"Quantity required")

            if (part := get_parts(part_number)) is None:
                return self._show_error("Part not found", f"Part number '{part_number}' not found")
            try:
                if (number := int(quantity)) <= 0:
                    raise ValueError
            except ValueError:
                return self._show_error("Quantity invalid", f"Invalid quantity '{quantity}'")

            part_quantities.append((part, number))

        self.save_job(Job(department, contact, comment, self.room, part_quantities))
        self.destroy()

    def _show_error(self, title: str, message: str) -> None:
        show_error(title, message)  # type: ignore
        self.focus()
