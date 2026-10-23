# LLM Wiki

長期圧縮コンテキスト。原則: contracts `llm-wiki-discipline`（手本: defuddle
`docs/llm-wiki/`）。正本を複製せず、検証済み知識を出典付きで圧縮する。

## Verified Knowledge

- モデルプレビューの検索はパス全体を `glob.escape` し、モデル名・格納先の `[]`・`?`・`*` を文字として扱う。対応画像と safetensors 内のカバー画像をHTTP応答の画素で確認し、既存のパス・symlink防御も検証。出典: [`get_model_previews`](../../app/model_manager.py)、[回帰テスト](../../tests-unit/app_test/model_manager_test.py)、[検証記録](log.md#2026-10-23--モデルプレビュー検索でglob特殊文字をリテラルに扱う)。`?`・`*` を含むファイルの実検証はLinux上（Windowsでは作成不可）。

- `safe_linear` の全 GPU 一括切替と「テストゼロ」という旧指摘は解消済み。現行のデバイス別状態・エラー解放先と6件の CPU・モック回帰テスト、実機検証の限界は [解析文書の2.2節](../CODEBASE_ANALYSIS.md#22-モデル管理サンプリング層) を参照（2026-10-23、コードとテストを照合）。

- 成果物: 上流 comfyanonymous/ComfyUI（モジュラー型 AI コンテンツ生成エンジン）のローカル fork/ワーキングコピー。README は上流本文のまま。（出典: README.md、上流 GitHub リポ表示）
- カスタマイズ: fork 固有コミット数は自律ループ作業で変わるため、現行値は `git rev-list --count a402fd40^2..HEAD` で都度計測する。履歴値は2026-09-26に20、2026-10-22T05:10Zに43、2026-10-22T20:18Zに48（同時点のローカル `up/master` は ahead 543 / lag 0）だった。`up/master` は f6c162dd（2026-06-23）の古い参照で、これらの比較は現在の upstream 状態を示さない。fork 固有の内容: Makefile 標準化とクロスプラットフォーム対応、Woodpecker gate 追加と upstream テスト workflow のガード、safe_linear のデバイス別フォールバック、seedvr2 テスト順依存修正、CODEBASE_ANALYSIS.md・AUTOMATION.md。（出典: git 計測 / 2026-09-26 fork カスタマイズ調査。計測時は `git rev-list --count a402fd40^2..HEAD`、`git rev-list --left-right --count origin/main...HEAD`、`git rev-list --count HEAD..up/master`、`git log -1 --format=%H up/master` を実行）

- Q3 test-inventory audit (2026-10-23 snapshot, before the API logger regression tests): a source qualifies when a `test_*` function/method contains `assert`, a unittest `assert*` call, `pytest.raises`, or `pytest.fail`. This syntactic rule includes helper/tooling tests that assert behavior; it measures extraction eligibility, not invariant coverage. All 188 Python test sources at that audit have a recorded file hash, test symbol, and expectation line(s). Only 1/188 files were referenced by invariants, below 50%. Later test additions are outside that snapshot. See [the per-file audit](test-constraint-inventory.ndjson) and `.concept/ontology_metrics.json`.
