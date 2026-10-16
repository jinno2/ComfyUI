# Active AUTO Decisions (cache) — safe to delete

## AUTO:UnitTestGate.scope:unit_only
- Status: ACTIVE
- Chosen: Commit gate = `make test` (pytest tests-unit) only; integration tests/ optional per run
- Policy: primary_text_authority + reversibility
- Expires After Runs: 20
- Linked: AMB-UNIT-001
- Revert Triggers: primary_evidence_contradiction

## AUTO:ForkUpstreamSync.count:git_recency
- Status: ACTIVE
- Chosen: Current fork-specific count = ~20 (git log, 2026-09-26); 13 is a historical 2026-09-20 snapshot
- Policy: recency + primary_measurement
- Expires After Runs: 20
- Linked: AMB-FORK-001 / CFLT-FORK-001
- Revert Triggers: primary_evidence_contradiction
