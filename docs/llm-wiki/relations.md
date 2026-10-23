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
