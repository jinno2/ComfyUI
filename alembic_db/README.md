## Generate new revision

1. Update the asset models in `app/assets/database/models.py` (`app/database/models.py` defines the shared `Base`).
2. Run `alembic revision --autogenerate -m "{your message}"`
