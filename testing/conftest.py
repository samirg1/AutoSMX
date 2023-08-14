from typing import Any, Callable

import pytest


@pytest.fixture
def pyautogui_fixture(monkeypatch: pytest.MonkeyPatch):
    buffer: dict[str, list[str]] = {
        "hot_key_calls": [],
        "sleep_calls": [],
        "typewrite_calls": [],
        "click_calls": [],
    }

    def mock_hotkey(*args: str) -> None:
        buffer["hot_key_calls"].append(str(args))

    def mock_sleep(seconds: float) -> None:
        buffer["sleep_calls"].append(str(seconds))

    def mock_typewrite(text: str) -> None:
        buffer["typewrite_calls"].append(text)

    def mock_click(position: tuple[int, int]) -> None:
        buffer["click_calls"].append(str(position))

    monkeypatch.setattr("pyautogui.hotkey", mock_hotkey)
    monkeypatch.setattr("pyautogui.sleep", mock_sleep)
    monkeypatch.setattr("pyautogui.typewrite", mock_typewrite)
    monkeypatch.setattr("pyautogui.click", mock_click)
    monkeypatch.setattr("pyautogui.size", lambda: (100, 100))

    return buffer


@pytest.fixture
def pyperclip_fixture(monkeypatch: pytest.MonkeyPatch):
    buffer: dict[str, list[str]] = {"paste_calls": []}

    def mock_paste() -> str:
        buffer["paste_calls"].append("Selected Text")
        return "Selected Text"

    monkeypatch.setattr("pyperclip.paste", mock_paste)
    return buffer


@pytest.fixture
def pynput_fixture(monkeypatch: pytest.MonkeyPatch):
    class AlwaysEqual:
        def __eq__(self, other: Any):
            return True

    class MockListener:
        def __init__(self, on_click: Callable[[float, float, AlwaysEqual, bool], bool]) -> None:
            self.on_click = on_click
            self.started = False

        def start(self):
            self.started = True

        def join(self):
            self.on_click(100, 200, AlwaysEqual(), True)

    monkeypatch.setattr("pynput.mouse.Listener", MockListener)
