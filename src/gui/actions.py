import os
from enum import Enum
from typing import cast

from design.Item import Item
from design.Job import Job
from design.Test import Test
from design.TestJob import TestJob
from design.data import SCRIPT_DOWNS
from gui.automations import click, click_key, get_selected_text, type, wait
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


def get_item_job(item_number: str, positions: Positions, jobs: dict[str, Job], job: Job | None = None) -> tuple[Item, Job]:
    click(positions.testing_tab)  # enter item number into testing tab
    click_key(_KEYS.tab.value, times=5)
    type(item_number)
    click_key(_KEYS.enter.value)

    click(positions.assets_tab)  # enter item number into assets tab
    wait(0.5)
    click_key(_KEYS.tab.value)
    type(item_number)
    click_key(_KEYS.enter.value)
    wait(0.5)

    click_key(_KEYS.tab.value, times=5)  # get to serial number
    previous = get_selected_text()
    click_key(_KEYS.tab.value)
    next = get_selected_text()
    if next != previous:
        serial = next
        final_tabs = 3
    else:
        click_key(_KEYS.tab.value)
        serial = get_selected_text()
        final_tabs = 2

    click_key(_KEYS.tab.value)  # get rest of information
    model = get_selected_text()
    click_key(_KEYS.tab.value, times=2)
    description = get_selected_text()
    click_key(_KEYS.tab.value, times=2)
    manufacturer = get_selected_text()

    item = Item(item_number, description, model, manufacturer, serial)
    if job is None or job.campus == "Unknown":  # get job if needed
        click_key(_KEYS.tab.value)
        company = get_selected_text()
        click_key(_KEYS.tab.value)
        campus = get_selected_text()
        click_key(_KEYS.tab.value)
        department = get_selected_text()
        job = jobs.get(campus, Job(company, campus, department))

    click(positions.assets_tab)  # exit assets tab
    click_key(_KEYS.tab.value, times=final_tabs)
    click_key(_KEYS.enter.value)

    click(positions.testing_tab)  # reset
    wait(1)
    click(positions.window)
    wait(0.5)

    return item, cast(Job, job)  # type: ignore[redundant-cast]


def complete_test(test: Test, positions: Positions):  # pragma: no cover
    click(positions.testing_tab)  # go to scripts tab
    click_key(_KEYS.tab.value, times=5)
    click_key(_KEYS.enter.value)
    click_key(*_KEYS.ctrl_tab.value, times=2)

    click(positions.show_all_script, times=2)  # find and select script
    click_key(_KEYS.right.value)
    click_key(_KEYS.down.value, times=SCRIPT_DOWNS[test.script.nickname])
    click_key(_KEYS.enter.value)
    click_key(*_KEYS.ctrl_tab.value)
    wait(0.5)

    for i, value in enumerate(test.script_answers):  # enter script answers
        type(value)
        if i != len(test.script_answers) - 1:
            click_key(_KEYS.tab.value)

    if test.script.nickname == "TRACK":  # enter track weight if needed
        click(positions.track_weight_field, times=2)
        type(test.script_answers[-3])

    click_key(*_KEYS.ctrl_tab.value)  # enter testjobs if needed
    if test.testjobs:
        wait(0.5)
        _navigate_to_sm_incident()
        for testjob in test.testjobs:
            _complete_testjob(testjob)

    click_key(*_KEYS.ctrl_tab.value)  # enter comment if needed
    if test.comment:
        click(positions.comment_box)
        type(test.comment)
        click_key(*_KEYS.shift_tab.value)

    type(test.final_result)  # finish test
    click_key(_KEYS.tab.value, times=7)
    # click_key(KEYS.enter.value)
    # click(positions.window)


def _navigate_to_sm_incident():
    delay = 0.1
    click_key(_KEYS.right.value)
    wait(delay)
    click_key(*_KEYS.shift_tab.value)
    wait(delay)
    click_key(_KEYS.right.value)
    wait(delay)
    click_key(_KEYS.right.value)
    wait(delay)
    click_key(*_KEYS.shift_tab.value)
    click_key(_KEYS.right.value)
    wait(delay)
    click_key(*_KEYS.shift_tab.value)
    wait(delay)
    click_key(_KEYS.right.value)


def _complete_testjob(testjob: TestJob):
    type(testjob.department)
    click_key(_KEYS.enter.value)
    type(testjob.contact_name)
    click_key(_KEYS.enter.value, times=3)
    type(testjob.comment)
    click_key(_KEYS.tab.value, times=9)
    click_key(_KEYS.enter.value)
