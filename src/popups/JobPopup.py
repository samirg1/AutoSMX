import customtkinter as ctk
import tkinter
from typing import Callable, Iterable
from db.get_parts import get_parts

from design.Job import Job
from design.Part import Part
from popups.Popup import Popup
from popups.SearchPartPopup import SearchPartPopup
from utils.constants import CTK_TEXT_START


class JobPopup(Popup):
    def __init__(self, master: tkinter.Misc | None, default_dept: str, default_contact: str, save_job: Callable[[Job], None], previous_parts: Iterable[Part]):
        super().__init__(master, "Add Job", height_factor=0.5, columns=2)
        self.save_job = save_job
        self.previous_parts = previous_parts

        ctk.CTkLabel(self.frame, text="Department").grid(column=0, row=0)
        department = ctk.StringVar(value=default_dept)
        ctk.CTkEntry(self.frame, textvariable=department).grid(column=1, row=0)

        ctk.CTkLabel(self.frame, text="Contact Name").grid(column=0, row=1)
        contact = ctk.StringVar(value=default_contact)
        ctk.CTkEntry(self.frame, textvariable=contact).grid(column=1, row=1)

        ctk.CTkLabel(self.frame, text="Comment").grid(column=0, row=2, columnspan=2, sticky=ctk.EW)
        comment = tkinter.Text(self.frame, height=4, width=100)
        self.after(100, comment.focus)
        comment.grid(column=0, row=3, columnspan=2)

        self.add_button = ctk.CTkButton(self.frame, text="+", command=self._add_line)
        self.search_button = ctk.CTkButton(self.frame, text="Search")
        self.save_button = ctk.CTkButton(self.frame, text="Save", command=lambda: self._save_job(department.get(), contact.get(), comment.get(CTK_TEXT_START, ctk.END)))
        
        self.parts: list[tuple[ctk.StringVar, ctk.StringVar]] = []
        self.row = 6
        self._add_line()

        comment.bind("<Alt-s>", lambda _: self.save_button.invoke())
        comment.bind("<Alt-c>", lambda _: self.destroy())

    def _add_line(self) -> None:
        part_var = ctk.StringVar()
        self.parts.append((part_var, ctk.StringVar()))
        ctk.CTkLabel(self.frame, text="Part Number").grid(column=0, row=self.row)
        ctk.CTkLabel(self.frame, text="Quantity").grid(column=1, row=self.row)

        part_number = ctk.CTkEntry(self.frame, textvariable=self.parts[len(self.parts) - 1][0])
        part_number.grid(column=0, row=self.row + 1)
        ctk.CTkEntry(self.frame, textvariable=self.parts[len(self.parts) - 1][1]).grid(column=1, row=self.row + 1)
        part_label = ctk.CTkLabel(self.frame, text="")
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
        SearchPartPopup(self, part_var, self.previous_parts).mainloop()

    def _save_job(self, department: str, contact: str, comment: str) -> None:
        part_quantities: list[tuple[Part, int]] = []
        for part_number, quantity in self.parts:
            part_number = part_number.get()
            quantity = quantity.get()

            if part_number == "" and quantity == "":
                continue
            elif part_number == "":
                return self._show_error("Invalid Input", f"Part number required")
            elif quantity == "":
                return self._show_error("Invalid Input", f"Quantity required")
            
            part = get_parts(part_number)
            if part is None:
                return self._show_error("Part not found", f"Part number '{part_number}' not found")
            try:
                number = int(quantity)
                if number <= 0:
                    raise ValueError
            except ValueError:
                return self._show_error("Quantity invalid", f"Invalid quantity '{quantity}'")
            
            part_quantities.append((part, number))

        self.save_job(Job(department, contact, comment, part_quantities))
        self.destroy()

    def _show_error(self, title: str, message: str) -> None:
        tkinter.messagebox.showerror(title, message)  # type: ignore
        self.focus()