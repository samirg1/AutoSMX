import json
from typing import Any, Literal

STORAGE_KEYS = Literal["testing_tab_position", "assets_tab_position", "area_script_position", "comment_box_position", "positions_set", "window_position", "item_model_to_script_answers"]


class StorageManager:
    def __init__(self, filename: str):
        self._storage: dict[STORAGE_KEYS, Any] = {}
        try:
            with open(filename, "r+") as file:
                self._storage = json.load(file)
        except FileNotFoundError:
            with open(filename, "w") as file:
                file.write("{" + "}")

        self.filename = filename

    def __getitem__(self, key: STORAGE_KEYS) -> Any:
        return self._storage.get(key, None)

    def update(self, data: dict[STORAGE_KEYS, Any | None]) -> None:
        self._storage.update(data)
        self._save()

    def _save(self) -> None:
        with open(self.filename, "w") as file:
            json.dump(self._storage, file, indent=4)
