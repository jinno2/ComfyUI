"""Tests for WeightHook warnings about hook keys that match no model layer."""

from comfy import hooks


class FakePatcher:
    def __init__(self, applied_keys):
        self.applied_keys = applied_keys
        self.added_patches = None

    def add_hook_patches(self, hook, patches, strength_patch=1.0, strength_model=1.0):
        self.added_patches = dict(patches)
        return list(self.applied_keys)


def make_weight_hook(weights):
    hook = hooks.WeightHook()
    hook.need_weight_init = False
    hook.weights = weights
    return hook


def test_warns_only_for_unapplied_keys(caplog):
    hook = make_weight_hook({"applied": 1.0, "missing": 1.0})
    patcher = FakePatcher(["applied"])
    registered = hooks.HookGroup()

    with caplog.at_level("WARNING"):
        result = hook.add_hook_patches(patcher, {}, {}, registered)

    assert result is True
    assert registered.hooks == [hook]
    assert patcher.added_patches == {"applied": 1.0, "missing": 1.0}
    assert [record.getMessage() for record in caplog.records] == ["hook key not applied: missing"]


def test_no_warning_when_all_keys_applied(caplog):
    hook = make_weight_hook({"a": 1.0, "b": 1.0})
    patcher = FakePatcher(["a", "b"])
    registered = hooks.HookGroup()

    with caplog.at_level("WARNING"):
        result = hook.add_hook_patches(patcher, {}, {}, registered)

    assert result is True
    assert registered.hooks == [hook]
    assert caplog.records == []
