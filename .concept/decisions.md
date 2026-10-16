# Active AUTO Decisions (cache) — safe to delete

## AUTO:Prompt.definition:graph_unit_by_prompt_id
- Status: ACTIVE
- Chosen: Prompt = グラフ全体を prompt_id で管理する実行単位
- Policy: industry_convention + reversibility
- Expires After Runs: 20
- Linked: AMB-PROMPT-001
- Revert Triggers: primary_evidence_contradiction, security_risk

## AUTO:Node.registration:hasattr_gate
- Status: ACTIVE
- Chosen: 動的ノード収集は hasattr(module, "NODE_CLASS_MAPPINGS") のみを正とする
- Policy: code_evidence
- Expires After Runs: 20
- Linked: INV-NODE-001
- Revert Triggers: primary_evidence_contradiction

## AUTO:LatentPreview.gc_watch
- Status: ACTIVE
- Chosen: LatentPreview は ontology に置かず term_queue (TP-000006) で様子見
- Policy: bloat_control (new-terms-via-queue rule)
- Expires After Runs: 10
- Linked: TP-000006
- Revert Triggers: primary_evidence_contradiction
