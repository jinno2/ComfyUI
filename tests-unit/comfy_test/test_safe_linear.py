"""safe_linear CUDA fallback behavior tests (all CPU-safe)."""

import pytest
import torch

import comfy.model_management
from comfy import ops


@pytest.fixture(autouse=True)
def _reset_force_matmul(monkeypatch):
    monkeypatch.setattr(ops, "CUDA_LINEAR_FORCE_MATMUL_DEVICES", set())


def _sample():
    torch.manual_seed(0)
    return torch.randn(3, 4), torch.randn(5, 4), torch.randn(5)


def test_safe_linear_prefers_f_linear_when_not_forced(monkeypatch):
    input, weight, bias = _sample()
    matmul_calls = []
    monkeypatch.setattr(ops, "_linear_via_matmul", lambda *a: matmul_calls.append(a))

    out = ops.safe_linear(input, weight, bias)

    torch.testing.assert_close(out, torch.nn.functional.linear(input, weight, bias))
    assert matmul_calls == []


def test_safe_linear_skips_fallback_for_cpu_tensors(monkeypatch):
    input, weight, bias = _sample()
    monkeypatch.setattr(ops, "CUDA_LINEAR_FORCE_MATMUL_DEVICES", {input.device})

    out = ops.safe_linear(input, weight, bias)

    torch.testing.assert_close(out, torch.nn.functional.linear(input, weight, bias))
    assert ops._can_use_cuda_linear_matmul_fallback(input, weight) is False


def test_safe_linear_uses_matmul_when_forced_for_device(monkeypatch):
    input, weight, bias = _sample()
    monkeypatch.setattr(ops, "CUDA_LINEAR_FORCE_MATMUL_DEVICES", {input.device})
    monkeypatch.setattr(ops, "_can_use_cuda_linear_matmul_fallback", lambda i, w: True)

    out = ops.safe_linear(input, weight, bias)

    torch.testing.assert_close(out, torch.matmul(input, weight.transpose(-1, -2)) + bias)


def test_safe_linear_retries_then_escalates_on_persistent_cublas_error(monkeypatch):
    input, weight, bias = _sample()

    def _explode(*args):
        raise RuntimeError("CUBLAS_STATUS_NOT_INITIALIZED")

    monkeypatch.setattr(torch.nn.functional, "linear", _explode)
    monkeypatch.setattr(ops, "_can_use_cuda_linear_matmul_fallback", lambda i, w: True)
    discarded = []
    monkeypatch.setattr(comfy.model_management, "discard_cuda_async_error", lambda device: discarded.append(device))
    monkeypatch.setattr(comfy.model_management, "soft_empty_cache", lambda: None)

    out = ops.safe_linear(input, weight, bias)

    torch.testing.assert_close(out, torch.matmul(input, weight.transpose(-1, -2)) + bias)
    assert discarded == [input.device]
    assert ops.CUDA_LINEAR_FORCE_MATMUL_DEVICES == {input.device}


def test_safe_linear_reraises_unrelated_errors(monkeypatch):
    input, weight, bias = _sample()

    def _explode(*args):
        raise RuntimeError("expected scalar type BFloat but found Float")

    monkeypatch.setattr(torch.nn.functional, "linear", _explode)
    monkeypatch.setattr(ops, "_can_use_cuda_linear_matmul_fallback", lambda i, w: True)

    with pytest.raises(RuntimeError, match="expected scalar type"):
        ops.safe_linear(input, weight, bias)

    assert ops.CUDA_LINEAR_FORCE_MATMUL_DEVICES == set()


def test_discard_cuda_async_error_allocates_on_requested_device(monkeypatch):
    devices = []

    class _FakeTensor:
        def __add__(self, other):
            return self

    def _fake_tensor(data, dtype=None, device=None):
        devices.append(device)
        return _FakeTensor()

    monkeypatch.setattr(torch, "tensor", _fake_tensor)
    monkeypatch.setattr(comfy.model_management, "synchronize", lambda: None)

    comfy.model_management.discard_cuda_async_error(torch.device("cpu"))
    comfy.model_management.discard_cuda_async_error()

    assert devices[:2] == [torch.device("cpu")] * 2
    assert devices[2:] == [comfy.model_management.get_torch_device()] * 2
