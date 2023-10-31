import tkinter
from tkinter import ttk

from design.Problem import Problem
from pages.Page import Page
from popups.ProblemEntryPopup import ProblemEntryPopup
from popups.SyncPopup import SyncPopup


class ProblemPage(Page):
    def setup(self) -> None:
        # top row
        ttk.Label(self.frame, text="Problems").grid(column=0, row=0, columnspan=1)
        add_button = ttk.Button(self.frame, text="+", command=self.add_tests)
        add_button.grid(column=1, row=0, columnspan=1)
        add_button.focus()
        add_button.bind("<Return>", lambda _: add_button.invoke())
        ttk.Button(self.frame, text="Settings", command=lambda: self.change_page("SETTINGS")).grid(column=2, row=0, columnspan=2)
        ttk.Label(self.frame, text=f"{'-' * 50}").grid(column=0, row=1, columnspan=4)
        row = 2

        # tree setup
        tree = ttk.Treeview(self.frame, columns=("text", "number"), show="tree headings", height=10, selectmode="browse")
        style = ttk.Style(self.frame)
        style.configure("Treeview", rowheight=60)  # pyright: ignore
        tree.column("#0", width=0)
        tree.column("text", anchor=tkinter.W)
        tree.column("number", width=10, anchor=tkinter.CENTER)
        tree.heading("text", text="Jobs")
        tree.heading("number", text="#")

        # default
        if not self.shared.problems:
            tree.insert("", tkinter.END, values=("No problems yet, click '+' to add",))
            tree.configure(selectmode="none")

        # add each problem to the tree
        for campus, problem in self.shared.problems.items():
            problem_node = tree.insert("", tkinter.END, campus, values=(f"{problem}",))

            if problem.open_problems:
                open_problem_node = tree.insert(problem_node, tkinter.END, values=("Open Problems", len(problem.open_problems)))
                for open_problem in problem.open_problems:
                    tree.insert(open_problem_node, tkinter.END, values=(f"{open_problem}",))

            problem_jobs = self.shared.job_manager.problem_to_jobs.get(problem, [])
            if problem_jobs:
                job_node = tree.insert(problem_node, tkinter.END, values=("Jobs Raised", len(problem_jobs)))
                for job in problem_jobs:
                    item = self.shared.job_manager.job_to_item[job]
                    first_line = str(job).split("\n")[0]
                    tree.insert(job_node, tkinter.END, values=(f"{first_line}\n{item.description}\n{item.number}",))

            if problem.tests:
                test_node = tree.insert(problem_node, tkinter.END, values=("Tests", f"{len(problem.tests)}"))
                for script_name, value in problem.test_breakdown.items():
                    tree.insert(test_node, tkinter.END, values=(f"{script_name}", value))

        # completing tree setup
        scrollbar = ttk.Scrollbar(self.frame, orient=tkinter.VERTICAL, command=tree.yview)  # pyright: ignore
        tree.configure(yscroll=scrollbar.set)  # type: ignore
        scrollbar.grid(row=row, column=4, sticky=tkinter.NS)
        tree.grid(row=row, column=0, columnspan=4, sticky=tkinter.EW)
        row += 1

        # add job manipulation buttons
        button1 = ttk.Button(self.frame, text="Enter Problem", command=lambda: self.add_tests(tree), state="disabled")
        button1.grid(row=row, column=0, columnspan=4)
        button2 = ttk.Button(self.frame, text="Delete Problem", command=lambda: self.delete_problem(tree), state="disabled")
        button2.grid(row=row + 1, column=0, columnspan=4)
        row += 2

        tree.bind("<<TreeviewSelect>>", lambda _: self.on_first_select(tree, button1, button2))

        self.frame.rowconfigure(row, minsize=10)
        ttk.Label(self.frame, text=f"{'-' * 50}").grid(column=0, row=row+1, columnspan=4)
        row += 2

        ttk.Button(self.frame, text="Sync", command=self.sync).grid(row=row, column=0, columnspan=4)
        row += 1
        
    def on_first_select(self, tree: ttk.Treeview, *buttons: ttk.Button) -> None:
        for button in buttons:
            button.configure(state="normal")
        tree.unbind("<<TreeviewSelect>>")

    def get_selected_problem(self, tree: ttk.Treeview) -> Problem:
        item = tree.focus()
        possible_parent1 = tree.parent(item)
        parent1 = possible_parent1 if possible_parent1 else item
        possible_parent2 = tree.parent(parent1)
        parent2 = possible_parent2 if possible_parent2 else parent1

        return self.shared.problems[parent2]

    def delete_problem(self, tree: ttk.Treeview) -> None:
        problem = self.get_selected_problem(tree)
        del self.shared.problems[problem.campus]
        if problem in self.shared.job_manager.problem_to_jobs:
            del self.shared.job_manager.problem_to_jobs[problem]
        self.change_page("PROBLEM")

    def add_tests(self, tree: ttk.Treeview | None = None) -> None:
        if tree is None:
            ProblemEntryPopup(self.frame, lambda problem: self.add_problem(problem))
        else:
            self.add_problem(self.get_selected_problem(tree))

    def add_problem(self, problem: Problem) -> None:
        self.shared.problem = problem
        self.shared.problems[problem.campus] = problem
        self.change_page("TEST")

    def sync(self):
        SyncPopup(self.frame, self.shared.problem).mainloop()
