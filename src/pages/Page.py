from abc import ABC, abstractmethod
from typing import Callable
import customtkinter as ctk

from storage.Storage import Storage
from utils.constants import PAGE_NAMES


class Page(ABC):
    def __init__(self, frame: ctk.CTkScrollableFrame, change_page: Callable[[PAGE_NAMES], None], storage: Storage) -> None:
        self.frame = frame
        self.change_page = change_page
        self.storage = storage

    @abstractmethod
    def setup(self) -> None:
        ...
