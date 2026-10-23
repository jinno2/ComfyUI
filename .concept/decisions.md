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
- Chosen: Latest recorded snapshot was measured as a402fd40^2..HEAD (57 at 40a7bdef on 2026-10-23T00:39:24Z, inside the recording run); older figures are dated historical snapshots
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
- 2026-10-23T00:39:24Z (run_id clock) `git rev-list --count a402fd40^2..HEAD` → 57; `git rev-list --count up/master..HEAD` → 552; `git rev-list --count HEAD..up/master` → 0 (upstream fully contained); up/master tip f6c162dd (2026-06-23, stale)
- Measured in worktree @ 40a7bdef, inside the run that recorded it (provenance fix for the prior-run 40-minute measurement/run_id lead)
- Re-canonicalization: UNMAPPED claims 10/11/24 superseded by new ComfyUI-boundary claims (same run); claim 63 (evidence-fidelity audit) intentionally stays UNMAPPED — ledger-maintenance facts belong to no domain concept
- 2026-10-23T00:47Z `make test VENV_BIN=/home/jinno/ComfyUI/.venv/bin` → exit 0, wall 7m12s (in-worktree @ 40a7bdef; worktree has no .venv, main checkout venv borrowed)
- Run reports are each run's final CYCLE_SUMMARY output; this section carries only the latest durable measurement trace (not a history log)
