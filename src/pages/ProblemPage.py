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
        add_button.grid(column=15, row=0, columnspan=1)
        add_button.focus()
        add_button.bind("<Return>", lambda _: add_button.invoke())
        button1 = ttk.Button(self.frame, text="Enter Problem", command=lambda: self.add_tests(tree), state="disabled")
        button1.grid(row=0, column=16, columnspan=1)
        button2 = ttk.Button(self.frame, text="Delete Problem", command=lambda: self.delete_problem(tree), state="disabled")
        button2.grid(row=0, column=17, columnspan=1)
        ttk.Button(self.frame, text="Settings", command=lambda: self.change_page("SETTINGS")).grid(column=18, row=0, columnspan=1)
        ttk.Button(self.frame, text="Sync", command=self.sync).grid(row=0, column=19, columnspan=1)
        ttk.Label(self.frame, text=f"{'-' * 300}").grid(column=0, row=1, columnspan=20)
        row = 2

        # tree setup
        tree = ttk.Treeview(self.frame, columns=("text",), show="headings", height=25, selectmode="browse", padding=20)
        style = ttk.Style(self.frame)
        style.configure("Treeview", rowheight=30)  # pyright: ignore 
        tree.heading("text", text="Problems")

        # default
        if not self.shared.problems:
            tree.insert("", tkinter.END, values=("No problems yet, click '+' to add",))
            tree.configure(selectmode="none")

        # add each problem to the tree
        for campus, problem in self.shared.problems.items():
            problem_node = tree.insert("", tkinter.END, campus, values=(f"{problem}",))

            if problem.open_problems:
                open_problem_node = tree.insert(problem_node, tkinter.END, values=(f"\tOpen Problems ({len(problem.open_problems)})",))
                for open_problem in problem.open_problems:
                    tree.insert(open_problem_node, tkinter.END, values=(f"\t\t{open_problem}",))

            problem_jobs = self.shared.job_manager.problem_to_jobs.get(problem, [])
            if problem_jobs:
                job_node = tree.insert(problem_node, tkinter.END, values=(f"\tJobs Raised ({len(problem_jobs)})",))
                for job in problem_jobs:
                    item = self.shared.job_manager.job_to_item[job]
                    tree.insert(job_node, tkinter.END, values=(f"\t\t{item.description} ({item.number}): {job.comment.replace("\n", " | ")}",))

            if problem.tests:
                test_node = tree.insert(problem_node, tkinter.END, values=(f"\tTests ({len(problem.tests)})",))
                for script_name, value in problem.test_breakdown.items():
                    tree.insert(test_node, tkinter.END, values=(f"\t\t{script_name} ({value})",))

        # completing tree setup
        scrollbar = ttk.Scrollbar(self.frame, orient=tkinter.VERTICAL, command=tree.yview)  # pyright: ignore
        tree.configure(yscroll=scrollbar.set)  # type: ignore
        scrollbar.grid(row=row, column=20, sticky=tkinter.NS)
        tree.grid(row=row, column=0, columnspan=20, sticky=tkinter.EW)
        row += 1

        tree.bind("<<TreeviewSelect>>", lambda _: self.on_first_select(tree, button1, button2))

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

    def sync(self) -> None:
        SyncPopup(self.frame, self.shared.problem).mainloop()
