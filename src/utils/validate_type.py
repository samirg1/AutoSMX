import types
from typing import Any, Type, TypeVar, cast, get_origin, get_args


_T = TypeVar("_T")


class _ValidateTypeError(TypeError):
    t: type
    obj: Any

    def __init__(self, *args: object) -> None:
        super().__init__(self.t, *args)


def validate_type(t: Type[_T], obj: Any) -> _T:
    _ValidateTypeError.t = t
    _ValidateTypeError.obj = obj
    _validate_type_aux(t, obj)
    return cast(_T, obj)


def _validate_type_aux(expected: Type[_T], actual: Any | list[Any] | tuple[Any, ...], parent: str = "") -> _T:
    origin, args = get_origin(expected), get_args(expected)

    if origin is None:
        if not isinstance(actual, expected):
            raise _ValidateTypeError(f"Actual does not equal expected, {actual=}, expected={expected.__name__}, {parent=}")
        return expected()

    if isinstance(expected, types.UnionType):
        for arg in args:
            try:
                _validate_type_aux(arg, actual, parent + f" union{args}")
                break
            except _ValidateTypeError:
                continue
        else:
            raise _ValidateTypeError(f"Type of actual does not match union, {actual=}, union={expected}, {parent=}")

    elif not isinstance(actual, origin):
        raise _ValidateTypeError(f"Actual not same as expected origin, {actual=}, expected={origin.__name__}, {parent=}")

    elif isinstance(actual, list):
        for c in actual:
            _validate_type_aux(args[0], c, parent + " list")

    elif isinstance(actual, tuple):
        if len(args) != len(actual):
            args = tuple(arg.__name__ for arg in args)
            raise _ValidateTypeError(f"Expected args and actual not same length, {args=}, {actual=}, {parent=}")

        for i, (arg, c) in enumerate(zip(args, actual)):
            _validate_type_aux(arg, c, parent + f" tuple[{i}]")

    return expected


if __name__ == "__main__":
    import pytest

    accepted: list[tuple[type, Any]] = [
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
    for t, obj in accepted:
        validate_type(t, obj)

    not_accepted: list[tuple[type, Any]] = [
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
    for t, obj in not_accepted:
        with pytest.raises(TypeError):
            validate_type(t, obj)
