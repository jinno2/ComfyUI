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
- Chosen: Fork-specific count is measured fresh as a402fd40^2..HEAD (43 at 2026-10-22T05:10Z, in-worktree); older figures (13, ~20, 515-ahead) are dated historical snapshots
- Policy: recency + primary_measurement
- Expires After Runs: 20
- Linked: AMB-FORK-001 (resolved) / CFLT-FORK-001 (resolved 2026-10-16)
- Revert Triggers: primary_evidence_contradiction

## Verification Log (cache: latest measurement per decision key)
- 2026-10-22T05:10Z `git rev-list --count a402fd40^2..HEAD` → 43; `git rev-list --count up/master..HEAD` → 538; `git rev-list --count HEAD..up/master` → 0 (upstream fully contained); up/master tip f6c162dd (2026-06-23, stale); `git rev-list --left-right --count origin/main...HEAD` → 22/12
- Measured in worktree /home/jinno/ComfyUI-aihub-20261022-050533-040919 @ efad1d1b, branch ai/ComfyUI/instruction-20261022-050533-040919
- Run reports are each run's final CYCLE_SUMMARY output; this section carries only the latest durable measurement trace (not a history log)
