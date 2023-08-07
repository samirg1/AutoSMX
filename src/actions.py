import os
from enum import Enum

import pyautogui

from automations import click, click_key, get_selected_text, type
from design import Item, Job, Test, TestJob

WINDOWS = os.name == "nt"


class KEYS(Enum):
    enter = "enter" if WINDOWS else "return"
    tab = "tab"
    shift_tab = "shift", "tab"
    ctrl_tab = "ctrl" if WINDOWS else "command", "tab"
    copy = "ctrl" if WINDOWS else "command", "c"
    right = "right"
    down = "down"


def get_item_job(item_number: str, asset_position: tuple[int, int], testing_position: tuple[int, int], window_position: tuple[int, int], jobs: dict[str, Job], job: Job | None = None) -> tuple[Item, Job]:
    click()
    type(item_number)
    click_key(KEYS.enter.value)
    click(asset_position)
    click_key(KEYS.tab.value)
    type(item_number)
    click_key(KEYS.enter.value)
    click_key(KEYS.tab.value, times=7)
    serial = get_selected_text()
    click_key(KEYS.tab.value)
    model = get_selected_text()
    click_key(KEYS.tab.value, times=2)
    description = get_selected_text()
    click_key(KEYS.tab.value, times=2)
    manufacturer = get_selected_text()

    item = Item(item_number, description, model, manufacturer, "None", "None", serial)

    click_key(KEYS.tab.value)
    company = get_selected_text()
    click_key(KEYS.tab.value)
    campus = get_selected_text()
    click_key(KEYS.tab.value)
    department = get_selected_text()
    click_key(KEYS.tab.value, times=21)
    click_key(KEYS.enter.value)

    click(testing_position)
    click(window_position)

    if job is None:
        return item, jobs.get(campus, Job(company, campus, department))
    return item, job


def complete_test(test: Test, area_position: tuple[int, int], comment_position: tuple[int, int]):
    click()
    click_key(KEYS.tab.value, times=5)
    click_key(KEYS.enter.value)
    click_key(*KEYS.ctrl_tab.value, times=2)

    click(area_position, times=2)
    click_key(KEYS.right.value)
    click_key(KEYS.down.value, times=test.script.downs)
    click_key(KEYS.enter.value)
    click_key(*KEYS.ctrl_tab.value)

    script_values = test.script_answers
    for i, value in enumerate(script_values):
        type(value, delay=0.5)
        if i != len(script_values) - 1:
            click_key(KEYS.tab.value)

    click_key(*KEYS.ctrl_tab.value)

    if test.testjobs:
        _navigate_to_sm_incident()
        for testjob in test.testjobs:
            _complete_testjob(testjob)

    click_key(*KEYS.ctrl_tab.value)
    if test.comment:
        click(comment_position)
        type(test.comment)
        click_key(*KEYS.shift_tab.value)

    type(test.final_result)
    click_key(KEYS.tab.value, times=7)
    # click_key(KEYS.enter.value)


def _navigate_to_sm_incident():
    click_key(KEYS.right.value)
    click_key(*KEYS.shift_tab.value)
    click_key(KEYS.right.value)
    click_key(KEYS.right.value)
    click_key(*KEYS.shift_tab.value)
    click_key(KEYS.right.value)
    click_key(*KEYS.shift_tab.value)
    click_key(KEYS.right.value)


def _complete_testjob(testjob: TestJob):
    type(testjob.department)
    click_key(KEYS.enter.value)
    type(testjob.contact_name)
    click_key(KEYS.enter.value, times=3)
    type(testjob.comment)
    click_key(KEYS.tab.value, times=9)
    click_key(KEYS.enter.value)