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


## 2026-10-23 — API ログの認証・Cookie ヘッダを両方向でマスク

Task: `tas-task-508bebb6a4041f01ead1897a53705607288280ee17b06e7176056628f0451d5e`（AC1–AC4）。LOOP.md の候補と既存計画・ソース・テスト・docs・CI を比較し、解析文書 H1 に残るログ漏えいを1件の改善として選択した。既定の `make test` は worktree の `.venv` 不在で起動できたテストがなく、既存環境の指定で検証を継続した。

判断と反証: H1 の「全リクエスト認証ヘッダが無マスク」という旧記述は、既存の `_redact_headers` が Authorization と X-API-KEY を処理しているため現状と異なる。一方、Cookie とレスポンスヘッダは未処理だった。修正前の実ファイル回帰テストは `2 failed, 2 passed`（exit 1）となり、両方向で機密値が残ることを再現した。既存の共通処理に Cookie・Set-Cookie を追加し、レスポンスでも同じ処理を使う2行の実装変更とした。

- AC1・AC2: `/home/jinno/ComfyUI/.venv/bin/python -m pytest tests-unit/comfy_api_nodes_test/request_logger_test.py -q` → `5 passed in 7.84s`、exit 0。片方向ずつ・両方向同時のローカルログ実ファイルで、大文字小文字を混ぜた4種の機密値が消え、`***` の記録数が対象方向数と一致した。通常ヘッダ・ステータス・入力辞書の維持と、ヘッダが None/空辞書の場合も確認した。ログ: `/tmp/comfyui-20261023-150512-redaction-final.log`。
- AC3: 既定の `make test` → exit 2（`.venv/bin/python` 不在、recipe error 127）。`make test PYTHON=/home/jinno/ComfyUI/.venv/bin/python` → exit 0。最終集計行は出なかったため、ANSI 色を除去したログの行末結果マーカーを集計し、収集2007件と `PASSED` 1933件＋`SKIPPED` 74件の一致、`FAILED`・`ERROR`・`XPASS` 0件を確認した。末尾の websocket テストまで到達。ログ: `/tmp/comfyui-20261023-150512-final-tests.log`。変更前の同じ gate も exit 0（収集2002件、結果マーカー1928件＋74件）だった。
- AC3: venv には Ruff がなかったため既存の `/home/jinno/.local/bin/ruff check comfy_api_nodes/util/request_logger.py tests-unit/comfy_api_nodes_test/request_logger_test.py` を使用し `All checks passed!`、exit 0。`git diff --check` も成功。
- 証拠 SHA-256: `comfy_api_nodes/util/request_logger.py` = `84e02f245e51c1981c6aa04f4343377773c2e0c11ff9b33d6b36ba37e2f7f3cf`、`tests-unit/comfy_api_nodes_test/request_logger_test.py` = `23d6ba7ffa65c71df11e81a64a7c8bae0dc4448a5f3d2c9ee39306d45f976eed`。

AC4 ペルソナレビュー: `.claude/skills/persona-review/SKILL.md` に従い、Codex が元のH1、差分、テストの実ファイル検証を照合した視点別自己レビュー。独立した人物・モデルのレビューではない。

| 視点 | 反応・粗指摘 | 適用した処置 |
| --- | --- | --- |
| ローカル生成ワークフロー利用者 | 「認証情報の漏えい全般が直ったように読めると、何をログに残せるか判断を誤る。」 | 解析文書の H1 と要約・検証表を更新し、対象が4種のヘッダに限られ、URL・クエリ・本文・エラー文字列は対象外と明記した。 |
| デバイス・回帰テスト保守者 | 「片方向ずつ成功しても、リクエストとレスポンスが同時に渡る実際の呼び出しは検査していない。」 | 両方向同時のケースを追加し、マスク済みヘッダの記録数と入力辞書の不変性も確認した。全体 gate でも5件すべて PASSED を確認した。 |

関連記録: 新規テスト追加に合わせ、wiki index の188ソース監査を過去のスナップショットと明記した（監査の再実施・現行カバレッジの更新ではない）。リポ間の責務は変更なし。指示された証拠検査で relations.md の古い index ハッシュを更新し、既存4エントリすべてのパス・SHA-256を実ファイルと照合した。今回の成果はヘッダログの修正1件であり、外部サービス・実モデル生成・デバイス別推論は検証対象外。

## 2026-10-23 — smoke スクリプトで生成失敗を即座に検出

Run: `20261023-160240-999153`。Task: `tas-task-508bebb6a4041f01ead1897a53705607288280ee17b06e7176056628f0451d5e`（今回の登録は 16:06:26 UTC、AC1–AC4）。LOOP、PURPOSE、charter、TODO、既存解析、ソース・テスト・Makefile・CI を比較し、`make smoke` が使う `scripts/generate_one.py::wait_for_completion` の終了判定を1件の改善として選択した。解析 H2・H3 は現行コードでは既に対応されていた。モデル一覧キャッシュや settings TODO の変更は今回の対象外。

