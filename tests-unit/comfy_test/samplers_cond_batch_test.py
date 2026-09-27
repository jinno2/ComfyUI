"""_calc_cond_batch single-GPU and multigpu fallback paths must agree.

Both paths share grouping, memory-fit planning, and output accumulation; the
multigpu path layers per-device scheduling and dispatch on top. Running the
real functions against a stub model keeps the two behaviors locked together.
"""

import torch

import comfy.samplers


class StubPatcher:
    def prepare_hook_patches_current_keyframe(self, timestep, hooks, model_options):
        pass

    def prepare_state(self, timestep, model_options):
        pass

    def apply_hooks(self, hooks=None):
        return {}

    def get_free_memory(self, device):
        return 1 << 40


class StubCondTensor:
    def __init__(self, tensor):
        self.tensor = tensor

    def can_concat(self, other):
        return True

    def size(self):
        return self.tensor.size()

    def concat(self, others):
        return StubCondTensor(torch.cat([self.tensor] + [o.tensor for o in others]))

    def to(self, device):
        return StubCondTensor(self.tensor.to(device))


class StubCondValue:
    def __init__(self, value):
        self.value = value

    def process_cond(self, batch_size, area=None):
        return StubCondTensor(torch.full([batch_size, 4, 8], self.value))


class StubModel:
    def __init__(self):
        self.current_patcher = StubPatcher()
        self.batch_sizes = []

    def memory_required(self, input_shape, cond_shapes=None):
        return 1.0

    def apply_model(self, input_x, timestep, **c):
        self.batch_sizes.append(input_x.shape[0])
        return input_x + timestep.view(-1, 1, 1, 1)


def _cond(value, uuid="u"):
    return {"uuid": uuid, "model_conds": {"c_crossattn": StubCondValue(value)}}


def _model_options(clone_model=None):
    options = {"transformer_options": {"sample_sigmas": torch.linspace(1.0, 0.0, 6)}}
    if clone_model is not None:
        clone = type("Clone", (), {"model": clone_model})
        options["multigpu_clones"] = {torch.device("cpu"): clone}
    return options


def _run(model, conds, x_in, timestep, clone_model=None):
    return comfy.samplers._calc_cond_batch(model, conds, x_in, timestep, _model_options(clone_model))


def test_single_and_multigpu_fallback_agree():
    x_in = torch.arange(2 * 4 * 8 * 8, dtype=torch.float32).reshape(2, 4, 8, 8)
    timestep = torch.tensor([999.0, 999.0])
    conds = [[_cond(1.0, "a")], [_cond(-1.0, "b")]]

    single_model = StubModel()
    out_single = _run(single_model, conds, x_in, timestep)

    multi_model = StubModel()
    out_multi = _run(multi_model, conds, x_in, timestep, clone_model=multi_model)

    assert len(out_single) == len(out_multi) == 2
    for a, b in zip(out_single, out_multi):
        assert torch.equal(a, b)
    # free memory is ample, so both conds concatenate into one apply_model call
    assert single_model.batch_sizes == [4]
    assert multi_model.batch_sizes == [4]


def test_single_and_multigpu_fallback_agree_with_areas():
    x_in = torch.zeros([2, 4, 8, 8])
    timestep = torch.tensor([500.0, 500.0])
    conds = [
        [{"uuid": "a", "area": (8, 8, 0, 0), "model_conds": {"c_crossattn": StubCondValue(1.0)}}],
        [{"uuid": "b", "area": (4, 4, 4, 4), "model_conds": {"c_crossattn": StubCondValue(-1.0)}}],
    ]

    single_model = StubModel()
    out_single = _run(single_model, conds, x_in, timestep)

    multi_model = StubModel()
    out_multi = _run(multi_model, conds, x_in, timestep, clone_model=multi_model)

    for a, b in zip(out_single, out_multi):
        assert torch.equal(a, b)
    # different areas cannot concatenate, so each cond runs as its own batch
    assert single_model.batch_sizes == [2, 2]
    assert multi_model.batch_sizes == [2, 2]
