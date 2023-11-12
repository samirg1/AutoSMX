from contextlib import contextmanager
import pathlib
import pickle
from typing import Generator

from design.Problem import Problem
from design.JobManager import JobManager
from utils.constants import APPLICATION_PATH


class Storage:
    __slots__ = ("_file_path", "problems", "problem", "job_manager", "total_tests", "test_breakdown", "tutorial_complete", "skip_overall_result_check", "item_model_to_script_answers")

    def __init__(self) -> None:
        self._file_path = pathlib.Path(APPLICATION_PATH, "store.pkl")
        self.problems: dict[str, Problem] = {}
        self.problem: Problem | None = None
        self.job_manager = JobManager()
        self.tutorial_complete = False
        self.skip_overall_result_check = False
        self.total_tests = 0
        self.test_breakdown: dict[str, int] = {}
        self.item_model_to_script_answers: dict[str, list[str]] = {}

        try:
            with open(self._file_path, mode="rb") as f:
                for name, value in pickle.load(f).items():
                    setattr(self, name, value)
        except (FileNotFoundError, EOFError):
            self._save()

    def _save(self) -> None:
        data = {key: getattr(self, key) for key in self.__slots__}
        with open(self._file_path, mode="wb") as f:
            try:
                pickle.dump(data, f)
            except Exception as e:
                with open(self._file_path, mode="w") as backup:
                    backup.write(f"{data}")
                raise e from None

    @contextmanager
    def edit(self) -> Generator["Storage", None, None]:
        try:
            yield self
        finally:
            self._save()
