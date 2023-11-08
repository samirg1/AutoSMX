from typing import Any
import pytest

from utils.validate_type import validate_type, _ValidateTypeError  # pyright: ignore[reportPrivateUsage]


successes: list[tuple[type, Any]] = [
    (list[int], []),
    (list[str], []),
    (list[float], []),
    (list[int | str], ["1", 1]),
    (list[list[int]], []),
    (list[list[int]], [[]]),
    (list[list[list[int]]], []),
    (list[list[list[int]]], [[[]]]),
    (list[int], [1, 2, 3]),
    (list[str], ["1"]),
    (list[float], [1.0]),
    (list[list[str]], [["1"]]),
    (list[list[int]], [[1]]),
    (list[list[float]], [[1.0]]),
    (list[list[list[int]]], [[[1]]]),
    (list[tuple[int, int, str, float]], [(1, 1, "1", 1.0)] * 10_000),
    (list[tuple[str, str, int]], [("1", "1", 1), ("2", "2", 2)]),
    (list[tuple[str, str | None, int | float, str, float]], [("1", None, 1, "1", 1.0), ("1", "10.01", 1.0, "1", 1.0)]),
    (tuple[int], (1,)),
    (tuple[str], ("1",)),
    (tuple[str, int], ("1", 1)),
    (tuple[str, int, float], ("1", 1, 1.0)),
    (tuple[str, int, tuple[str]], ("1", 1, ("1",))),
    (tuple[str, int, list[str]], ("1", 1, ["1"])),
]


@pytest.mark.parametrize(("t", "obj"), successes)
def test_validate_type(t: type, obj: Any) -> None:
    validate_type(t, obj)


failures: list[tuple[type, Any]] = [
    (list[int], ["1"]),
    (list[int], [1, "1"]),
    (list[int | float], ["1", 1]),
    (list[int | str], ["1", 1.0]),
    (list[float], [1.0, 1.0, 1.0, 1.0, 1]),
    (list[int], [1.0, 1]),
    (list[list[int]], [1]),
    (list[list[int]], [["1"]]),
    (list[list[list[int]]], [[1]]),
    (list[tuple[str, str, int]], [("1", "1", 1), ("2", "2", 2.0)]),
    (list[list[list[int]]], [[["1"]]]),
    (list[int], ""),
    (list[int], ()),
    (list[int], (1,)),
]


@pytest.mark.parametrize(("t", "obj"), failures)
def test_validate_type_fail(t: type, obj: Any) -> None:
    with pytest.raises(_ValidateTypeError):
        validate_type(t, obj)
