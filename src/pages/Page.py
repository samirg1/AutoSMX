from abc import ABC, abstractmethod
from tkinter import ttk
from typing import Callable, Literal

from design.Job import Job
from design.TestJobManager import TestJobManager
from storage.Storage import Storage

TPAGES = Literal["START", "JOB", "TEST", "TESTJOB"]


class SharedPageInfo:
    def __init__(self, jobs: dict[str, Job], testjob_manager: TestJobManager, storage: Storage) -> None:
        self.jobs = jobs
        self.testjob_manager = testjob_manager
        self.job: Job | None = None
        self.storage = storage
        self.previous_item_number: str = ""


class Page(ABC):
    def __init__(
        self,
        frame: ttk.Frame,
        change_page: Callable[[TPAGES], None],
        shared: SharedPageInfo,
    ) -> None:
        self.frame = frame
        self.change_page = change_page
        self.shared = shared

    @abstractmethod
    def setup(self):
        ...
