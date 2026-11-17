import pytest
import torch

from comfy import samplers

DEVICES = ["cpu"] + (["cuda"] if torch.cuda.is_available() else [])


def _resolve_mask_area(mask, dims):
    conditions = [{"mask": mask, "set_area_to_bounds": True}]
    samplers.resolve_areas_and_cond_masks_multidim(conditions, dims, mask.device)
    return conditions[0]


@pytest.mark.parametrize("device", DEVICES)
def test_mask_bounds_preserve_2d_area_order_and_minimum_size(device):
    mask = torch.zeros((1, 12, 16), device=device)
    mask[0, 2:8, 5:14] = 1

    condition = _resolve_mask_area(mask, (12, 16))

    assert condition["area"] == (8, 9, 2, 5)


@pytest.mark.parametrize("device", DEVICES)
def test_empty_2d_mask_bounds_are_noop_area(device):
    mask = torch.zeros((1, 12, 16), device=device)

    condition = _resolve_mask_area(mask, (12, 16))

    assert condition["area"] == (8, 8, 0, 0)


@pytest.mark.parametrize("device", DEVICES)
def test_empty_mask_bounds_are_noop_area_for_all_dimensions(device):
    mask = torch.zeros((1, 10, 12, 16), device=device)

    condition = _resolve_mask_area(mask, (10, 12, 16))

    assert condition["area"] == (1, 8, 8, 0, 0, 0)


@pytest.mark.parametrize("device", DEVICES)
def test_3d_mask_bounds_align_with_sampler_area_contract(device):
    mask = torch.zeros((1, 10, 12, 16), device=device)
    mask[0, 2:5, 4:10, 5:14] = 1
    condition = _resolve_mask_area(mask, (10, 12, 16))
    condition.update(model_conds={}, uuid="mask-bounds")
    x_in = torch.zeros((1, 4, 10, 12, 16), device=device)

    resolved = samplers.get_area_and_mult(condition, x_in, torch.tensor([1.0], device=device))

    assert condition["area"] == (3, 8, 9, 2, 4, 5)
    assert resolved.input_x.shape == (1, 4, 3, 8, 9)
    torch.testing.assert_close(resolved.input_x, x_in[:, :, 2:5, 4:12, 5:14])
    torch.testing.assert_close(resolved.mult, mask[:, None, 2:5, 4:12, 5:14].repeat(1, 4, 1, 1, 1))
