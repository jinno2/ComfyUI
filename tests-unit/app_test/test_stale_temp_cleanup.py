"""Stale temp cleanup keeps an unattended long-running server from filling its disk."""

import os
import time

import folder_paths
from app.assets.lifecycle import cleanup_stale_temp_files


def test_cleanup_stale_temp_files(tmp_path, monkeypatch):
    monkeypatch.setattr(folder_paths, "temp_directory", str(tmp_path))
    old_time = time.time() - 48 * 60 * 60

    old = tmp_path / "old.png"
    old.write_bytes(b"x")
    os.utime(old, (old_time, old_time))
    fresh = tmp_path / "fresh.png"
    fresh.write_bytes(b"y")

    emptied = tmp_path / "emptied"
    emptied.mkdir()
    old_in_dir = emptied / "old.png"
    old_in_dir.write_bytes(b"x")
    os.utime(old_in_dir, (old_time, old_time))

    kept = tmp_path / "kept"
    kept.mkdir()
    fresh_in_dir = kept / "fresh.png"
    fresh_in_dir.write_bytes(b"y")

    removed = cleanup_stale_temp_files(max_age_seconds=24 * 60 * 60)

    assert removed == 2
    assert not old.exists()
    assert not emptied.exists()
    assert fresh.exists()
    assert kept.exists() and fresh_in_dir.exists()


def test_cleanup_stale_temp_files_missing_dir(tmp_path, monkeypatch):
    monkeypatch.setattr(folder_paths, "temp_directory", str(tmp_path / "nope"))
    assert cleanup_stale_temp_files() == 0
