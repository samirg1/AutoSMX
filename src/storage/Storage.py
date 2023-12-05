import os
import pathlib
import pickle
from contextlib import contextmanager
from typing import Generator, Self

from design.JobManager import JobManager
from design.Part import Part
from design.Problem import Problem
from design.ScriptInfo import ScriptInfo
from utils.constants import APPLICATION_PATH
from utils.MRUList import MRUList


class Storage:
    __slots__ = (
        "_file_path",
        "_backup_file_path",
        "problems",
        "problem",
        "job_manager",
        "tutorial_complete",
        "skip_overall_result_check",
        "total_tests",
        "test_breakdown",
        "previous_parts",
        "item_model_to_script_answers",
        "added_script_infos",
        "deleted_script_numbers",
    )

    def __init__(self, *, _file_path: pathlib.Path | None = None) -> None:
        self._file_path = _file_path or pathlib.Path(APPLICATION_PATH, "store.pkl")
        self._backup_file_path = self._file_path.parent / "backup.pkl"
        self.problems: dict[str, Problem] = {}
        self.problem: Problem | None = None
        self.job_manager = JobManager()
        self.tutorial_complete = False
        self.skip_overall_result_check = False
        self.total_tests = 0
        self.test_breakdown: dict[str, int] = {}
        self.previous_parts: MRUList[Part] = MRUList()
        self.item_model_to_script_answers: dict[str, list[str]] = {}
        self.added_script_infos: list[ScriptInfo] = []
        self.deleted_script_numbers: set[int] = set()

        try:
            with open(self._file_path, mode="rb") as f:
                for name, value in pickle.load(f).items():
                    setattr(self, name, value)
        except (FileNotFoundError, EOFError):
            self._save()

    def _save(self) -> None:
        data = {key: getattr(self, key) for key in self.__slots__}
        with open(self._backup_file_path, mode="wb") as backup:
            to_back_up = bytes()
            try:
                with open(self._file_path, mode="rb") as current:
                    to_back_up = current.read()
            except FileNotFoundError:
                ...

            backup.write(to_back_up)

        with open(self._file_path, mode="wb") as f:
            try:
                pickle.dump(data, f)
            except BaseException as e:
                with open(self._backup_file_path, mode="rb") as backup, open(self._file_path, mode="wb") as current:
                    current.write(backup.read())
                raise e from None
            finally:
                os.remove(self._backup_file_path)

    @contextmanager
    def edit(self) -> Generator[Self, None, None]:
        try:
            yield self
        finally:
            self._save()
