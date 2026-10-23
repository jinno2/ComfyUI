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
- Chosen: Fork-specific count is measured fresh as a402fd40^2..HEAD; latest value cached below, full series in claims.ndjson; SOT files stay snapshot-free (2026-10-23 restructure)
- Policy: recency + primary_measurement + bloat_control
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
- 2026-10-23T01:50:20Z (run_id clock, worktree @ 0e3380c5) `git rev-list --count a402fd40^2..HEAD` → 61; `git rev-list --count up/master..HEAD` → 556; `git rev-list --count HEAD..up/master` → 0 (upstream fully contained); up/master tip f6c162dd (2026-06-23, stale). Growth since prior anchor 60 @ f0a0a09f is the single loop commit 0e3380c5 (.concept sync)
- 2026-10-23T01:50Z run: SOT de-snapshot restructure per prior-run improvement feedback — dated per-run counts removed from ontology.yml (TERM-FORK), invariants.yml (INV-FORK-002) and ambiguities.yml (AMB-FORK-001); claims.ndjson and this cache are the only dated-value stores going forward
- Run reports are each run's final CYCLE_SUMMARY output; this section carries only the latest durable measurement trace (not a history log)
