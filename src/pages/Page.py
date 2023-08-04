from abc import ABC, abstractmethod
from tkinter import ttk
from typing import Any, Callable, Literal

TPAGES = Literal["START", "JOB", "TEST", "TESTJOB"]

class Page(ABC):
    def __init__(self, frame: ttk.Frame, change_page: Callable[..., None], **kwargs: Any) -> None:
        self.frame = frame
        self.change_page = change_page
        self.kwargs = kwargs
    
    @abstractmethod
    def setup(self):
        ...