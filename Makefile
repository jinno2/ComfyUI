# =============================================================================
# ComfyUI Makefile
# Cross-platform: macOS (Apple Silicon / Intel) and Linux (NVIDIA CUDA)
# =============================================================================

.DEFAULT_GOAL := help

# ---- Platform detection -----------------------------------------------------

UNAME_S := $(shell uname -s)
ifeq ($(UNAME_S),Darwin)
    PLATFORM      := macos
    PLATFORM_ARCH  := $(shell uname -m)
    PYTHON_BIN     := python3
    VENV_BIN       := .venv/bin
    HAS_NVIDIA     := no
    SERVICE_HINT   := launchd
else
    PLATFORM      := linux
    PLATFORM_ARCH  := $(shell uname -m)
    PYTHON_BIN     := python3
    VENV_BIN       := .venv/bin
    HAS_NVIDIA     := $(shell command -v nvidia-smi >/dev/null 2>&1 && echo yes || echo no)
    SERVICE_HINT   := systemd
endif

# ---- Configuration ----------------------------------------------------------

PYTHON         := $(VENV_BIN)/python
VENV           := .venv
SERVICE_NAME  ?= comfyui
PROJECT_NAME   := ComfyUI

# Minimum torch version compatible with comfy-kitchen 0.2.8
# (uses torch.library.custom_op, added in torch 2.4).
TORCH_MIN      := 2.4

# ---- Colors ----------------------------------------------------------------

