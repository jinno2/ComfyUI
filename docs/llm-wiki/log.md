# GoalDev Log

永続的決定と完了記録を追記する。各エントリに日付と検証を必ず付ける
（原則: contracts `llm-wiki-discipline` の log-is-append-with-correction）。

## 2026-09-26 — llm-wiki スキャフォールド

contracts の llm-wiki-discipline 原則に基づき `docs/llm-wiki/` を新設した。

- **Verification**: 原則 `registry/principles/llm-wiki-discipline.yaml`（contracts リポ commit 3ab5768）。

## 2026-09-26 — fork カスタマイズ調査（upstream Comfy-Org/ComfyUI）

参照のある upstream リモートは `up`（upstream リモートは未 fetch で参照なし）のため `up/master` と比較。先行 515 件の大半は a402fd40 の upstream merge による上流新規分で、fork 固有は a402fd40^2..HEAD の 20 commits（jinno author 18 件）。内容: Makefile 標準化・クロスプラットフォーム対応（dev/test/lint/service、launchd 例、WAI-ANIMA セットアップ）、Woodpecker gate 追加と upstream テスト workflow のガード、safe_linear matmul の per-device フォールバック、seedvr2 テストの順依存修正、CODEBASE_ANALYSIS.md / AUTOMATION.md、ブランチ名 master→main 変更。

- **Verification**: git log up/master..HEAD = 515 commits（うち a402fd40^2..HEAD = 20 commits が fork 固有）、jinno author = 18 commits, diff --stat 654 files +174245/-20123。

## 2026-09-26 — 親の確定（jinno確定）
- relations.md の階層関係を草案から確定版へ更新。親: business_operation_notes。
- Verification: contracts registry `organization/repositories/comfyui.yaml` の spec.parent（ecbc226）と突合し一致を確認。

## 2026-10-22 — fork 固有コミット数の pointer 化（Dot D1-2）

docs/CODEBASE_ANALYSIS.md と本 wiki index の fork 数値（13 件 / 約 20 commits・先行 515）を観測日付きの履歴値として明記し、現行値への pointer（`git rev-list --count a402fd40^2..HEAD`）を追記した。値の唯一の所在は git 計測で、文書側は pointer に留める（charter MET-002・CFLT-FORK-001 解決方針に整合）。

- **Verification**: 2026-10-22T05:10Z、worktree efad1d1b で計測: `git rev-list --count a402fd40^2..HEAD` = 43、`up/master..HEAD` = 538、`HEAD..up/master` = 0（up/master f6c162dd 2026-06-23 は merge a402fd40 で完全包含）、`origin/main...HEAD` = 22/12。

## 2026-10-22 — fork 状態の再計測

fork 固有コミット数とローカル upstream ref との差分を最新 HEAD で再計測し、`.concept/` と wiki index の履歴値を更新した。`up/master` は 2026-06-23 の stale ref のため、この ahead 数は upstream の最新状態を表さない。

- **Verification**: 2026-10-22T20:18Z、worktree c6904572 で計測: `git rev-list --count a402fd40^2..HEAD` = 48、`up/master..HEAD` = 543、`HEAD..up/master` = 0（ローカル `up/master` f6c162dd、2026-06-23）。


## 2026-10-23 — Q3 test-inventory evidence audit

Moved the per-file test audit out of `.concept/`, whose schema is a fixed 14-file set, and replaced category-only classifications with a testable eligibility rule. A Python source qualifies when a `test_*` function or method contains `assert`, a unittest `assert*` call, `pytest.raises`, or `pytest.fail`; each of the 188 rows records the source SHA-256, matching test symbol, and exact expectation line(s). This establishes extraction eligibility, not that the invariant has already been captured. The prior 185/188 split excluded three tests without support under that criterion, so Q3 now uses all 188 files. Existing invariant evidence still covers one unique file (1/188, 0.53%); Q3 remains below its 50% target.

- **Verification**: Exact path-set, per-file AST expectation, line and SHA-256 checks passed (188/188); all `.concept` YAML, JSON and JSONL parsed, and its 14 files match the fixed schema. `git diff --check` passed. `rtk test make test VENV_BIN=/home/jinno/ComfyUI/.venv/bin` exited 0; RTK retained only the last five log lines, so this run's output did not include a pytest count.

