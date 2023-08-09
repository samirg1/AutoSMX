import json
from dataclasses import asdict, dataclass, field


@dataclass(slots=True)
class Positions:
    testing_tab: tuple[int, int] | None = None
    assets_tab: tuple[int, int] | None = None
    show_all_script: tuple[int, int] | None = None
    comment_box: tuple[int, int] | None = None
    window: tuple[int, int] | None = None

    @classmethod
    def keys(cls):
        return cls.__annotations__.keys()

    @classmethod
    def from_dict(cls, data: dict[str, tuple[int, int]]):
        return cls(**data)


@dataclass(slots=True)
class Storage:
    _json_file_path: str
    positions: Positions = field(default_factory=Positions)
    positions_set: bool = False
    item_model_to_script_answers: dict[str, list[str]] = field(default_factory=dict)

    @classmethod
    def from_json_file(cls, filename: str):
        try:
            with open(filename, "r") as file:
                data = json.load(file)
                data["positions"] = Positions.from_dict(data["positions"])
                return cls(**data)
        except FileNotFoundError:
            with open(filename, "w") as file:
                instance = cls(filename)
                json.dump(asdict(instance), file, indent=4)
            return instance

    def save(self) -> None:
        with open(self._json_file_path, "w") as file:
            json.dump(asdict(self), file, indent=4)
