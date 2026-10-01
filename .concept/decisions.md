# Active AUTO Decisions (cache) — safe to delete

## AUTO:ExecutionGraph.responsibility:execution_py_orchestrates_graph_holds_data
- Status: ACTIVE
- Chosen: execution.py が検証・キャッシュ・結果生成を担い、comfy_execution/graph.py が DynamicPrompt/ExecutionList 等のグラフ構造を提供
- Policy: verified_evidence
- Expires After Runs: 20
- Linked: AMB-EXEC-001
- Revert Triggers: primary_evidence_contradiction

## AUTO:ModelPatcher.definition:sd_loader_wraps_model_in_patcher
- Status: ACTIVE
- Chosen: load_diffusion_model 系は BaseModel を ModelPatcher に包んで返す。ModelPatcher が呼び出し側の操作単位
- Policy: verified_evidence
- Expires After Runs: 20
- Linked: AMB-TERM-001
- Revert Triggers: primary_evidence_contradiction

## AUTO:ontology.layer_assignment:engine_pillars_core
- Status: ACTIVE
- Chosen: ExecutionGraph/ModelPatcher/ModelManagement を core、Sampler/LatentFormat/PromptServer/QuantOps を domain に採用（AGENTS.md の境界規定 + CODEBASE_ANALYSIS.md#L65 の権威記述に基づく）
- Policy: spec_alignment
- Expires After Runs: 20
- Linked: TP-000001..TP-000007
- Revert Triggers: primary_evidence_contradiction

## AUTO:ontology.layer_assignment:infrastructure_terms_domain
- Status: ACTIVE
- Chosen: CoreComfyUI (TP-000008) / AttentionBackend (TP-000009) を domain に採用。core は実行・パッチ・デバイスメモリの 3 権威に留置（AGENTS.md 権威記述 + 実コード確認: nodes.py#L2349, comfy/ldm/modules/attention.py#L891-L904, comfy/ops.py#L68-L96）
- Policy: spec_alignment + conservative_layering
- Expires After Runs: 20
- Linked: TP-000008, TP-000009
- Revert Triggers: primary_evidence_contradiction
