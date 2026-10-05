import os

import pytest

import comfy.memory_management


@pytest.fixture(autouse=True)
def _disable_dynamic_vram(monkeypatch):
    # Importing `main` (app_test) enables DynamicVRAM process-wide, which makes
    # disable_weight_init.Linear defer weight creation to state-dict loads.
    # Unit tests build modules and call forward directly, so pin the flag off
    # to keep the suite order-independent.
    monkeypatch.setattr(comfy.memory_management, "aimdo_enabled", False)


_collected = 0


def pytest_collection_finish(session):
    global _collected
    _collected = len(session.items)


def pytest_sessionfinish(session, exitstatus):
    # CI evidence consumers need the actual allocation: under xdist the native
    # "N workers [M items]" collection lines are that evidence, so stay silent.
    if session.config.pluginmanager.getplugin("xdist") is None:
        print(f"\npytest serial runtime: process={os.getpid()} collected={_collected}")  # noqa: T201
