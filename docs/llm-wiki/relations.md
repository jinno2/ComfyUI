# Repository relations
Repository: ComfyUI

## business_operation_notes
- Status: confirmed
- Relationship: parent/child — 本forkは business_operation_notes 配下に属する（エスカレーションの親）。配置は contracts registry の spec.parent で確定し、2026-09-26 の一括親レビューを jinno が現状案で承認した。
- Responsibility: business_operation_notes が配下リポジトリの所有・階層判断を持つ。ComfyUI は fork 自体の恒久自律開発（上流自動追従なし）を持つ。
- Canonical sources: contracts:registry/organization/repositories/comfyui.yaml (spec.parent), ComfyUI:AUTOMATION.md
- Change rule: contracts の registry/organization/repositories/comfyui.yaml の spec.parent が変わったら本セクションを更新し registry ファイルを再ハッシュする（contracts commit を出典に付す）。
- Evidence: contracts:registry/organization/repositories/comfyui.yaml sha256:13d83bcea7a49803dc1a3cdb1bce5fb0a30404c6ef1458bb834eb284ba2df618
- Follow-up: [ ] business_operation_notes, 親リポの正本ファイルが手元に存在したら（新規checkout・配置変更など）, peer 側の実バイトから sha256 を取得して direct な peer 証拠を追記する, 完了条件: ハッシュ済み peer ファイルパスを本メモに記録

## Comfy-Org/ComfyUI
- Status: confirmed
- Relationship: source/copy — 本リポは upstream Comfy-Org/ComfyUI の fork。upstream は pinned（upstreamPolicy: pinned-planned-upgrades, pinnedAt 43f4f0b1c715bfee306a10f335e0c48567880e72, 出典: contracts registry）。merge は所有者の明示指示時のみ（AUTOMATION.md Driver）。
- Responsibility: upstream が元コードベースを持つ。本forkが fork 固有基盤（Makefile 標準化・クロスプラットフォーム対応・Woodpecker gate と upstream workflow ガード等）を持つ。
- Canonical sources: ComfyUI:.git/config (remote upstream), contracts:registry/organization/repositories/comfyui.yaml (annotations.upstream / upstreamPolicy / pinnedAt), ComfyUI:AUTOMATION.md
- Change rule: upstream remote URL または contracts の pin が変わったら本セクションを更新し .git/config と registry ファイルを再ハッシュする。upstream の取り込みは所有者の明示指示時に限る。
- Evidence: ComfyUI:.git/config sha256:076d5741a211211dae5b1d84af58e6607c1561ff4be5f9456a0d4c37f90cdf8a
- Evidence: contracts:registry/organization/repositories/comfyui.yaml sha256:13d83bcea7a49803dc1a3cdb1bce5fb0a30404c6ef1458bb834eb284ba2df618

- Observation: 2026-09-26 の fork 調査時点で上流比 515 コミット先行（大半は upstream merge 分、fork 固有は約 20 commits）。再計測は upstream fetch 後に `git log upstream/master..` で行う。
- Observation: 以前の推定草案（jinno確定待ち）は 2026-09-26 の一括レビューで現状案のまま確定された。provider/consumer の検証済み関係はまだない。
