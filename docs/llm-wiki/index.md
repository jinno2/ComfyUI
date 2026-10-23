# LLM Wiki

長期圧縮コンテキスト。原則: contracts `llm-wiki-discipline`（手本: defuddle
`docs/llm-wiki/`）。正本を複製せず、検証済み知識を出典付きで圧縮する。

## Verified Knowledge

- `safe_linear` の全 GPU 一括切替と「テストゼロ」という旧指摘は解消済み。現行のデバイス別状態・エラー解放先と6件の CPU・モック回帰テスト、実機検証の限界は [解析文書の2.2節](../CODEBASE_ANALYSIS.md#22-モデル管理サンプリング層) を参照（2026-10-23、コードとテストを照合）。

- 成果物: 上流 comfyanonymous/ComfyUI（モジュラー型 AI コンテンツ生成エンジン）のローカル fork/ワーキングコピー。README は上流本文のまま。（出典: README.md、上流 GitHub リポ表示）
- カスタマイズ: fork 固有コミット数は自律ループの作業で増え続けるため、現行値は `git rev-list --count a402fd40^2..HEAD` で都度計測する（2026-09-26 観測 20、2026-10-22T05:10Z 観測 43、2026-10-22T20:18Z 観測 48）。2026-10-22T20:18Z のローカル `up/master`（f6c162dd、2026-06-23）比較は ahead 543、lag 0。この ref は stale で upstream の最新状態を示さない。fork 固有の内容: Makefile 標準化とクロスプラットフォーム対応、Woodpecker gate 追加と upstream テスト workflow のガード、safe_linear のデバイス別フォールバック、seedvr2 テスト順依存修正、CODEBASE_ANALYSIS.md・AUTOMATION.md。（出典: git a402fd40^2..HEAD 計測 / 2026-09-26 fork カスタマイズ調査）

- Q3 test-inventory audit: a source qualifies when a `test_*` function/method contains `assert`, a unittest `assert*` call, `pytest.raises`, or `pytest.fail`. This syntactic rule includes helper/tooling tests that assert behavior; it measures extraction eligibility, not invariant coverage. All 188 current Python test sources have a recorded file hash, test symbol, and expectation line(s). Only 1/188 files are referenced by invariants, so Q3 remains below 50%. See [the per-file audit](test-constraint-inventory.ndjson) and `.concept/ontology_metrics.json`.
