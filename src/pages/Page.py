from abc import ABC, abstractmethod
from tkinter import ttk
from typing import Callable, Literal

from design import Job

TPAGES = Literal["START", "JOB", "TEST", "TESTJOB"]


class SharedPageInfo:
    def __init__(self) -> None:
        self.assets_position: tuple[int, int] = (0, 0)
        self.testing_position: tuple[int, int] = (0, 0)
        self.area_position: tuple[int, int] = (0, 0)
        self.comments_position: tuple[int, int] = (0, 0)
        self.position_set = 0
        self.jobs: dict[str, Job] = {}
        self.job: Job | None = None


class Page(ABC):
    def __init__(self, frame: ttk.Frame, change_page: Callable[[TPAGES], None], shared: SharedPageInfo) -> None:
        self.frame = frame
        self.change_page = change_page
        self.shared = shared

    @abstractmethod
    def setup(self):
        ...
