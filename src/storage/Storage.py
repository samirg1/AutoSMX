from contextlib import contextmanager
import pathlib
import pickle
from typing import Generator

from design.Problem import Problem


class Storage:
    __slots__ = ("_file_path", "problems", "total_tests", "test_breakdown", "tutorial_complete", "item_model_to_script_answers")

    def __init__(self, file_path: pathlib.Path) -> None:
        self._file_path = file_path
        self.problems: dict[str, Problem] = {}
        self.tutorial_complete = False
        self.total_tests = 0
        self.test_breakdown: dict[str, int] = {}
        self.item_model_to_script_answers: dict[str, list[str]] = {}

        try:
            with open(self._file_path, mode="rb") as f:
                for name, value in pickle.load(f).items():
                    setattr(self, name, value)
        except FileNotFoundError:
            self._save()

    def _save(self) -> None:
        with open(self._file_path, mode="wb") as f:
            pickle.dump({key: getattr(self, key) for key in self.__slots__}, f)

    @contextmanager
    def edit(self) -> Generator["Storage", None, None]:
        try:
            yield self
        finally:
            self._save()
