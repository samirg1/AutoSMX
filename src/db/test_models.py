from abc import ABC
from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass(frozen=True)
class Model(ABC):
    def fields(self) -> str:
        return f"({', '.join(self.__annotations__.keys())})"

    def values(self) -> tuple[Any, ...]:
        return tuple(asdict(self).values())


@dataclass(repr=False, frozen=True, kw_only=True)
class TestModel(Model):
    test_id: str
    logical_name: str
    customer_barcode: str
    test_date: str
    sysmoduser: str
    problem_number: str
    user_name: str
    comments: str
    customer_id: str
    company_name: str
    location: str
    dept: str
    pointsync_id: str | None = field(default=None, init=False)
    overall: str
    building: str = field(default_factory=str, init=False)
    floor: str = field(default_factory=str, init=False)
    room: str
    model: str
    manufacturer: str
    description: str
    serial_no_: str
    pointsync_time: str | None = field(default=None, init=False)
    sysmodtime: str
    interfaced: str | None = field(default=None, init=False)


@dataclass(repr=False, frozen=True, kw_only=True)
class ScriptTesterModel(Model):
    test_id: str
    script_number: int
    tester_number: str


@dataclass(repr=False, frozen=True, kw_only=True)
class ScriptLineModel(Model):
    test_id: str
    script_number: int
    script_line: int
    result: str
    comments: str | None = field(default=None, init=False)
    date_performed: str | None = field(default=None, init=False)
    performed_by: str
    script_line_text: str
    set_point: int | None
    page: str | None = field(default=None, init=False)
    orderprgn: str | None = field(default=None, init=False)
