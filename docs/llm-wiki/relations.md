# Repository relations
Repository: comfyui

## business_operation_notes
- Status: confirmed
- Relationship: parent / escalation
- Responsibility: ComfyUI owns the local node-graph AI content engine and its fork changes; business_operation_notes owns cross-repository context and is the direct escalation parent.
- Canonical sources: contracts:registry/organization/repositories/comfyui.yaml; contracts:registry/principles/escalation-chain.yaml
- Change rule: resolve questions from this repository's wiki and canonical sources first, then escalate unresolved ownership questions to the parent.
- Evidence: contracts:registry/organization/repositories/comfyui.yaml sha256:13d83bcea7a49803dc1a3cdb1bce5fb0a30404c6ef1458bb834eb284ba2df618
- Evidence: ComfyUI:docs/llm-wiki/index.md sha256:9d0167be9fc74020d51022448e0adbbc34ec6507f035c1e86f8e3f0c2d7e5ad1
- Follow-up: [ ] business_operation_notes: its relations memo omits ComfyUI although the registry names it as the parent; add ComfyUI to the child list and complete when the entry has current evidence.

## Comfy-Org/ComfyUI
- Status: confirmed
- Relationship: source/copy
- Responsibility: Comfy-Org/ComfyUI owns the upstream project; this repository owns its local fork changes and compatibility with upstream.
- Canonical sources: contracts:registry/organization/repositories/comfyui.yaml; ComfyUI:README.md; ComfyUI:LOOP.md
- Change rule: on upstream synchronization, re-check the merge base and fork-specific count; do not push upstream.
- Evidence: contracts:registry/organization/repositories/comfyui.yaml sha256:13d83bcea7a49803dc1a3cdb1bce5fb0a30404c6ef1458bb834eb284ba2df618
- Evidence: ComfyUI:README.md sha256:224e65e44969e84401213f00765c69709b762a81566ef6123a26f495892d4797
- Observation: At c6904572 (2026-10-22T20:18Z), a402fd40^2..HEAD = 48 and local up/master..HEAD = 543; HEAD..up/master = 0. Local up/master f6c162dd is dated 2026-06-23 and stale, so this does not establish current upstream lag.

- Observation: No provider/consumer relationship with another repository is verified in the inspected imports, CLI calls, dependency declarations, generated artifacts, CI/configuration, or work rules.

## tas_autopilot
- Status: confirmed
- Relationship: operator / operated
- Responsibility: tas_autopilot operates this checkout's autonomous dispatch lane (post-dispatch PR creation and landing via gh CLI) and files control-plane inbox escalations for it; ComfyUI owns the node-graph AI content engine and its fork changes.
- Canonical sources: tas_autopilot:tas_autopilot/control_plane/post_dispatch.py; tas_autopilot:AUTOMATION.md
- Change rule: when tas_autopilot post-dispatch PR behavior changes, re-check auto_merge_blocked escalations filed for this repository's tas/auto/* branches and the gh default-repo resolution noted below.
- Evidence: tas_autopilot:tas_autopilot/control_plane/post_dispatch.py sha256:2fa168013ddd7a4fe7b8a3581d81d52c6d730a8f28410d2a5ae2a1215f15a7a4
- Observation: At tas_autopilot 3dfc7d0f (observed 2026-10-26), the pr create path pins --repo <origin slug> (:982) but the collision-recovery adoption query gh_list_open_pr (:229) does not; from this checkout gh 2.46.0 resolves the default repo to Comfy-Org/ComfyUI, so adoption misses open PRs on jinno2/ComfyUI and false auto_merge_blocked escalations recur (PR #46 case).
- Follow-up: [ ] tas_autopilot: pass the origin repo_slug into _adopt_existing_pr/gh_list_open_pr and add ["--repo", slug] to the pr list args, with a fork-parent regression test (upstream remote present); complete when the adoption query is repo-pinned and the regression test exists in tas_autopilot.
