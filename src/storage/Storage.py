import json
from contextlib import contextmanager
from dataclasses import asdict, dataclass, field


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
    _json_file_path: str
    positions: Positions = field(default_factory=Positions)
    positions_set: bool = False
    item_model_to_script_answers: dict[str, list[str]] = field(default_factory=dict)

    @classmethod
    def from_json_file(cls, filename: str):
        try:
            with open(filename, "r") as file:
                data = {}
                try:
                    data = json.load(file)
                except json.JSONDecodeError:
                    raise FileNotFoundError
                data["positions"] = Positions.from_dict(data.get("positions", {}))
                data["_json_file_path"] = filename
                return cls(**data)
        except FileNotFoundError:
            with open(filename, "w") as file:
                instance = cls(filename)
                json.dump(asdict(instance), file, indent=4)
            return instance

    def _save(self) -> None:
        with open(self._json_file_path, "w") as file:
            json.dump(asdict(self), file, indent=4)

    @contextmanager
    def edit(self):
        try:
            yield self
        finally:
            self._save()
