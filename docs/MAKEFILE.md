# Makefile

Cross-platform Makefile for ComfyUI development — handles macOS (Apple Silicon /
Intel) and Linux (NVIDIA CUDA), plus a one-shot smoke test that goes from
`make install` to a generated PNG.

The Makefile auto-detects the platform with `uname` and branches accordingly.
Run `make help` to see what's available in your environment.

## Quick start

```bash
make install        # create .venv and install dependencies
make smoke          # start server, generate one image, stop server
make device-info    # show platform / Python / torch backend
```

The smoke target assumes a checkpoint is present at
`models/checkpoints/v1-5-pruned-emaonly.safetensors`. Download one with:

```bash
curl -L -o models/checkpoints/v1-5-pruned-emaonly.safetensors \
  https://huggingface.co/stable-diffusion-v1-5/stable-diffusion-v1-5/resolve/main/v1-5-pruned-emaonly.safetensors
```

## Targets

### Setup

| Target           | What it does                                                |
| ---------------- | ----------------------------------------------------------- |
| `make install`   | Create `.venv`, install requirements, ensure torch ≥ 2.4    |
| `make full_install` | `clean` + `install` + `build`                            |
| `make update`    | `git pull` + `install` + `build`                            |
| `make full_update` | `clean` + `git pull` + `install` + `build`                |
| `make device-info` | Print platform, Python, torch backend (cuda / mps)        |

### Run

| Target      | What it does                                                |
| ----------- | ----------------------------------------------------------- |
| `make dev`  | Run with `--listen 0.0.0.0 --port 8188 --verbose`           |
| `make run`  | Production-style server (after `make build`)                |

### Service

Platform-conditional:

- **Linux** uses systemd (`systemctl start/stop/...`)
- **macOS** uses a lightweight background process managed via
  `.run/comfyui.pid` + `.run/comfyui.log`. For native launchd integration, see
  [`scripts/comfyui.plist.example`](../scripts/comfyui.plist.example).

| Target           | Linux                       | macOS                                |
| ---------------- | --------------------------- | ------------------------------------ |
| `make start`     | `sudo systemctl start ...`  | `nohup ... &`, writes `.run/comfyui.pid` |
| `make stop`      | `sudo systemctl stop ...`   | `kill $(cat .run/comfyui.pid)`        |
| `make restart`   | build + restart             | build + stop + start                  |
| `make status`    | `systemctl status`          | PID alive check                       |
| `make logs`      | `journalctl -u ... -f`      | `tail -f .run/comfyui.log`            |

### Test

| Target                  | What it does                       |
| ----------------------- | ---------------------------------- |
| `make test`             | unit + integration                 |
| `make test-unit`        | `tests-unit/` only                 |
| `make test-integration` | `tests/` only                      |

### Code quality

`make lint`, `make format`, and `make format-check` auto-install `ruff` into
the venv if missing (ruff is not in `requirements.txt` — it's a dev-only tool).

### Smoke test

`make smoke` runs the full pipeline:

1. Verifies a checkpoint is present in `models/checkpoints/`
2. Starts the server via `make start`
3. Polls `http://127.0.0.1:8188/` until ready (up to 90 s; ComfyUI boot is slow)
4. Runs [`scripts/generate_one.py`](../scripts/generate_one.py) which queues the
   default SD 1.5 workflow via the HTTP API, polls `/history/<id>` for
   completion, downloads the resulting PNG, and saves it to
   `output/comfyui_smoke.png`
5. Stops the server

If the server fails to bind within 90 s the smoke test prints the last 30 lines
of the log for debugging.

### Maintenance

| Target       | What it does                                       |
| ------------ | -------------------------------------------------- |
| `make build` | Install `comfyui-frontend-*` packages              |
| `make clean` | Remove `__pycache__`, `.pyc`, caches, `.run/`      |

## Configuration knobs

- `SERVICE_NAME` — systemd unit name on Linux (default: `comfyui`)

## Why this Makefile exists

The repo's `requirements.txt` ships an unpinned `torch`, which lets `uv` resolve
to `torch==2.2.2` on macOS arm64. That release predates `torch.library.custom_op`
(torch 2.4+), which `comfy-kitchen` relies on, so a fresh `uv pip install -r
requirements.txt` crashes on import. The Makefile's `_ensure-torch` step
upgrades torch after the install so this is invisible to users.

On macOS arm64, `uv venv --python python3` may auto-download an x86_64
interpreter under Rosetta, which then has no torch ≥ 2.4 wheels. `_create-venv`
walks Homebrew / mise paths first and falls back to a fresh `uv python install
3.13`.

See [`MAC.md`](./MAC.md) for the macOS-specific walkthrough.
