"""Runs the asset system's startup and shutdown maintenance: clearing temp rows
and files, recording a hash-mode transition, and handing the filesystem scan to
the background seeder. Startup only enqueues transition work — draining it
belongs to the seeder, so a large library cannot stall the server before it
accepts requests. It also settles, before any of that, whether the database
dependencies exist at all, disabling the asset routes when they do not.
"""

from __future__ import annotations

import logging
import os
import shutil
import time
from datetime import timedelta

import folder_paths
from sqlalchemy import delete, select, update

from app.assets.database.models import Asset, AssetContent, AssetMeta, AssetTag
from app.assets.database.queries.records import delete_record
from app.assets.helpers import get_utc_now, sql_path_under_prefix
from app.assets.services.hash_mode_state import enqueue_transition_work
from app.assets.services.hash_mode_state import record_transition_intent
from app.database.db import can_create_session, create_session
from comfy.cli_args import args

_excluded_scan_roots: set[str] = set()
_hash_mode_transition: str | None = None


def get_excluded_scan_roots() -> frozenset[str]:
    return frozenset(_excluded_scan_roots)


def record_hash_mode_transition_intent() -> None:
    global _hash_mode_transition

    with create_session() as session:
        _hash_mode_transition = record_transition_intent(session)
        session.commit()


def enqueue_mode_transition_work() -> None:
    with create_session() as session:
        enqueue_transition_work(session, _hash_mode_transition)
        session.commit()


def wipe_temp_db_rows(session) -> tuple[int, int]:
    try:
        temp_root = os.path.abspath(folder_paths.get_temp_directory())
    except OSError:
        return 0, 0
    # These rows are hard-deleted, so the predicate must stay case-SENSITIVE: admitting a
    # case-different persistent directory destroys user assets.
    under_temp = sql_path_under_prefix(AssetContent.path, temp_root)

    temp_record_ids = list(
        session.scalars(
            select(Asset.id)
            .join(AssetContent, Asset.content_id == AssetContent.id)
            .where(under_temp)
        )
    )

    records_deleted = 0
    for record_id in temp_record_ids:
        delete_record(session, record_id)
        records_deleted += 1

    contents_deleted = 0
    for content in session.scalars(select(AssetContent).where(under_temp)).all():
        session.delete(content)
        contents_deleted += 1

    session.flush()
    return records_deleted, contents_deleted


def cleanup_temp_filesystem() -> bool:
    temp_dir = os.path.abspath(folder_paths.get_temp_directory())
    if not os.path.exists(temp_dir):
        return True
    try:
        shutil.rmtree(temp_dir)
        return True
    except OSError as exc:
        logging.warning(
            "Failed to remove temp directory %s: %s — excluding from scan for this process",
            temp_dir,
            exc,
        )
        _excluded_scan_roots.add(temp_dir)
        return False


STALE_TEMP_MAX_AGE = 24 * 60 * 60
MISSING_CONTENT_MAX_AGE = timedelta(days=30)


def purge_stale_missing_contents(session) -> int:
    cutoff = get_utc_now() - MISSING_CONTENT_MAX_AGE
    stale_content_ids = select(AssetContent.id).where(
        AssetContent.is_missing.is_(True), AssetContent.missing_at < cutoff
    )
    if session.scalar(stale_content_ids.limit(1)) is None:
        return 0
    stale_record_ids = select(Asset.id).where(Asset.content_id.in_(stale_content_ids))
    session.execute(update(Asset).where(Asset.preview_id.in_(stale_record_ids)).values(preview_id=None))
    session.execute(delete(AssetMeta).where(AssetMeta.asset_id.in_(stale_record_ids)))
    session.execute(delete(AssetTag).where(AssetTag.asset_id.in_(stale_record_ids)))
    session.execute(delete(Asset).where(Asset.id.in_(stale_record_ids)))
    result = session.execute(delete(AssetContent).where(AssetContent.id.in_(stale_content_ids)))
    return result.rowcount


def purge_stale_missing_contents_safely() -> None:
    try:
        with create_session() as session:
            purge_stale_missing_contents(session)
            session.commit()
    except Exception:
        logging.exception("Stale missing asset cleanup failed")


def cleanup_stale_temp_files(max_age_seconds: float = STALE_TEMP_MAX_AGE) -> int:
    """Delete temp files older than max_age_seconds and prune the dirs they empty.

    Temp is ephemeral by contract — a restart wipes it outright — so nothing may
    rely on it surviving, while files in use are always freshly written and never
    candidates. Keeps an unattended long-running server from filling its disk.
    """
    temp_dir = os.path.abspath(folder_paths.get_temp_directory())
    if not os.path.isdir(temp_dir):
        return 0
    deadline = time.time() - max_age_seconds
    removed = 0
    for root, dirs, files in os.walk(temp_dir, topdown=False):
        for name in files:
            path = os.path.join(root, name)
            try:
                if os.stat(path).st_mtime < deadline:
                    os.unlink(path)
                    removed += 1
            except OSError:
                pass
        for name in dirs:
            try:
                os.rmdir(os.path.join(root, name))
            except OSError:
                pass
    return removed


def start_asset_seeder() -> bool:
    from app.assets.seeder import asset_seeder

    started = asset_seeder.start(
        roots=("models", "input", "output"),
        prune_first=True,
        compute_hashes=args.enable_asset_hashing,
    )
    if started:
        logging.info("Background asset scan initiated for models, input, output")
    return started


def run_asset_startup() -> None:
    try:
        with create_session() as session:
            wipe_temp_db_rows(session)
            session.commit()
    except Exception:
        logging.exception("Temp DB row wipe failed; skipping filesystem cleanup")
        enqueue_mode_transition_work()
        start_asset_seeder()
        return
    cleanup_temp_filesystem()
    enqueue_mode_transition_work()
    start_asset_seeder()


def run_startup(*, enable_assets: bool) -> None:
    try:
        if enable_assets:
            run_asset_startup()
        else:
            cleanup_temp_filesystem()
    except Exception:
        logging.exception("Asset startup maintenance failed")


def run_asset_shutdown_cleanup() -> None:
    try:
        with create_session() as session:
            wipe_temp_db_rows(session)
            session.commit()
    except Exception:
        logging.exception("Temp DB row wipe failed during shutdown")
    finally:
        cleanup_temp_filesystem()


def run_shutdown() -> None:
    try:
        if can_create_session():
            run_asset_shutdown_cleanup()
        else:
            cleanup_temp_filesystem()
    except Exception:
        logging.exception("Asset shutdown cleanup failed")
