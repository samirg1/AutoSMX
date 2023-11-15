import pathlib
import pickle
import os
from typing import Any, Callable, Generator

import pytest
from design import JobManager

from storage.Storage import Storage
from utils.MRUList import MRUList

_EMPTY_DATA: dict[str, Any] = {
    "problem": None,
    "problems": {},
    "total_tests": 0,
    "test_breakdown": {},
    "tutorial_complete": False,
    "item_model_to_script_answers": {},
    "added_scripts": [],
    "job_manager": JobManager(),
    "previous_parts": MRUList(),
    "skip_overall_result_check": False,
}


@pytest.fixture
def get_file_for_testing() -> Generator[Callable[..., pathlib.Path], None, None]:
    original_file_content: dict[str, Any] | str = {}
    file_name = ""
    file_exists = True

    def _get_file(name: str) -> pathlib.Path:
        filename = pathlib.Path("testing", "storage", name)
        nonlocal file_name
        file_name = filename
        try:
            with open(file_name, mode="rb") as file:
                nonlocal original_file_content
                original_file_content = pickle.load(file)
        except FileNotFoundError:
            nonlocal file_exists
            file_exists = False
        return filename

    yield _get_file

    if not file_exists:
        return os.remove(file_name)
    with open(file_name, "wb") as file:
        pickle.dump(original_file_content, file)


@pytest.mark.parametrize("file_name", ["empty.pkl", "storage.pkl", "invalid.pkl", "missing.pkl"])
def test_empty_missing_invalid_json(file_name: str, get_file_for_testing: Callable[[str], pathlib.Path]) -> None:
    name = get_file_for_testing(file_name)
    _EMPTY_DATA["_file_path"] = name
    storage = Storage(_file_path=name)
    for key, value in _EMPTY_DATA.items():
        assert getattr(storage, key) == value

    with storage.edit():
        ...

    with open(name, mode="rb") as file:
        data = pickle.load(file)
        assert data == _EMPTY_DATA


def test_storage_edit_and_save(get_file_for_testing: Callable[[str], pathlib.Path]) -> None:
    file = get_file_for_testing("storage.pkl")
    storage = Storage(_file_path=file)

    with storage.edit():
        storage.total_tests += 1
        storage.test_breakdown["test"] = 1
        storage.tutorial_complete = True
        storage.item_model_to_script_answers["test"] = ["test"]

    with open(file, mode="rb") as f:
        data = pickle.load(f)
        assert data["total_tests"] == 1
        assert data["test_breakdown"] == {"test": 1}
        assert data["tutorial_complete"]
        assert data["item_model_to_script_answers"] == {"test": ["test"]}

    storage2 = Storage(_file_path=file)
    assert storage2.total_tests == 1
    assert storage2.test_breakdown == {"test": 1}
    assert storage2.tutorial_complete
    assert storage2.item_model_to_script_answers == {"test": ["test"]}

    with pytest.raises(AttributeError):
        storage2.x = 1  # type: ignore
