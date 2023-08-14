import os
from enum import Enum
from typing import cast

from automations import click, click_key, get_selected_text, type, wait
from design.Item import Item
from design.Job import Job
from design.TestJob import TestJob
from design.Test import Test
from Storage import Positions

WINDOWS = os.name == "nt"


class KEYS(Enum):
    enter = "enter" if WINDOWS else "return"
    tab = "tab"
    shift_tab = "shift", "tab"
    ctrl_tab = "ctrl" if WINDOWS else "command", "tab"
    copy = "ctrl" if WINDOWS else "command", "c"
    right = "right"
    down = "down"


def get_item_job(item_number: str, positions: Positions, jobs: dict[str, Job], job: Job | None = None) -> tuple[Item, Job]:
    click()
    type(item_number)
    click_key(KEYS.enter.value)
    click(positions.assets_tab)
    wait(0.5)
    click_key(KEYS.tab.value)
    type(item_number)
    click_key(KEYS.enter.value)
    wait(0.5)
    click_key(KEYS.tab.value, times=7)
    serial = get_selected_text()
    click_key(KEYS.tab.value)
    model = get_selected_text()
    click_key(KEYS.tab.value, times=2)
    description = get_selected_text()
    click_key(KEYS.tab.value, times=2)
    manufacturer = get_selected_text()

    item = Item(item_number, description, model, manufacturer, "None", "None", serial)
    if job is None or job.campus == "Unknown":
        click_key(KEYS.tab.value)
        company = get_selected_text()
        click_key(KEYS.tab.value)
        campus = get_selected_text()
        click_key(KEYS.tab.value)
        department = get_selected_text()
        job = jobs.get(campus, Job(company, campus, department))

    click(positions.assets_tab)
    click_key(KEYS.tab.value, times=2)
    click_key(KEYS.enter.value)

    click(positions.testing_tab)
    wait(1)
    click(positions.window)
    wait(0.5)

    return item, cast(Job, job)  # type: ignore[redundant-cast]


def complete_test(test: Test, positions: Positions):
    click(positions.testing_tab)
    click_key(KEYS.tab.value, times=5)
    click_key(KEYS.enter.value)
    click_key(*KEYS.ctrl_tab.value, times=2)

    click(positions.show_all_script, times=2)
    click_key(KEYS.right.value)
    click_key(KEYS.down.value, times=test.script.downs)
    click_key(KEYS.enter.value)
    click_key(*KEYS.ctrl_tab.value)
    wait(0.5)

    for i, value in enumerate(test.script_answers):
        type(value)
        if i != len(test.script_answers) - 1:
            click_key(KEYS.tab.value)

    if test.script.nickname == "TRACK":
        click(positions.track_weight_field, times=2)
        type(test.script_answers[-3])

    click_key(*KEYS.ctrl_tab.value)

    if test.testjobs:
        wait(0.5)
        _navigate_to_sm_incident()
        for testjob in test.testjobs:
            _complete_testjob(testjob)

    click_key(*KEYS.ctrl_tab.value)
    if test.comment:
        click(positions.comment_box)
        type(test.comment)
        click_key(*KEYS.shift_tab.value)

    type(test.final_result)
    click_key(KEYS.tab.value, times=7)
    # click_key(KEYS.enter.value)
    # click(positions.window)


def _navigate_to_sm_incident():
    click_key(KEYS.right.value)
    wait(0.1)
    click_key(*KEYS.shift_tab.value)
    wait(0.1)
    click_key(KEYS.right.value)
    wait(0.1)
    click_key(KEYS.right.value)
    wait(0.1)
    click_key(*KEYS.shift_tab.value)
    click_key(KEYS.right.value)
    wait(0.1)
    click_key(*KEYS.shift_tab.value)
    wait(0.1)
    click_key(KEYS.right.value)


def _complete_testjob(testjob: TestJob):
    type(testjob.department)
    click_key(KEYS.enter.value)
    type(testjob.contact_name)
    click_key(KEYS.enter.value, times=3)
    type(testjob.comment)
    click_key(KEYS.tab.value, times=9)
    click_key(KEYS.enter.value)
