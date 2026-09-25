# Repository relations
Repository: ComfyUI

## 階層関係（エスカレーション経路）

- 親: business_operation_notes（jinno確定 2026-09-26）
- 根拠: 上流 Comfy-Org/ComfyUI の fork。上流比 515 コミット先行だが大半は upstream merge 分で fork 固有は 20 commits（Makefile 標準化・クロスプラットフォーム対応・Woodpecker gate＋upstream テスト workflow ガード・safe_linear per-device フォールバック・seedvr2 テスト修正・CODEBASE_ANALYSIS.md）。画像生成研究のため business_operation_notes 配下（出典: git log up/master..、fork 調査 2026-09-26）
- 出典: contracts registry `registry/organization/repositories/comfyui.yaml` の spec.parent（contracts commit ecbc226）。2026-09-26 の一括レビュー表 output/repo-parent-review-2026-09-26.md（ローカル output ディレクトリ）を jinno が現状案で承認。

- Observation: 以前の推定草案（jinno確定待ち）は 2026-09-26 の一括レビューで現状案のまま確定された。provider/consumer の検証済み関係はまだない。
