# macOS setup notes

ComfyUI runs on Apple Silicon (M1/M2/M3/M4) and Intel Macs. This document
covers the Apple Silicon path; Intel Macs follow the same steps but use the CPU
backend (no MPS).

## Prerequisites

- macOS 14 (Sonoma) or later — required for recent PyTorch wheels
- Python 3.12 or 3.13 (arm64 build). Either:
  - **Homebrew**: `brew install python` (creates `/opt/homebrew/bin/python3`)
  - **mise**: install Python via `mise use python@3.13`
- [`uv`](https://docs.astral.sh/uv/) (`brew install uv` or
  `curl -LsSf https://astral.sh/uv/install.sh | sh`)

## First-time setup

```bash
git clone <repo-url> comfyui
cd comfyui
make install        # auto-detects arm64 Python, creates .venv, installs deps
make device-info    # confirm torch can see MPS
```

`make device-info` should print something like:

```
Platform
  uname:        Darwin arm64
  has nvidia:   no
  ProductName:		macOS
  ProductVersion:		26.5
  BuildVersion:		25F71

Python
Python 3.14.5

Torch backend
  torch:        2.12.1
  cuda:         False
  mps:          True
```

If `mps: False`, your Python interpreter is x86_64 (Rosetta). Re-check the
preceding step — the Makefile walks Homebrew and mise paths before falling back
to a uv-managed interpreter, so a wrong `PATH` is the most common cause.

## Downloading a model

`models/checkpoints/` ships empty. For a smoke test, SD 1.5 is the smallest
option that matches ComfyUI's example workflow:

```bash
curl -L -o models/checkpoints/v1-5-pruned-emaonly.safetensors \
  https://huggingface.co/stable-diffusion-v1-5/stable-diffusion-v1-5/resolve/main/v1-5-pruned-emaonly.safetensors
```

(~4 GB; takes a few minutes on a typical home connection.)

## Running the server

Foreground (interactive):

```bash
make dev
```

Background (logs to `.run/comfyui.log`, PID to `.run/comfyui.pid`):

```bash
make start
make status
make logs          # Ctrl+C to stop tailing
make stop
```

## Smoke test

```bash
make smoke
```

This starts the server, runs `scripts/generate_one.py` (which queues the SD 1.5
workflow via the HTTP API and downloads the result), and stops the server. The
PNG lands in `output/comfyui_smoke.png`.

## Launchd (optional)

For a persistent service that starts on login, copy
[`scripts/comfyui.plist.example`](../scripts/comfyui.plist.example) to
`~/Library/LaunchAgents/com.yourorg.comfyui.plist`, edit the path placeholders,
then:

```bash
launchctl load -w ~/Library/LaunchAgents/com.yourorg.comfyui.plist
launchctl unload ~/Library/LaunchAgents/com.yourorg.comfyui.plist   # to stop
tail -f ~/Library/Logs/com.yourorg.comfyui.out.log
```

## Why MPS, not CUDA

NVIDIA GPUs are not supported on macOS. The PyTorch wheels for `macosx_*_arm64`
ship with the Metal Performance Shaders (MPS) backend instead of CUDA. The rest
of ComfyUI's CUDA-specific code paths (e.g. `comfy-aimdo`) gracefully report
unavailable on Darwin and the rest of the pipeline runs on MPS.

## Known limitations on Apple Silicon

- Generation is slower than a comparable NVIDIA GPU. SD 1.5 at 512×512, 20
  steps takes ~30–60 s on M-series Pro/Max; longer on base models.
- The `comfy-aimdo` package (which optimises inference on Windows / Linux
  NVIDIA) is not supported on Darwin and reports `unsupported operating system`
  at startup — this is harmless.
- A few nodes assume CUDA memory semantics and may not behave identically on
  MPS. The default SD 1.5 workflow works without modifications.

## Troubleshooting

**`AttributeError: module 'torch.library' has no attribute 'custom_op'`**

The installed torch is too old (< 2.4). The Makefile's `_ensure-torch` step
should prevent this; if you see it, run `make install` again to force the
upgrade path.

**`torch.cuda.is_available()` is False — that's correct on Mac**

NVIDIA GPUs aren't supported on macOS. Check `torch.backends.mps.is_available()`
instead. If MPS is False, your interpreter is x86_64; reinstall with an arm64
Python (see Prerequisites).

**The server boots but generation fails silently**

Check `.run/comfyui.log`. The `Using sub quadratic optimization for attention`
line indicates the server reached the scheduler stage. If a generation error
appears after that, the most common cause is an out-of-memory condition on
larger models — close other GPU-intensive apps or use a smaller model.

**`make smoke` says the server didn't bind within 90 s**

ComfyUI's import chain is heavy (torch + transformers + comfy_kitchen + custom
ops + alembic DB migrations). On a cold start with many apps open, it can take
over 60 s to reach `Starting server`. The 90 s budget should cover normal use;
if not, increase it in `Makefile` (`_smoke-wait-and-run`).