## 2026-10-23 — concept snapshot cleanup

Removed dated fork-count samples from ontology, invariant, ambiguity, and resolved-conflict SOT records. Historical measurements remain in the append-only claims ledger; the latest observation stays in the decisions cache. Q3 remains 1/188 and FAIL under its active decision; no threshold or coverage claim was changed.

- **Verification**: At HEAD `984d68f4`, `a402fd40^2..HEAD` = 64, `up/master..HEAD` = 559, `HEAD..up/master` = 0. All `.concept` YAML, JSON, and JSONL parsed; 14 `.concept` files remain; budget counts are within limits; `git diff --check` passed. `make test` was interrupted after 20m20s (exit 130), with no pytest summary; no pass/fail result is claimed.

## 2026-10-23 — safe_linear 解析の現行実装への訂正

Task: `tas-task-508bebb6a4041f01ead1897a53705607288280ee17b06e7176056628f0451d5e`。
修正対象は `docs/CODEBASE_ANALYSIS.md` の safe_linear 記述のみ。旧来の全 GPU 一括切替・解放先未指定・テスト不在の指摘を、現行コードと既存回帰テストに基づいて訂正した。要約表、H5、M6、戦略的注記、検証表にも訂正を適用し、無関係な指摘は再確認済みと扱わない。ランタイムコードは変更していない。リポ間の関係・責務は変わらないため relations.md は更新しない。

- AC1: `comfy/ops.py` の `safe_linear` と `_should_retry_cuda_linear`、`comfy/model_management.py` の `discard_cuda_async_error`、既存テスト6件の本文を照合。デバイス別 set、入力デバイスの指定、エラー allowlist、量子化・layout 除外を確認した。文書内のローカルリンク3件の実在も確認。
- AC2（対象検証）: `/home/jinno/ComfyUI/.venv/bin/python -m pytest tests-unit/comfy_test/test_safe_linear.py -q` → `6 passed in 0.49s`、exit 0。CPU テンソルとモックによる検証であり、実機の複数 GPU・cuBLAS 障害回復・性能は未検証。
- AC2（全体 gate）: `make test` はこの worktree に `.venv` がなく exit 2（Python 起動 error 127）。既存環境を指定した `make test PYTHON=/home/jinno/ComfyUI/.venv/bin/python` は exit 0。ログ `/tmp/comfyui-113783-tests.log` は2002件の収集と末尾の websocket テスト成功を記録するが、pytest の最終集計行がないため、集計結果としての成功・スキップ件数は断定しない。`git diff --check` と文書内の旧記述の残存・リンク先・テスト数・スキルヘッダ検査も成功。
- 証拠 SHA-256: `comfy/ops.py` = `39d4699f2cefea9f68e37a7833d67b474f3e4575c9c7454cfe3189aba3f34bec`、`comfy/model_management.py` = `44f981415e3b1c5882b881b98d9bb761d369739b3b29a5ff1b5d9eee74da88a8`、`tests-unit/comfy_test/test_safe_linear.py` = `3a5caffe55047c8d59a7f67409178628ac7162705d3cd582be4f8c6d1bbb0cbc`。

ペルソナレビュー（AC3）: Codex がリポ固有の2視点で自己レビューした。独立した人物・モデルのレビューではない。手順は `.claude/skills/persona-review/SKILL.md` に新設。

| 視点 | 反応・指摘 | 処置 |
| --- | --- | --- |
| ローカル生成ワークフロー利用者 | 「詳細節を直しても、冒頭と改善候補に全 GPU 一括切替・テスト不在と残っていると、まだ修正が必要なのか迷う。」 | 要約表、H5・M6、戦略的注記、検証表、末尾の未検証事項を同じ実装証拠で訂正した。 |
| デバイス・回帰テスト保守者 | 「6件のテストだけで実機の複数 GPU も安全とは言えない。旧記述のオーバーヘッドゼロ・数値健全も測定根拠がない。」 | CPU・モックでの保証範囲と実機・性能の未検証を明記し、根拠のない性能・数値評価を削除。行番号に依存した参照をファイルリンクとシンボル名へ変更した。 |
