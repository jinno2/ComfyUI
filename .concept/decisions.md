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
- Chosen: Latest recorded snapshot was measured as a402fd40^2..HEAD (54 at 65220ff8 on 2026-10-22T23:36Z); older figures are dated historical snapshots
- Policy: recency + primary_measurement
- Expires After Runs: 20
- Linked: AMB-FORK-001 (resolved) / CFLT-FORK-001 (resolved 2026-10-16)
- Revert Triggers: primary_evidence_contradiction

## AUTO:Q3.denominator:retain_evidence_only
- Status: ACTIVE
- Chosen: Keep only evidence-backed invariants; Q3 fails under the literal all-test-file proxy until an audited extractable-file denominator exists.
- Policy: primary_evidence + budget_integrity
- Expires After Runs: 20
- Linked: AMB-Q3-001
- Revert Triggers: audited extractable-file inventory changes the denominator

## Verification Log (cache: latest measurement per decision key)
- 2026-10-22T23:36Z `git rev-list --count a402fd40^2..HEAD` → 54; `git rev-list --count up/master..HEAD` → 549; `git rev-list --count HEAD..up/master` → 0 (upstream fully contained); up/master tip f6c162dd (2026-06-23, stale)
- Measured in worktree @ 65220ff8
- Run reports are each run's final CYCLE_SUMMARY output; this section carries only the latest durable measurement trace (not a history log)
