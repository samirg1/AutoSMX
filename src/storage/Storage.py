import json
import pathlib
from contextlib import contextmanager
from dataclasses import asdict, dataclass, field
from pathlib import Path


@dataclass(slots=True, repr=False, eq=False)
class Positions:
    testing_tab: tuple[int, int] | None = None
    assets_tab: tuple[int, int] | None = None
    show_all_script: tuple[int, int] | None = None
    comment_box: tuple[int, int] | None = None
    window: tuple[int, int] | None = None
    track_weight_field: tuple[int, int] | None = None

    @classmethod
    def keys(cls):
        return cls.__annotations__.keys()

    @classmethod
    def from_dict(cls, data: dict[str, tuple[int, int]]):
        return cls(**data)


@dataclass(slots=True, repr=False, eq=False)
class Storage:
    _json_file_path: Path | str = field(default=pathlib.Path("src", "storage", "store.json"))
    total_tests: int = field(default=0, init=False)
    test_breakdown: dict[str, int] = field(default_factory=dict, init=False)
    positions: Positions = field(default_factory=Positions, init=False)
    positions_set: bool = field(default=False, init=False)
    item_model_to_script_answers: dict[str, list[str]] = field(default_factory=dict, init=False)

    def __post_init__(self) -> None:
        try:
            with open(self._json_file_path) as file:
                data = {}
                try:
                    data = json.load(file)
                    if not data:
                        raise FileNotFoundError
                except json.JSONDecodeError:
                    raise FileNotFoundError

                for key, value in data.items():
                    data = value if key != "positions" else Positions.from_dict(value)
                    setattr(self, key, data)

        except FileNotFoundError:
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
