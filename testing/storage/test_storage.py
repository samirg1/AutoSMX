import json
import os
from typing import Any, Callable, cast

import pytest

from storage import Positions, Storage

_EMPTY_DATA: dict[str, Any] = {
    "total_tests": 0,
    "test_breakdown": {},
    "positions": {
        "testing_tab": None,
        "assets_tab": None,
        "show_all_script": None,
        "comment_box": None,
        "window": None,
        "track_weight_field": None,
    },
    "positions_set": False,
    "item_model_to_script_answers": {},
}


@pytest.fixture
def get_file_for_testing():
    original_file_content: dict[str, Any] | str = {}
    file_name = ""
    file_exists = True

    def _get_file(name: str):
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
        if isinstance(original_file_content, dict):  # type: ignore
            json.dump(original_file_content, file, indent=4)
        else:
            file.write(original_file_content)


@pytest.mark.parametrize("file_name", ["empty.json", "storage.json", "invalid.json", "missing.json"])
def test_empty_missing_invalid_json(file_name: str, get_file_for_testing: Callable[[str], str]):
    file_name = get_file_for_testing(file_name)
    _EMPTY_DATA["_json_file_path"] = file_name
    storage = Storage(file_name)
    assert isinstance(storage.positions, Positions)
    for key, value in _EMPTY_DATA.items():
        if key == "positions":
            for k, v in cast(dict[str, None], value).items():
                assert getattr(storage.positions, k) == v
        else:
            assert getattr(storage, key) == value

    with open(file_name) as file:
        data = json.load(file)
        assert data == _EMPTY_DATA


def test_storage_edit(get_file_for_testing: Callable[[str], str]):
    file = get_file_for_testing("storage.json")
    storage = Storage(file)
    
    with storage.edit():
        storage.total_tests += 1
        storage.test_breakdown["test"] = 1
        storage.positions.testing_tab = (1, 1)
        storage.positions.assets_tab = (2, 2)
        storage.positions.show_all_script = (3, 3)
        storage.positions.comment_box = (4, 4)
        storage.positions.window = (5, 5)
        storage.positions.track_weight_field = (6, 6)
        storage.positions_set = True
        storage.item_model_to_script_answers["test"] = ["test"]
    
    with open(file) as f:
        data = json.load(f)
        assert data["total_tests"] == 1
        assert data["test_breakdown"] == {"test": 1}
        assert data["positions"] == {
            "testing_tab": [1, 1],
            "assets_tab": [2, 2],
            "show_all_script": [3, 3],
            "comment_box": [4, 4],
            "window": [5, 5],
            "track_weight_field": [6, 6],
        }
        assert data["positions_set"]
        assert data["item_model_to_script_answers"] == {"test": ["test"]}






if __name__ == "__main__":
    pytest.main()