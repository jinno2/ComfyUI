# Repository relations
Repository: comfyui

## business_operation_notes
- Status: confirmed
- Relationship: parent/child and escalation — this fork belongs under `business_operation_notes`, which owns cross-repository context and is the direct escalation parent. The registry’s `spec.parent` is authoritative; jinno approved the current arrangement in the 2026-09-26 parent review.
- Responsibility: `business_operation_notes` owns cross-repository ownership and hierarchy decisions. ComfyUI owns the local node-graph AI content engine and its fork-specific changes, including ongoing autonomous development without automatic upstream updates.
- Canonical sources: `contracts:registry/organization/repositories/comfyui.yaml` (`spec.parent`); `contracts:registry/principles/escalation-chain.yaml`; `ComfyUI:docs/llm-wiki/index.md`; `ComfyUI:AUTOMATION.md`
- Change rule: resolve questions from this repository’s wiki and canonical sources first, then escalate unresolved ownership questions to the parent. If `spec.parent` changes, update this section and re-hash the registry file, citing the contracts commit.
- Evidence: `contracts:registry/organization/repositories/comfyui.yaml` sha256:13d83bcea7a49803dc1a3cdb1bce5fb0a30404c6ef1458bb834eb284ba2df618
- Evidence: `ComfyUI:docs/llm-wiki/index.md` sha256:9d0167be9fc74020d51022448e0adbbc34ec6507f035c1e86f8e3f0c2d7e5ad1
- Follow-up: [ ] `business_operation_notes`: when the parent repository’s authoritative file is available locally, hash its actual bytes and record the peer file path and SHA-256 here. Complete when direct, hashed peer evidence is recorded.

## Comfy-Org/ComfyUI
- Status: confirmed
- Relationship: source/copy — this repository is a fork of upstream Comfy-Org/ComfyUI. Upstream is pinned (`upstreamPolicy: pinned-planned-upgrades`, `pinnedAt: 43f4f0b1c715bfee306a10f335e0c48567880e72`, per the contracts registry). Merge upstream only on the owner’s explicit instruction.
- Responsibility: upstream owns the source project. This fork owns its fork-specific changes and infrastructure, including Makefile standardization, cross-platform support, Woodpecker gates, and upstream workflow guards.
- Canonical sources: `ComfyUI:.git/config` (upstream remote); `contracts:registry/organization/repositories/comfyui.yaml` (`annotations.upstream`, `upstreamPolicy`, and `pinnedAt`); `ComfyUI:AUTOMATION.md`
- Change rule: if the upstream remote URL or registry pin changes, update this section and re-hash `.git/config` and the registry file. Import upstream only on the owner’s explicit instruction; when synchronizing, re-check the merge base and fork-specific commit count. Do not push upstream.
- Evidence: `ComfyUI:.git/config` sha256:076d5741a211211dae5b1d84af58e6607c1561ff4be5f9456a0d4c37f90cdf8a
- Evidence: `contracts:registry/organization/repositories/comfyui.yaml` sha256:13d83bcea7a49803dc1a3cdb1bce5fb0a30404c6ef1458bb834eb284ba2df618
- Observation: At c6904572 (2026-10-22T20:18Z), `a402fd40^2..HEAD` = 48 and local `up/master..HEAD` = 543; `HEAD..up/master` = 0. Local `up/master` f6c162dd is dated 2026-06-23 and stale, so this does not establish current upstream lag.
- Observation: The 2026-09-26 fork investigation found the fork 515 commits ahead of upstream, mostly from upstream merges, with about 20 fork-specific commits. Re-measure after fetching upstream with `git log upstream/master..`.
- Observation: No provider/consumer relationship with another repository is verified in the inspected imports, CLI calls, dependency declarations, generated artifacts, CI/configuration, or work rules. The 2026-09-26 parent review also confirmed that no such relationship had been verified.
