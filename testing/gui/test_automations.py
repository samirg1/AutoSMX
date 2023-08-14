import os
os.environ['DISPLAY'] = ':0'
from gui.automations import click, click_key, get_click_position, get_selected_text, type, wait


def test_click_key(pyautogui_fixture: dict[str, list[str]]):
    click_key("ctrl", "c")
    assert pyautogui_fixture["hot_key_calls"] == ["('ctrl', 'c')"]


def test_wait(pyautogui_fixture: dict[str, list[str]]):
    wait(0.5)
    assert pyautogui_fixture["sleep_calls"] == ["0.5"]


def test_type(pyautogui_fixture: dict[str, list[str]]):
    type("Hello, World!")
    assert pyautogui_fixture["typewrite_calls"] == ["Hello, World!"]


def test_click(pyautogui_fixture: dict[str, list[str]]):
    click()
    click((100, 200))
    assert pyautogui_fixture["click_calls"] == ["(50, 50)", "(100, 200)"]


def test_get_click_position(pynput_fixture: None):
    result = get_click_position()
    assert result == (100, 200)


def test_get_selected_text(pyautogui_fixture: dict[str, list[str]], pyperclip_fixture: dict[str, list[str]]):
    result = get_selected_text()
    assert result == "Selected Text"
    assert pyautogui_fixture["hot_key_calls"] == [f"('{'ctrl' if os.name == 'nt' else 'command'}', 'c')"]
    assert pyperclip_fixture["paste_calls"] == ["Selected Text"]
