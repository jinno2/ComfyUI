# Active AUTO Decisions (cache) — safe to delete

## AUTO:ExecutionOrchestration.boundary:prompt_id_is_execution_state
- Status: ACTIVE
- Chosen: prompt_id is execution-relevant queue identity (progress reset, execution events, cache invalidation); AGENTS.md's id exclusion refers to frontend workflow document ids
- Policy: reversibility + blast_radius_minimization
- Expires After Runs: 20
- Linked: AMB-EXEC-001 / CFLT-EXEC-001
- Revert Triggers: primary_evidence_contradiction, owner_decision_conflict on the AGENTS.md execution boundary, regression in execution event consumers
