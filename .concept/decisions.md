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

## AUTO:Q3.denominator:audited_extractable_subset
- Status: ACTIVE
- Chosen: Use the revalidated audited subset (185 of 188 test files encode repository-level constraints); keep evidence-backed invariants only.
- Policy: primary_evidence + budget_integrity
- Expires After Runs: 20
- Linked: AMB-Q3-001
- Revert Triggers: current test-file inventory differs from the audited inventory

## AUTO:Q3.coverage:report_observed
- Status: ACTIVE
- Chosen: Report the observed unique-file coverage as 1/185 (0.5%) and FAIL against the existing 50% threshold. Do not invent coverage or relax the threshold; the 60-invariant cap alone does not prove the target impossible.
- Policy: primary_evidence + budget_integrity
- Expires After Runs: 20
- Linked: AMB-Q3-002
- Revert Triggers: owner or metric specification defines a different Q3 aggregation rule

## Verification Log (cache: latest measurement per decision key)
- In-worktree observation at b9ce5171 `git rev-list --count a402fd40^2..HEAD` → 62; `git rev-list --count up/master..HEAD` → 557; `git rev-list --count HEAD..up/master` → 0 (upstream fully contained); up/master tip f6c162dd (2026-06-23, stale)
- Run reports are each run's final CYCLE_SUMMARY output; this section carries only the latest durable measurement trace (not a history log)
