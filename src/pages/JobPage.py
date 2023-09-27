import tkinter
from tkinter import ttk

from design.Job import Job
from pages.Page import Page
from popups.JobEntryPopup import JobEntryPopup


class JobPage(Page):
    def setup(self):
        # top row
        ttk.Label(self.frame, text="Jobs").grid(column=0, row=0, columnspan=1)
        ttk.Button(self.frame, text="+", width=1, command=self.add_tests).grid(column=1, row=0, columnspan=1)
        ttk.Button(self.frame, text="Settings", command=lambda: self.change_page("SETTINGS")).grid(column=2, row=0, columnspan=2)
        ttk.Label(self.frame, text=f"{'-' * 50}").grid(column=0, row=1, columnspan=4)
        row = 2

        # tree setup
        tree = ttk.Treeview(self.frame, columns=("text", "number"), show="tree headings", height=10, selectmode="browse")
        style = ttk.Style(self.frame)
        style.configure("Treeview", rowheight=60)  # type: ignore
        tree.column("#0", width=0)
        tree.column("text", anchor=tkinter.W)
        tree.column("number", width=10, anchor=tkinter.CENTER)
        tree.heading("text", text="Jobs")
        tree.heading("number", text="#")

        # default
        if not self.shared.jobs:
            tree.insert("", tkinter.END, values=("No jobs yet, click '+' to add",))
            tree.configure(selectmode="none")

        # add each job to the tree
        for campus, job in self.shared.jobs.items():
            job_node = tree.insert("", tkinter.END, campus, values=(f"{job}",))

            job_testjobs = self.shared.testjob_manager.job_to_testjobs.get(job, [])
            if job_testjobs:
                testjob_node = tree.insert(job_node, tkinter.END, values=("Jobs Raised", len(job_testjobs)))
                for testjob in job_testjobs:
                    item = self.shared.testjob_manager.testjob_to_item[testjob]
                    first_line = str(testjob).split("\n")[0]
                    tree.insert(testjob_node, tkinter.END, values=(f"{first_line}\n{item.description}\n{item.number}",))

            if job.tests:
                test_node = tree.insert(job_node, tkinter.END, values=("Tests", f"{len(job.tests)}"))
                for script_name, value in job.test_breakdown.items():
                    tree.insert(test_node, tkinter.END, values=(f"{script_name}", value))

        # completing tree setup
        scrollbar = ttk.Scrollbar(self.frame, orient=tkinter.VERTICAL, command=tree.yview)  # type: ignore
        tree.configure(yscroll=scrollbar.set)  # type: ignore
        scrollbar.grid(row=row, column=4, sticky=tkinter.NS)
        tree.grid(row=row, column=0, columnspan=4, sticky=tkinter.EW)
        row += 1

        # add job manipulation buttons
        button1 = ttk.Button(self.frame, text="Enter Job", command=lambda: self.add_tests(tree), state="disabled")
        button1.grid(row=row, column=0, columnspan=4)
        button2 = ttk.Button(self.frame, text="Delete Job", command=lambda: self.delete_job(tree), state="disabled")
        button2.grid(row=row + 1, column=0, columnspan=4)

        tree.bind("<<TreeviewSelect>>", lambda _: self.on_first_select(tree, button1, button2))

    def on_first_select(self, tree: ttk.Treeview, *buttons: ttk.Button):
        for button in buttons:
            button.configure(state="normal")
        tree.unbind("<<TreeviewSelect>>")

    def get_selected_job(self, tree: ttk.Treeview) -> Job:
        item = tree.focus()
        possible_parent1 = tree.parent(item)
        parent1 = possible_parent1 if possible_parent1 else item
        possible_parent2 = tree.parent(parent1)
        parent2 = possible_parent2 if possible_parent2 else parent1

        return self.shared.jobs[parent2]

    def delete_job(self, tree: ttk.Treeview) -> None:
        job = self.get_selected_job(tree)
        del self.shared.jobs[job.campus]
        if job in self.shared.testjob_manager.job_to_testjobs:
            del self.shared.testjob_manager.job_to_testjobs[job]
        self.change_page("JOB")

    def add_tests(self, tree: ttk.Treeview | None = None) -> None:
        if tree is None:
            JobEntryPopup(self.frame, lambda job: self.add_job(job))
        else:
            self.shared.job = self.get_selected_job(tree)

    def add_job(self, job: Job) -> None:
        self.shared.job = job
        self.change_page("TEST")
