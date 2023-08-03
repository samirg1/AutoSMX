from abc import ABC, abstractmethod
from tkinter import ttk

# from pages import App


class Page(ABC):
    def __init__(self, parent) -> None:
        self.parent = parent
        self.frame = ttk.Frame(parent, padding="3 3 12 12")
    
    @abstractmethod
    def setup(self):
        ...