# Active AUTO Decisions (cache) — safe to delete

## AUTO:AssetPersistence.model_location:app_assets_database
- Status: ACTIVE
- Chosen: Asset ORM models live in app/assets/database/models.py (imports shared Base from app/database/models.py); app/database/models.py is shared Base + helper only. alembic_db/README.md step-1 pointer is stale.
- Policy: code_evidence + minimal_blast_radius
- Expires After Runs: 20
- Linked: CFLT-ASSETPERSIST-001
- Revert Triggers: primary_evidence_contradiction
