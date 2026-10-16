# Active AUTO Decisions (cache) — safe to delete

## AUTO:Prompt.definition:graph_unit_by_prompt_id
- Status: ACTIVE
- Chosen: Prompt = グラフ全体を prompt_id で管理する実行単位（実行時グラフ構造は DynamicPrompt）
- Policy: industry_convention + reversibility
- Expires After Runs: 20
- Linked: AMB-PROMPT-001 / TP-000001 (merged)
- Revert Triggers: primary_evidence_contradiction, security_risk

## AUTO:Node.registration:dual_path
- Status: ACTIVE
- Chosen: ノード収集は V1 (NODE_CLASS_MAPPINGS) と V3 (comfy_entrypoint → ComfyExtension.get_node_list) の二経路を正とする
- Policy: code_evidence
- Expires After Runs: 20
- Linked: CFLT-NODE-001 / INV-NODE-001
- Revert Triggers: primary_evidence_contradiction
