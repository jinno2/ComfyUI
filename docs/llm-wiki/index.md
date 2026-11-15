# LLM Wiki

長期圧縮コンテキスト。原則: contracts `llm-wiki-discipline`（手本: defuddle
`docs/llm-wiki/`）。正本を複製せず、検証済み知識を出典付きで圧縮する。

## Verified Knowledge

- 成果物: 上流 comfyanonymous/ComfyUI（モジュラー型 AI コンテンツ生成エンジン）のローカル fork/ワーキングコピー。README は上流本文のまま。（出典: README.md、上流 GitHub リポ表示）
- カスタマイズ: fork 固有は約 20 commits（jinno author 実測）。Makefile 標準化とクロスプラットフォーム対応、Woodpecker gate 追加と upstream テスト workflow のガード、safe_linear のデバイス別フォールバック、seedvr2 テスト順依存修正、CODEBASE_ANALYSIS.md・AUTOMATION.md。先行 515 の大半は upstream merge による上流新規分。（出典: git log up/master..HEAD 515 commits / a402fd40^2..HEAD = 20 commits）
- 計画スパイン: 長期方針の見直し・約30分の実行波・Dot 向けワーカー指示書は `docs/plan/`（long-term-direction.md / milestones.md / dot-worker.md）。ゴールの正本は charter のまま、見直し記録と実行波のみを保持。（出典: docs/plan/、2026-10-21 @ 4c0788db 観測）
- 実行用マイルストーン索引: `docs/MILESTONES.md` が charter の MS-001..MS-003 を Outcome / Acceptance / Evidence / Status・依存・次の一手の形で実行可能な分解として持ち、正本 `REPO_METADATA.json` は charter と `docs/plan/milestones.md` の投影（source_hash は git blob ID）。charter MS-003 の deliverables は 2026-11-03 に追跡3ファイル構成へ修正。（出典: docs/MILESTONES.md、.concept/charter.yml、REPO_METADATA.json、2026-11-03 観測）
- WP-A1 受入証拠: alembic 連鎖 0001..0008 は空の一時 SQLite DB に exit 0 で全適用され、単一 head `0008_missing_content_age` に一致（隔離 ini、`user/comfyui.db` 不使用）。証跡は `docs/plan/evidence/wp-a1-alembic-chain.md`。旧 run 20261107-233514-229391 の証拠窓欠損（authorized_observation は構造的に検証不能）に対する recovery で永続化。（出典: docs/plan/evidence/wp-a1-alembic-chain.md、run 20261107-235007-331852 実測）
