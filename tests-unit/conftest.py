import pytest

import comfy.memory_management


@pytest.fixture(autouse=True)
def _disable_dynamic_vram(monkeypatch):
    # Importing `main` (app_test) enables DynamicVRAM process-wide, which makes
    # disable_weight_init.Linear defer weight creation to state-dict loads.
    # Unit tests build modules and call forward directly, so pin the flag off
    # to keep the suite order-independent.
    monkeypatch.setattr(comfy.memory_management, "aimdo_enabled", False)
