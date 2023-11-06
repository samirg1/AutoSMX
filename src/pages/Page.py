from abc import ABC, abstractmethod
from typing import Callable, Literal
import customtkinter as ctk

from design.JobManager import JobManager
from design.Problem import Problem
from storage.Storage import Storage

TPAGES = Literal["PROBLEM", "TEST", "TUTORIAL", "SETTINGS"]


class SharedPageInfo:
    def __init__(self, problems: dict[str, Problem], job_manager: JobManager, storage: Storage) -> None:
        self.problems = problems
        self.job_manager = job_manager
        self.problem: Problem | None = None
        self.storage = storage

class Page(ABC):
    def __init__(self, frame: ctk.CTkScrollableFrame, change_page: Callable[[TPAGES], None], shared: SharedPageInfo) -> None:
        self.frame = frame
        self.change_page = change_page
        self.shared = shared

    @abstractmethod
    def setup(self) -> None:
        ...
