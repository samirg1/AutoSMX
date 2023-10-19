import ctypes
import os
import subprocess
from enum import Enum

from design.data import SCRIPT_DOWNS
from design.Job import Job
from design.Test import Test
from gui.automations import click, click_key, type, wait
from storage.Storage import Positions

_WINDOWS = os.name == "nt"


class _KEYS(Enum):
    enter = "enter" if _WINDOWS else "return"
    tab = "tab"
    shift_tab = "shift", "tab"
    ctrl_tab = "ctrl" if _WINDOWS else "command", "tab"
    copy = "ctrl" if _WINDOWS else "command", "c"
    right = "right"
    down = "down"


def _enter_item_number(item_number: str, testing_tab_position: tuple[int, int] | None) -> None:
    click(testing_tab_position)  # enter item number into testing tab
    click_key(_KEYS.tab.value, times=5)
    type(item_number)
    click_key(_KEYS.enter.value)
    wait(0.5)


def complete_test(test: Test, positions: Positions, is_editing: bool) -> None:  # pragma: no cover
    _enter_item_number(test.item.number, positions.testing_tab)
    click_key(*_KEYS.ctrl_tab.value)
    if is_editing:
        click_key(_KEYS.enter.value)
        wait(1)
        click_key(_KEYS.tab.value, times=5)
    else:
        click_key(*_KEYS.ctrl_tab.value)
        click(positions.show_all_script, times=2)  # find and select script
        click_key(_KEYS.right.value)
        click_key(_KEYS.down.value, times=SCRIPT_DOWNS[test.script.number])
        click_key(_KEYS.enter.value)
        click_key(*_KEYS.ctrl_tab.value)
        wait(1)

    for i, value in enumerate(test.script_answers):  # enter script answers
        type(value)
        if i != len(test.script_answers) - 1:
            click_key(_KEYS.tab.value)

    if test.script.nickname == "TRACK":  # enter track weight if needed
        click(positions.track_weight_field, times=2)
        type(test.script_answers[-3])

    click_key(*_KEYS.ctrl_tab.value)  # enter testjobs if needed
    if test.jobs:
        wait(0.5)
        click(positions.sm_incident_tab)
        for testjob in test.jobs:
            _complete_testjob(testjob)

    click_key(*_KEYS.ctrl_tab.value)  # enter comment if needed
    if test.comment:
        click(positions.comment_box)
        type(test.comment)
        click_key(*_KEYS.shift_tab.value)

    type(test.final_result)  # finish test
    click_key(_KEYS.tab.value, times=7)


def _complete_testjob(testjob: Job) -> None:
    type(testjob.department)
    click_key(_KEYS.enter.value)
    type(testjob.contact_name)
    click_key(_KEYS.enter.value, times=3)
    type(testjob.comment)
    click_key(_KEYS.tab.value, times=9)
    click_key(_KEYS.enter.value)


def turn_off_capslock() -> None:
    try:
        subprocess.run(["osascript", "-l", "JavaScript", "src/gui/capslock_off.applescript"])
        return
    except OSError:
        ...

    try:
        if ctypes.WinDLL("User32.dll").GetKeyState(0x14):  # type: ignore
            click_key("capslock")
    except AttributeError:
        ...
