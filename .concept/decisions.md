# Active AUTO Decisions (cache) — safe to delete

## AUTO:AssetPersistence.model_location:app_assets_database
- Status: ACTIVE (materialized 2026-10-12T15:17:55Z)
- Chosen: Asset ORM models live in app/assets/database/models.py (imports shared Base from app/database/models.py); app/database/models.py is shared Base + helper only. alembic_db/README.md step 1 and alembic_db/env.py now match this layout (CFLT-ASSETPERSIST-001 resolved).
- Policy: code_evidence + minimal_blast_radius
- Expires After Runs: 20
- Linked: CFLT-ASSETPERSIST-001
- Revert Triggers: primary_evidence_contradiction