判断と反証: 「出力があれば生成成功」とは限らない。`main.py::prompt_worker` は失敗時も `status_str=error` の履歴を保存し、`execution.py::PromptQueue.task_done` は途中の出力をそのまま保持する。修正前の回帰テストは `3 failed, 4 passed`（exit 1）で、失敗時の不要な待機、途中出力の誤受理、出力なしの正常終了を待ち続ける挙動を再現した。エラーを出力・完了フラグより先に判定し、prompt ID とサーバログの確認先を示す例外にした。完了済みで出力が空の場合は呼び出し元の既存の「No images in outputs」判定へ戻す。

- AC1・AC2: `/home/jinno/ComfyUI/.venv/bin/python -m pytest tests-unit/scripts_test/generate_one_test.py -q` → `10 passed in 0.04s`、exit 0。エラー時の出力有無×`completed=False/True`、正常終了の出力有無、`status=None`、履歴未登録・404 後の成功、500 の伝播、未完了時のタイムアウトを検査。エラーでは HTTP 呼び出し1回・sleep 0回を確認した。ログ: `/tmp/comfyui-20261023-160240-polling-final.log`。
- AC3: 既定の `make test` は worktree の `.venv/bin/python` 不在で exit 2（recipe error 127）。既存環境を指定した変更前の `make test PYTHON=/home/jinno/ComfyUI/.venv/bin/python` は exit 0。最終集計行は出なかったため、ANSI 色を除去した行末マーカーを集計し、収集2007件＝`PASSED` 1933件＋`SKIPPED` 74件、`FAILED`・`ERROR`・`XPASS`・`XFAIL` 0件を確認した。ログ: `/tmp/comfyui-20261023-160240-baseline.log`。
- AC3: `/home/jinno/.local/bin/ruff check scripts/generate_one.py tests-unit/scripts_test/generate_one_test.py` → `All checks passed!`、exit 0。
- 証拠 SHA-256: `scripts/generate_one.py` = `da105f2677a1de3e4253a23dc9ab44a6be7659ecd8299c6e3f861080e897f0f7`、`tests-unit/scripts_test/generate_one_test.py` = `20880f202acbbc1793fd9b5375d46adc3a8d4f3d706528442fa474fef36e1584`。

検証環境の試行: `OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 make test PYTHON=/home/jinno/ComfyUI/.venv/bin/python` は既存の `video_types_test.py::test_save_to_transcode_keeps_audio_of_sparse_video` で数分進捗が出なかったため中断を判断し、自分が起動した pytest に SIGTERM を送った（make は exit 2）。終了ログでは当該ケースは PASSED に進み、次の `test_save_to_transcode_vfr_audio_covers_video_span` の実行中に停止していた。遅延の原因は未特定で、この試行を成功として数えない。ログ: `/tmp/comfyui-20261023-160240-final-tests.log`。コードを変更せず、変更前に成功したスレッド制限なしの条件で最終 gate を再実行した。

- AC3 最終 gate: `make test PYTHON=/home/jinno/ComfyUI/.venv/bin/python` → exit 0。最終集計行は出なかったため、ANSI 色を除去した行末マーカーを集計し、収集2017件＝`PASSED` 1943件＋`SKIPPED` 74件、`FAILED`・`ERROR`・`XPASS`・`XFAIL` 0件を確認した。追加10ケースすべてを全体実行でも確認し、末尾の websocket テストまで到達した。ログ: `/tmp/comfyui-20261023-160240-final-default-tests.log`。`git diff --check` も成功。

AC4 ペルソナレビュー: `.claude/skills/persona-review/SKILL.md` を使用し、Codex が元の終了判定、実際の履歴生成側、差分、回帰テストを照合した視点別自己レビュー。独立した人物・モデルによるレビューではない。

| 視点 | 反応・粗指摘 | 適用した処置 |
| --- | --- | --- |
| ローカル生成ワークフロー利用者 | 「画像が途中まで出ていても、最後に失敗した生成を成功として保存してほしくない。完了フラグだけでも判断できない。」 | エラーを最優先にし、途中画像の有無と `completed=False/True` の4ケースで即時失敗を確認。エラー文には prompt ID とサーバログの確認先を入れた。 |
| デバイス・回帰テスト保守者 | 「`task_done` は status を省略でき、履歴は `None` になり得る。新しい `.get` の連鎖で既存の履歴を壊していないか。」 | `status=None` を空辞書として扱い、既存の出力による終了を維持するテストを追加。HTTP と time はスクリプトの参照先をモックし、実通信・実 sleep を行わない。 |

リポ間の責務・依存関係・既存の概念は変更しておらず、relations と concept の更新は不要。実モデルによる画像生成、外部サービス、GPU・各デバイスでの推論は未検証。今回は履歴判定の改善1件であり、実生成の成功や性能改善を主張しない。
