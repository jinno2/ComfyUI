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
- Chosen: Fork-specific count is measured fresh as a402fd40^2..HEAD (48 at c6904572 on 2026-10-22T20:18Z, in-worktree); older figures (13, ~20, 515-ahead) are dated historical snapshots
- Policy: recency + primary_measurement
- Expires After Runs: 20
- Linked: AMB-FORK-001 (resolved) / CFLT-FORK-001 (resolved 2026-10-16)
- Revert Triggers: primary_evidence_contradiction

## Verification Log (cache: latest measurement per decision key)
- 2026-10-22T20:18Z `git rev-list --count a402fd40^2..HEAD` → 48; `git rev-list --count up/master..HEAD` → 543; `git rev-list --count HEAD..up/master` → 0 (upstream fully contained); up/master tip f6c162dd (2026-06-23, stale)
- Measured in current worktree @ c6904572
- Run reports are each run's final CYCLE_SUMMARY output; this section carries only the latest durable measurement trace (not a history log)
