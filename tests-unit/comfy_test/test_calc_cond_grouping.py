"""Characterization tests for the shared conds-by-hooks grouping helper."""

import torch

from comfy import samplers


class FakePatcher:
    def __init__(self):
        self.prepared = []

    def prepare_hook_patches_current_keyframe(self, timestep, hooks, model_options):
        self.prepared.append(hooks)


class FakeModel:
    def __init__(self):
        self.current_patcher = FakePatcher()


def test_groups_plain_conds_under_none_key():
    x_in = torch.zeros(1, 4, 8, 8)
    timestep = torch.tensor([999.0])
    out_conds, out_counts, hooked, default_conds, has_default = samplers._group_conds_by_hooks(
        FakeModel(), [[{"model_conds": {}, "uuid": "u"}], [{"model_conds": {}, "uuid": "u"}]], x_in, timestep, {}
    )

    assert len(hooked[None]) == 2
    assert hooked[None][0][1] == 0
    assert hooked[None][1][1] == 1
    assert has_default is False
    assert default_conds == [[], []]
    torch.testing.assert_close(out_conds[0], torch.zeros_like(x_in))
    assert torch.all(out_counts[0] == 1e-37)


def test_default_conds_are_not_run_directly():
    x_in = torch.zeros(1, 4, 8, 8)
    timestep = torch.tensor([999.0])
    default_cond = {"default": True, "model_conds": {}, "uuid": "u"}
    _, _, hooked, default_conds, has_default = samplers._group_conds_by_hooks(
        FakeModel(), [[default_cond], [{"model_conds": {}, "uuid": "u"}]], x_in, timestep, {}
    )

    assert has_default is True
    assert len(hooked[None]) == 1
    assert default_conds[0] == [default_cond]
    assert default_conds[1] == []


def test_hooks_are_grouped_separately_and_keyframe_prepared():
    x_in = torch.zeros(1, 4, 8, 8)
    timestep = torch.tensor([999.0])
    hooks = object()
    model = FakeModel()
    conds = [[{"model_conds": {}, "uuid": "u", "hooks": hooks}], [{"model_conds": {}, "uuid": "u"}]]

    _, _, hooked, _, _ = samplers._group_conds_by_hooks(model, conds, x_in, timestep, {})

    assert set(hooked.keys()) == {hooks, None}
    assert len(hooked[hooks]) == 1
    assert model.current_patcher.prepared == [hooks]
