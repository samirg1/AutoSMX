import json
import os
from typing import Any, Callable, Generator

import pytest

from storage.Storage import Storage

_EMPTY_DATA: dict[str, Any] = {
    "total_tests": 0,
    "test_breakdown": {},
    "tutorial_complete": False,
    "item_model_to_script_answers": {},
}


@pytest.fixture
def get_file_for_testing() -> Generator[Callable[..., str], None, None]:
    original_file_content: dict[str, Any] | str = {}
    file_name = ""
    file_exists = True

    def _get_file(name: str) -> str:
        name = f"testing/storage/{name}"
        nonlocal file_name
        file_name = name
        try:
            with open(file_name) as file:
                nonlocal original_file_content
                original_file_content = file.read()
                try:
                    original_file_content = json.load(file)
                except json.JSONDecodeError:
                    pass
        except FileNotFoundError:
            nonlocal file_exists
            file_exists = False
        return name

    yield _get_file

    if not file_exists:
        return os.remove(file_name)
    with open(file_name, "w") as file:
        if isinstance(original_file_content, dict):  # pyright: ignore[reportUnnecessaryIsInstance]
            json.dump(original_file_content, file, indent=4)
        else:
            file.write(original_file_content)


@pytest.mark.parametrize("file_name", ["empty.json", "storage.json", "invalid.json", "missing.json"])
def test_empty_missing_invalid_json(file_name: str, get_file_for_testing: Callable[[str], str]) -> None:
    file_name = get_file_for_testing(file_name)
    _EMPTY_DATA["_json_file_path"] = file_name
    storage = Storage(file_name)
    for key, value in _EMPTY_DATA.items():
        assert getattr(storage, key) == value

    with open(file_name) as file:
        data = json.load(file)
        assert data == _EMPTY_DATA


def test_storage_edit_and_save(get_file_for_testing: Callable[[str], str]) -> None:
    file = get_file_for_testing("storage.json")
    storage = Storage(file)

    with storage.edit():
        storage.total_tests += 1
        storage.test_breakdown["test"] = 1
        storage.tutorial_complete = True
        storage.item_model_to_script_answers["test"] = ["test"]

    with open(file) as f:
        data = json.load(f)
        assert data["total_tests"] == 1
        assert data["test_breakdown"] == {"test": 1}
        assert data["tutorial_complete"]
        assert data["item_model_to_script_answers"] == {"test": ["test"]}

    storage2 = Storage(file)
    assert storage2.total_tests == 1
    assert storage2.test_breakdown == {"test": 1}
    assert storage2.tutorial_complete
    assert storage2.item_model_to_script_answers == {"test": ["test"]}

    with pytest.raises(AttributeError):
        storage2.x = 1  # type: ignore
