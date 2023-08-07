import json
from typing import Any, Literal

STORAGE_KEYS = Literal["testing_tab_position", "assets_tab_position", "area_script_position", "comment_box_position", "positions_set"]


class StorageManager:
    def __init__(self, filename: str):
        self._storage: dict[str, Any] = {}
        with open(filename, "r") as file:
            self._storage = json.load(file)

        self.filename = filename

    def __getitem__(self, key: STORAGE_KEYS) -> Any:
        return self._storage[key]

    def __setitem__(self, key: STORAGE_KEYS, value: Any) -> None:
        self._storage[key] = value
        self._save()

    def _save(self) -> None:
        with open(self.filename, "w") as file:
            json.dump(self._storage, file, indent=4)
