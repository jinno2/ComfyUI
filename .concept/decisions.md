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
- Chosen: Fork-specific count is measured fresh as a402fd40^2..HEAD (33 on 2026-10-16); older figures (13, ~20) are historical snapshots
- Policy: recency + primary_measurement
- Expires After Runs: 20
- Linked: AMB-FORK-001 / CFLT-FORK-001 (resolved 2026-10-16)
- Revert Triggers: primary_evidence_contradiction
