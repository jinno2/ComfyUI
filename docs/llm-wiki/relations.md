# Repository relations
Repository: ComfyUI

## 階層関係（エスカレーション経路）

- 親: business_operation_notes（jinno確定 2026-09-26）
- 根拠: 上流 Comfy-Org/ComfyUI の fork。上流比 515 コミット先行だが大半は upstream merge 分で fork 固有は 20 commits（Makefile 標準化・クロスプラットフォーム対応・Woodpecker gate＋upstream テスト workflow ガード・safe_linear per-device フォールバック・seedvr2 テスト修正・CODEBASE_ANALYSIS.md）。画像生成研究のため business_operation_notes 配下（出典: git log up/master..、fork 調査 2026-09-26）
- 出典: contracts registry `registry/organization/repositories/comfyui.yaml` の spec.parent（contracts commit ecbc226）。2026-09-26 の一括レビュー表 output/repo-parent-review-2026-09-26.md（ローカル output ディレクトリ）を jinno が現状案で承認。

- Observation: 以前の推定草案（jinno確定待ち）は 2026-09-26 の一括レビューで現状案のまま確定された。

## tas_autopilot

- Status: confirmed
- Relationship: operator/operated — tas_autopilot の control_plane/post_dispatch.py が本リポ共有チェックアウトの default branch コミットを `tas/auto/<sha>` ブランチに park し、origin（jinno2/ComfyUI）へ push、self-PR で main に着地させる。
- Responsibility: ComfyUI はエンジン本体と default branch を所有。tas_autopilot は fleet の push/PR/merge 自動化を所有。
- Canonical sources: tas_autopilot:tas_autopilot/control_plane/post_dispatch.py
- Change rule: origin の URL や fork 親（Comfy-Org/ComfyUI、default branch は master）が変わったら、`.git/config` の `remote.origin.gh-resolved` と post_dispatch の PR targeting を再確認する。
- Evidence: tas_autopilot:tas_autopilot/control_plane/post_dispatch.py sha256:873189e860c2b680b38c4e73eb1e8af19f57fb96a68ebc54babf2e6c35c5d9a3
- Observation: 2026-09-26 の push_failed 根本原因。`gh_create_pr`（post_dispatch.py:499）が `gh pr create` に `--repo` を渡さず、gh が fork 親 Comfy-Org/ComfyUI を base リポに解決。親には `main` も head ブランチも存在しないため GraphQL「Head sha can't be blank / No commits between main and tas/auto/...」が出る。push 自体は成功済み（origin/tas/auto/1d7cf85977ab、2026-09-26 07:37 push）。本 clone では `git config --local remote.origin.gh-resolved jinno2/ComfyUI`（`gh repo set-default` が書くキーと同一）で緩和済み。
- Observation: gh アカウント nobu007（user ID 8529529）は 2026-09-26 時点で GraphQL レート制限枯渇＋504。targeting 修正後も quota 回復まで PR 作成は失敗し続ける（リポ外の運用課題）。
- Follow-up: [ ] tas_autopilot — `gh_create_pr` が origin 由来の `--repo`（または GH_REPO）を渡すようにし、per-clone の `remote.origin.gh-resolved` なしでも self-PR が fork 宛になること。完了条件: `gh-resolved` 未設定の clone で tas/auto/* ブランチの PR が jinno2/ComfyUI 宛に作成される。
