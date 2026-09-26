# Repository relations
Repository: ComfyUI

## 階層関係（エスカレーション経路）

- 親: business_operation_notes（jinno確定 2026-09-26）
- 根拠: 上流 Comfy-Org/ComfyUI の fork。上流比 515 コミット先行だが大半は upstream merge 分で fork 固有は 20 commits（Makefile 標準化・クロスプラットフォーム対応・Woodpecker gate＋upstream テスト workflow ガード・safe_linear per-device フォールバック・seedvr2 テスト修正・CODEBASE_ANALYSIS.md）。画像生成研究のため business_operation_notes 配下（出典: git log up/master..、fork 調査 2026-09-26）
- 出典: contracts registry `registry/organization/repositories/comfyui.yaml` の spec.parent（contracts commit ecbc226）。2026-09-26 の一括レビュー表 output/repo-parent-review-2026-09-26.md（ローカル output ディレクトリ）を jinno が現状案で承認。

- Observation: 以前の推定草案（jinno確定待ち）は 2026-09-26 の一括レビューで現状案のまま確定された。provider/consumer の検証済み関係はまだない。

## Comfy-Org/ComfyUI（上流）と comfy-cla

- Status: confirmed
- Relationship: source/copy — 本リポは上流の fork で、CLA 署名の集約先 comfy-org/comfy-cla は上流組織が管理する外部リポ
- Responsibility: cla-assistant チェック（.github/workflows/cla.yml）は署名書き込みに `PERSONAL_ACCESS_TOKEN`（comfy-org/comfy-cla 書き込み用 PAT）を要する。fork に当該 secret も集約リポへの書き込み権限も無く、チェックは fork 上で絶対に成功しない。job を upstream 限定ガード（`if: github.repository == 'Comfy-Org/ComfyUI'`、test-unit.yml 等と同一パターン）で skip させる
- Canonical sources: ComfyUI:.github/workflows/cla.yml
- Change rule: cla.yml の署名先（remote-organization-name / remote-repository-name）や secret 構成が変わったら本観察を見直す
- Evidence: ComfyUI:.github/workflows/cla.yml sha256:4bf787c98d90a2ba8c0dcdabad3263feadac6bb5e39e7ae5fb04486c353ecc7b
- Observation: 期待される CI 結果は fork 上 PR で cla-assistant job が skipped (neutral) になること。本 run では push しないため実機検証は未済
- Follow-up: [ ] ComfyUI, 次回 fork 上 PR の CI 実行で cla-assistant が skipped になることを確認（cla.yml ガード追加後の初回実行時に完了条件）
