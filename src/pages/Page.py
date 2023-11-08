from abc import ABC, abstractmethod
from typing import Callable, Literal
import customtkinter as ctk

from storage.Storage import Storage

TPAGES = Literal["PROBLEM", "TEST", "TUTORIAL", "SETTINGS"]


class Page(ABC):
    def __init__(self, frame: ctk.CTkScrollableFrame, change_page: Callable[[TPAGES], None], storage: Storage) -> None:
        self.frame = frame
        self.change_page = change_page
        self.storage = storage

    @abstractmethod
    def setup(self) -> None:
        ...
