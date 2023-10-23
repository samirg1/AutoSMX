import json
from contextlib import contextmanager
from pathlib import Path
from typing import Generator

from attrs import asdict, define, field


@define(repr=False, eq=False)
class Storage:
    _json_file_path: Path | str
    tutorial_complete: bool = field(default=False, init=False)
    total_tests: int = field(default=0, init=False)
    test_breakdown: dict[str, int] = field(factory=dict, init=False)
    item_model_to_script_answers: dict[str, list[str]] = field(factory=dict, init=False)

    def __attrs_post_init__(self) -> None:
        try:
            with open(self._json_file_path) as file:
                data = json.load(file)
                if not data:
                    return self._save()

                for key, value in data.items():
                    setattr(self, key, value)

        except (FileNotFoundError, json.JSONDecodeError):
            self._save()

    def _save(self) -> None:
        with open(self._json_file_path, "w") as file:
            data = asdict(self)
            data["_json_file_path"] = str(data["_json_file_path"])
            json.dump(data, file, indent=4)

    @contextmanager
    def edit(self) -> Generator["Storage", None, None]:
        try:
            yield self
        finally:
            self._save()
