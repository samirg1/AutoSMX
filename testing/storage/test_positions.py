import pytest

from storage.Storage import Positions

_POSITIONS_DATA: dict[str, tuple[int, int]] = {
    "testing_tab": (1, 2),
    "assets_tab": (3, 4),
    "show_all_script": (5, 6),
    "comment_box": (7, 8),
    "window": (9, 10),
    "track_weight_field": (11, 12),
    "sm_incident_tab": (13, 14),
}


def test_positions_initialization() -> None:
    positions = Positions(**_POSITIONS_DATA)
    assert positions.testing_tab == (1, 2)
    assert positions.assets_tab == (3, 4)
    assert positions.show_all_script == (5, 6)
    assert positions.comment_box == (7, 8)
    assert positions.window == (9, 10)
    assert positions.track_weight_field == (11, 12)
    assert positions.sm_incident_tab == (13, 14)


def test_positions_from_dict() -> None:
    positions = Positions.from_dict(_POSITIONS_DATA)
    assert positions.testing_tab == (1, 2)
    assert positions.assets_tab == (3, 4)
    assert positions.show_all_script == (5, 6)
    assert positions.comment_box == (7, 8)
    assert positions.window == (9, 10)
    assert positions.track_weight_field == (11, 12)
    assert positions.sm_incident_tab == (13, 14)


def test_positions_keys() -> None:
    expected_keys = {"testing_tab", "assets_tab", "show_all_script", "comment_box", "window", "track_weight_field", "sm_incident_tab"}
    assert set(Positions.keys()) == expected_keys


def test_positions_slots() -> None:
    positions = Positions(**_POSITIONS_DATA)
    with pytest.raises(AttributeError):
        positions.x = 1  # type: ignore
