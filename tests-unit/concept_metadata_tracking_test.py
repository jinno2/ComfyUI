"""Tests for the .concept metadata tracking policy."""

import shutil
import subprocess
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]

CONCEPT_SEEDS = (
    "charter.yml",
    "autopilot.yml",
    "ontology_budget.yml",
)
CONCEPT_RUNTIME = (
    "ambiguities.yml",
    "archive/ontology.snapshots/ontology.yml",
    "claims.ndjson",
    "conflicts.yml",
    "decisions.md",
    "invariants.yml",
    "mappings.yml",
    "ontology.yml",
    "ontology_metrics.json",
    "run_state.json",
    "term_queue.yml",
    "tombstones.yml",
)


def _git(*args):
    return subprocess.run(
        ["git", *args], cwd=REPO_ROOT, capture_output=True, text=True
    )


pytestmark = [
    pytest.mark.skipif(shutil.which("git") is None, reason="git not available"),
    pytest.mark.skipif(
        _git("rev-parse", "--is-inside-work-tree").returncode != 0,
        reason="not a git checkout",
    ),
]


@pytest.mark.parametrize("name", CONCEPT_RUNTIME)
def test_runtime_metadata_is_ignored(name):
    assert _git("check-ignore", "-q", f".concept/{name}").returncode == 0


@pytest.mark.parametrize("name", CONCEPT_SEEDS)
def test_seed_metadata_is_tracked_and_not_ignored(name):
    assert _git("ls-files", "--error-unmatch", f".concept/{name}").returncode == 0
    assert _git("check-ignore", "-q", f".concept/{name}").returncode != 0