BLUE    := \033[1;34m
GREEN   := \033[1;32m
YELLOW  := \033[1;33m
CYAN    := \033[1;36m
RED     := \033[1;31m
DIM     := \033[2m
BOLD    := \033[1m
RESET   := \033[0m

# ---- Prerequisite helpers ---------------------------------------------------

.PHONY: _ensure-uv
_ensure-uv:
	@which uv > /dev/null 2>&1 || (echo "$(YELLOW)uv not found. Installing...$(RESET)" && curl -LsSf https://astral.sh/uv/install.sh | sh)

# On macOS arm64, `uv venv --python python3` may auto-download an x86_64
# interpreter under Rosetta, which then has no torch 2.4+ wheels. Walk
# well-known locations for an arm64 build first.
.PHONY: _create-venv
_create-venv:
	@if [ ! -d "$(VENV)" ]; then \
		PY="$(PYTHON_BIN)"; \
		if [ "$(PLATFORM)" = "macos" ] && [ "$(PLATFORM_ARCH)" = "arm64" ]; then \
			PY=$$(for p in /opt/homebrew/bin/python3 \
			            /opt/homebrew/opt/python@3.13/bin/python3 \
			            /opt/homebrew/opt/python@3.12/bin/python3 \
			            $(HOME)/.local/share/mise/installs/python/3.13/bin/python3 \
			            $(HOME)/.local/share/mise/installs/python/3.12/bin/python3 \
			            /usr/local/bin/python3; do \
			    [ -x "$$p" ] && file "$$p" 2>/dev/null | grep -q arm64 && echo "$$p" && break; \
			  done); \
			if [ -n "$$PY" ]; then \
				echo "$(DIM)Using arm64 python: $$PY$(RESET)"; \
			else \
				echo "$(YELLOW)No arm64 python found — letting uv download 3.13$(RESET)"; \
				PY="3.13"; \
			fi; \
		fi; \
		echo "$(CYAN)Creating virtualenv at $(VENV)$(RESET)"; \
		uv venv $(VENV) --python "$$PY"; \
	fi

# =============================================================================
# Primary targets
# =============================================================================

.PHONY: help
help: ## Show this help
	@echo ""
	@echo "$(BOLD)$(PROJECT_NAME)$(RESET) $(DIM)(platform: $(PLATFORM)/$(PLATFORM_ARCH), nvidia: $(HAS_NVIDIA), service: $(SERVICE_HINT))$(RESET)"
	@echo ""
	@echo "$(BLUE)Setup$(RESET)"
	@echo "  $(GREEN)make install$(RESET)            Create .venv and install Python dependencies (uv pip)"
	@echo "  $(GREEN)make full_install$(RESET)      Clean everything, then install + build from scratch"
	@echo "  $(GREEN)make update$(RESET)            git pull && install && build"
	@echo "  $(GREEN)make full_update$(RESET)       Clean + full update (nuclear option)"
	@echo "  $(GREEN)make device-info$(RESET)       Show detected platform + Python + torch backend"
	@echo ""
	@echo "$(BLUE)Run$(RESET)"
	@echo "  $(GREEN)make dev$(RESET)               Start dev server on :8188 (verbose logs)"
	@echo "  $(GREEN)make run$(RESET)               Start production server on :8188"
	@echo ""
ifeq ($(PLATFORM),macos)
	@echo "$(BLUE)Service (macOS: launchd)$(RESET)"
	@echo "  $(GREEN)make start$(RESET)             Start ComfyUI in background (writes PID to .run/comfyui.pid)"
	@echo "  $(GREEN)make stop$(RESET)              Stop the background process"
	@echo "  $(GREEN)make restart$(RESET)           Build + stop + start"
	@echo "  $(GREEN)make status$(RESET)            Show background process status"
	@echo "  $(GREEN)make logs$(RESET)              Tail background logs (Ctrl+C to stop)"
	@echo "  $(DIM)For native launchd integration, see scripts/comfyui.plist.example$(RESET)"
else
	@echo "$(BLUE)Service (systemd: $(SERVICE_NAME))$(RESET)"
	@echo "  $(GREEN)make start$(RESET)             sudo systemctl start $(SERVICE_NAME)"
	@echo "  $(GREEN)make stop$(RESET)              sudo systemctl stop $(SERVICE_NAME)"
	@echo "  $(GREEN)make restart$(RESET)           Build + sudo systemctl restart $(SERVICE_NAME)"
	@echo "  $(GREEN)make status$(RESET)            Show systemd unit status"
	@echo "  $(GREEN)make logs$(RESET)              Tail journalctl logs (Ctrl+C to stop)"
endif
	@echo ""
	@echo "$(BLUE)Test$(RESET)"
	@echo "  $(GREEN)make test$(RESET)              Run all tests (tests-unit/ + tests/)"
	@echo "  $(GREEN)make test-unit$(RESET)         Run unit tests only (tests-unit/)"
	@echo "  $(GREEN)make test-integration$(RESET)  Run integration tests only (tests/)"
	@echo ""
	@echo "$(BLUE)Code quality$(RESET)"
	@echo "  $(GREEN)make lint$(RESET)              Check code with ruff (no changes)"
	@echo "  $(GREEN)make format$(RESET)            Auto-fix lint issues + format code"
	@echo "  $(GREEN)make format-check$(RESET)      Check if formatting is clean (CI-friendly)"
	@echo ""
	@echo "$(BLUE)Maintenance$(RESET)"
	@echo "  $(GREEN)make clean$(RESET)             Delete __pycache__, .pyc, .egg-info, caches"
	@echo "  $(GREEN)make build$(RESET)             Install frontend packages (comfyui-frontend-*)"
	@echo ""
	@echo "$(BLUE)Smoke test$(RESET)"
	@echo "  $(GREEN)make smoke$(RESET)             Start server + run one image generation (needs a checkpoint in models/checkpoints/)"
	@echo ""

# ---- Install ----------------------------------------------------------------

.PHONY: install
install: _ensure-uv _create-venv ## Create .venv (if needed) and install dependencies
	@echo "$(CYAN)Installing Python deps via uv pip into $(VENV)$(RESET)"
	uv pip install --python $(PYTHON) -r requirements.txt
	@if [ -f manager_requirements.txt ]; then \
		echo "$(CYAN)Installing manager requirements$(RESET)"; \
		uv pip install --python $(PYTHON) -r manager_requirements.txt; \
	fi
	@if [ -f tests-unit/requirements.txt ]; then \
		echo "$(CYAN)Installing test requirements$(RESET)"; \
		uv pip install --python $(PYTHON) -r tests-unit/requirements.txt; \
	fi
	@$(MAKE) --no-print-directory _ensure-torch
	@echo "$(GREEN)✓ install complete$(RESET)"
	@$(MAKE) --no-print-directory _post-install-hint

# Bump torch if the requirements.txt-resolved version is too old for
# comfy-kitchen (uses torch.library.custom_op, added in torch 2.4).
.PHONY: _ensure-torch
_ensure-torch:
	@CUR=$$($(PYTHON) -c "import torch;print(torch.__version__.split('+')[0])" 2>/dev/null); \
	if [ -z "$$CUR" ] || [ "$$(printf '%s\n%s' "$$CUR" "$(TORCH_MIN)" | sort -V | head -n1)" != "$(TORCH_MIN)" ]; then \
		echo "$(YELLOW)torch $$CUR < $(TORCH_MIN) — upgrading to >=$(TORCH_MIN) for comfy_kitchen$(RESET)"; \
		uv pip install --python $(PYTHON) --upgrade "torch>=$(TORCH_MIN)" torchvision torchaudio; \
	else \
		echo "$(DIM)torch $$CUR >= $(TORCH_MIN) — ok$(RESET)"; \
	fi

# Backend-specific install hint (informational, not strictly required for the
# default PyTorch wheels, but useful when an existing install is broken).
.PHONY: _post-install-hint
_post-install-hint:
ifeq ($(PLATFORM),macos)
	@echo ""
	@echo "$(DIM)macOS detected: PyTorch installed via requirements.txt already includes"
	@echo "MPS (Metal) wheels for Apple Silicon. To verify, run:$(RESET)"
	@echo "  $(CYAN)./.venv/bin/python -c 'import torch;print(\"mps:\", torch.backends.mps.is_available())'$(RESET)"
else ifeq ($(HAS_NVIDIA),yes)
	@echo ""
	@echo "$(DIM)NVIDIA GPU detected. To verify CUDA inside the venv, run:$(RESET)"
	@echo "  $(CYAN)./.venv/bin/python -c 'import torch;print(\"cuda:\", torch.cuda.is_available())'$(RESET)"
else
	@echo ""
	@echo "$(DIM)No NVIDIA GPU detected on Linux. ComfyUI will fall back to CPU.$(RESET)"
endif

.PHONY: full_install
full_install: clean install build ## Clean install + build from scratch

.PHONY: update
update: ## git pull + install + build
	git pull
	$(MAKE) install
	$(MAKE) build

.PHONY: full_update
full_update: clean ## Clean + update (full rebuild)
	git pull
	$(MAKE) install
	$(MAKE) build

# ---- Build ------------------------------------------------------------------

.PHONY: build
build: ## Build frontend package (pip install comfyui deps)
	@echo "$(CYAN)Installing comfyui-frontend-* packages$(RESET)"
	uv pip install --python $(PYTHON) comfyui-frontend-package comfyui-workflow-templates comfyui-embedded-docs

# ---- Run --------------------------------------------------------------------

.PHONY: dev
dev: ## Run in development mode (with auto-reload)
	$(PYTHON) main.py --listen 0.0.0.0 --port 8188 --verbose

.PHONY: run
run: build ## Run in production mode
	$(PYTHON) main.py --listen 0.0.0.0 --port 8188

# ---- Service management (platform-conditional) -----------------------------

ifeq ($(PLATFORM),macos)
# macOS: lightweight background process (no systemd, no launchd plist needed).
PIDFILE := .run/comfyui.pid
LOGFILE := .run/comfyui.log

.PHONY: start
start: ## Start ComfyUI in background
	@mkdir -p .run
	@if [ -f $(PIDFILE) ] && kill -0 $$(cat $(PIDFILE)) 2>/dev/null; then \
		echo "$(YELLOW)Already running (PID $$(cat $(PIDFILE)))$(RESET)"; \
	else \
		echo "$(GREEN)Starting ComfyUI in background...$(RESET)"; \
		nohup $(PYTHON) main.py --listen 0.0.0.0 --port 8188 > $(LOGFILE) 2>&1 & \
		echo $$! > $(PIDFILE); \
		sleep 1; \
		echo "$(GREEN)Started (PID $$(cat $(PIDFILE))). Logs: tail -f $(LOGFILE)$(RESET)"; \
	fi

.PHONY: stop
stop: ## Stop the background ComfyUI process
	@if [ -f $(PIDFILE) ] && kill -0 $$(cat $(PIDFILE)) 2>/dev/null; then \
		echo "$(YELLOW)Stopping PID $$(cat $(PIDFILE))...$(RESET)"; \
		kill $$(cat $(PIDFILE)); \
		rm -f $(PIDFILE); \
		echo "$(GREEN)Stopped$(RESET)"; \
	else \
		echo "$(DIM)Not running$(RESET)"; \
		rm -f $(PIDFILE); \
	fi

.PHONY: restart
restart: build ## Build + stop + start
	$(MAKE) stop
	$(MAKE) start

.PHONY: status
status: ## Show background process status
	@if [ -f $(PIDFILE) ] && kill -0 $$(cat $(PIDFILE)) 2>/dev/null; then \
		echo "$(GREEN)running$(RESET) (PID $$(cat $(PIDFILE)))"; \
	else \
		echo "$(DIM)stopped$(RESET)"; \
	fi

.PHONY: logs
logs: ## Tail background logs
	@echo "$(DIM)Tailing $(LOGFILE) (Ctrl+C to stop)$(RESET)"
	@tail -f $(LOGFILE)
else
# Linux: systemd
.PHONY: start
start: ## Start the systemd service
	sudo systemctl start $(SERVICE_NAME)

.PHONY: stop
stop: ## Stop the systemd service
	sudo systemctl stop $(SERVICE_NAME)

.PHONY: restart
restart: build ## Build + restart the systemd service
	sudo systemctl restart $(SERVICE_NAME)

.PHONY: status
status: ## Show systemd service status
	sudo systemctl status $(SERVICE_NAME) --no-pager

.PHONY: logs
logs: ## Tail systemd service logs
	journalctl -u $(SERVICE_NAME) -f
endif

# ---- Diagnostics ------------------------------------------------------------

.PHONY: device-info
device-info: ## Show platform, Python, and torch backend
	@echo "$(BOLD)Platform$(RESET)"
	@echo "  uname:        $(UNAME_S) $(PLATFORM_ARCH)"
	@echo "  has nvidia:   $(HAS_NVIDIA)"
ifeq ($(PLATFORM),macos)
	@sw_vers 2>/dev/null | sed 's/^/  /'
endif
	@echo ""
	@echo "$(BOLD)Python$(RESET)"
	@$(PYTHON) -V 2>/dev/null || echo "  (venv not created — run 'make install')"
	@echo ""
	@echo "$(BOLD)Torch backend$(RESET)"
	@$(PYTHON) -c "import torch; print('  torch:       ', torch.__version__); print('  cuda:        ', torch.cuda.is_available()); print('  mps:         ', getattr(torch.backends, 'mps', None) is not None and torch.backends.mps.is_available())" 2>/dev/null || echo "  (torch not installed — run 'make install')"

# ---- Test -------------------------------------------------------------------

.PHONY: test
test: ## Run all tests (unit + integration)
	$(PYTHON) -m pytest tests-unit tests -v

.PHONY: test-unit
test-unit: ## Run unit tests only
	$(PYTHON) -m pytest tests-unit -v

.PHONY: test-integration
test-integration: ## Run integration tests only
	$(PYTHON) -m pytest tests -v

# ---- Smoke test (end-to-end image generation) ------------------------------

.PHONY: smoke
smoke: ## Start server + run one image generation, then stop the server
	@if [ ! -f scripts/generate_one.py ]; then \
		echo "$(RED)scripts/generate_one.py not found$(RESET)" >&2; exit 1; \
	fi
	@if [ -z "$$(ls -A models/checkpoints 2>/dev/null | grep -v '^put_checkpoints_here$$')" ]; then \
		echo "$(YELLOW)No checkpoint found in models/checkpoints/$(RESET)" >&2; \
		echo "$(YELLOW)Place a .safetensors file there, or download SD 1.5:$(RESET)" >&2; \
		echo "  curl -L -o models/checkpoints/v1-5-pruned-emaonly.safetensors \\" >&2; \
		echo "    https://huggingface.co/stable-diffusion-v1-5/stable-diffusion-v1-5/resolve/main/v1-5-pruned-emaonly.safetensors" >&2; \
		exit 1; \
	fi
	@$(MAKE) --no-print-directory start
	@trap '$(MAKE) --no-print-directory stop >/dev/null 2>&1' EXIT; \
	$(MAKE) --no-print-directory _smoke-wait-and-run
	@$(MAKE) --no-print-directory stop >/dev/null 2>&1 || true
	@echo "$(GREEN)✓ smoke test complete — see output/$(RESET)"

.PHONY: _smoke-wait-and-run
_smoke-wait-and-run:
	@READY=0; \
	for i in $$(seq 1 90); do \
		if curl -sf http://127.0.0.1:8188/ >/dev/null 2>&1; then \
			echo "Server responsive ($$i s)"; \
			READY=1; \
			break; \
		fi; \
		sleep 1; \
	done; \
	if [ "$$READY" != "1" ]; then \
		echo "$(RED)Server failed to bind :8188 within 90 s$(RESET)" >&2; \
		tail -30 .run/comfyui.log >&2 || true; \
		exit 1; \
	fi
	@$(PYTHON) scripts/generate_one.py

# ---- Lint & Format ----------------------------------------------------------

# ruff is not in requirements.txt (dev-only) — install lazily if missing.
.PHONY: _ensure-ruff
_ensure-ruff:
	@$(PYTHON) -m ruff --version >/dev/null 2>&1 || \
		(echo "$(YELLOW)ruff not installed, installing...$(RESET)" && \
		 uv pip install --python $(PYTHON) ruff)

.PHONY: lint
lint: _ensure-ruff ## Run linter (ruff check)
	$(PYTHON) -m ruff check .

.PHONY: format
format: _ensure-ruff ## Auto-format code (ruff fix)
	$(PYTHON) -m ruff check --fix .
	$(PYTHON) -m ruff format .

.PHONY: format-check
format-check: _ensure-ruff ## Check formatting without changes
	$(PYTHON) -m ruff format --check .

# ---- Clean ------------------------------------------------------------------

.PHONY: clean
clean: ## Remove build artifacts and caches
	find . -type d -name __pycache__ -not -path './.venv/*' -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name '*.pyc' -not -path './.venv/*' -delete 2>/dev/null || true
	find . -type d -name '*.egg-info' -not -path './.venv/*' -exec rm -rf {} + 2>/dev/null || true
	rm -rf .pytest_cache .ruff_cache .run
