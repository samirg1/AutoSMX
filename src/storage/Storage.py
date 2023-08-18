import json
import pathlib
from contextlib import contextmanager
from pathlib import Path
from typing import Mapping, Optional, Sequence, Union

from attrs import asdict, define, field


def _tuple_converter(value: Optional[Sequence[int]]) -> Optional[tuple[int, ...]]:
    return tuple(value) if value else None


@define(repr=False, eq=False)
class Positions:
    testing_tab: Optional[tuple[int, int]] = field(default=None, converter=_tuple_converter)
    assets_tab: Optional[tuple[int, int]] = field(default=None, converter=_tuple_converter)
    show_all_script: Optional[tuple[int, int]] = field(default=None, converter=_tuple_converter)
    comment_box: Optional[tuple[int, int]] = field(default=None, converter=_tuple_converter)
    window: Optional[tuple[int, int]] = field(default=None, converter=_tuple_converter)
    track_weight_field: Optional[tuple[int, int]] = field(default=None, converter=_tuple_converter)

    @classmethod
    def keys(cls):
        return cls.__annotations__.keys()

    @classmethod
    def from_dict(cls, data: Mapping[str, Sequence[int]]):
        return cls(**data)


@define(repr=False, eq=False)
class Storage:
    _json_file_path: Union[Path, str] = field(default=pathlib.Path("src", "storage", "store.json"))
    total_tests: int = field(default=0, init=False)
    test_breakdown: dict[str, int] = field(factory=dict, init=False)
    positions: Positions = field(factory=Positions, init=False)
    positions_set: bool = field(default=False, init=False)
    item_model_to_script_answers: dict[str, list[str]] = field(factory=dict, init=False)

    def __attrs_post_init__(self) -> None:
        try:
            with open(self._json_file_path) as file:
                data = json.load(file)
                if not data:
                    return self._save()

                for key, value in data.items():
                    data = value if key != "positions" else Positions.from_dict(value)
                    setattr(self, key, data)

        except (FileNotFoundError, json.JSONDecodeError):
            self._save()

    def _save(self) -> None:
        with open(self._json_file_path, "w") as file:
            data = asdict(self)
            data["_json_file_path"] = str(data["_json_file_path"])
            json.dump(data, file, indent=4)

    @contextmanager
    def edit(self):
        try:
            yield self
        finally:
            self._save()
