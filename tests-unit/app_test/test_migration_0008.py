import sqlite3
from datetime import datetime, timedelta

from alembic import command
from alembic.config import Config

from app.assets.helpers import get_utc_now


def test_existing_missing_rows_get_a_new_retention_window(tmp_path):
    db_path = tmp_path / "assets.db"
    config = Config("alembic.ini")
    config.set_main_option("script_location", "alembic_db")
    config.set_main_option("sqlalchemy.url", f"sqlite:///{db_path}")
    command.upgrade(config, "0007_record_content_split")

    with sqlite3.connect(db_path) as connection:
        connection.execute(
            "INSERT INTO asset_contents (id, path, size_bytes, is_missing, created_at) "
            "VALUES (?, ?, ?, ?, ?)",
            ("old", "/tmp/old", 1, 1, "2020-01-01 00:00:00"),
        )

    command.upgrade(config, "head")
    with sqlite3.connect(db_path) as connection:
        missing_at = connection.execute(
            "SELECT missing_at FROM asset_contents WHERE id = 'old'"
        ).fetchone()[0]

    assert datetime.fromisoformat(missing_at) > get_utc_now() - timedelta(minutes=5)
