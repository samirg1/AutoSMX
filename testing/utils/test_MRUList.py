import pytest

from utils.MRUList import MRUList


@pytest.mark.parametrize(("mods", "expected", "string"), [
    ([1], [1], "1"),
    ([1, 2, 1], [1, 2], "1 -> 2"),
    ([1, 2, 2, 2, 2, 2, 1], [1, 2], "1 -> 2"),
    ([1, 2, 3, 4, 5], [5, 4, 3, 2, 1], "5 -> 4 -> 3 -> 2 -> 1"),
    ([1, 2, 3, 4, 5, 3, 6, 4, 1, 4, 5, 2, 4], [4, 2, 5, 1, 6, 3], "4 -> 2 -> 5 -> 1 -> 6 -> 3"),
    ([1, -1], [], ""),
    ([1, 2, 3, 4, -4], [3, 2, 1], "3 -> 2 -> 1"),
    ([1, 2, 3, 4, -4, -2], [3, 1], "3 -> 1"),
    ([1, 2, 2, 2, 2, 2, 2, -2], [1], "1"),
    ([1, 2, 2, 2, 2, 2, 2, -2, 2], [2, 1], "2 -> 1"),
])
def test_mru_list(mods: list[int], expected: list[int], string: str) -> None:
    lst: MRUList[int] = MRUList()
    for mod in mods:
        if mod > 0:
            lst.add(mod)
        else:
            lst.remove(-mod)

    assert len(lst) == len(expected)
    assert repr(lst) == f"MRUList({string})"
    assert [l for l in lst] == expected

    assert lst != 1
