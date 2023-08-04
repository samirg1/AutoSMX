from abc import ABC, abstractmethod
from tkinter import ttk
from typing import Any, Literal, Protocol

TPAGES = Literal["START", "JOB", "TEST", "TESTJOB"]

class Combiner(Protocol):
    def __call__(self, page: TPAGES, **kwargs: Any) -> None:
        ...


class Page(ABC):
    def __init__(self, frame: ttk.Frame, change_page: Combiner, **kwargs: Any) -> None:
        self.frame = frame
        self.change_page = change_page
        self.kwargs = kwargs
    
    @abstractmethod
    def setup(self):
        ...