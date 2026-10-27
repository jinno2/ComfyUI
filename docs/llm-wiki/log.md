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


## 2026-10-23 — モデルプレビュー検索でglob特殊文字をリテラルに扱う

Run: `20261023-170524-515104`。Task: `tas-task-508bebb6a4041f01ead1897a53705607288280ee17b06e7176056628f0451d5e`（17:08:53 UTC 登録、AC1–AC4）。LOOP・PURPOSE・charter、docs/dot の計画、既存解析、TODO、ソース・テスト、Makefile・CI・設定を比較。既定の `make test` は worktree の `.venv/bin/python` 不在で exit 2（recipe error 127）だったため、既存環境を指定して gate を確認した。モデル一覧キャッシュの修正は、メタデータと pathIndex の無効化条件まで変え得るため今回選ばず、`ModelFileManager.get_model_previews` のリテラルパス検索を1件の改善として選択した。

判断と反証: 「モデルのパスをそのまま glob に渡しても対応ファイルだけを探せる」という前提は成立しない。`model[v1]` や格納先の `[]` で404になり、`modelv.safetensors` の別のカバー画像を選ぶ場合もある。AC1 の変更前回帰テストは `7 failed, 9 passed`（exit 1、`/tmp/comfyui-20261023-170524-preview-red-final.log`）。basename 全体に `glob.escape` を適用し、拡張子探索用の末尾 `.*` だけをパターンとして残した。依存・通信・モデル推論の変更はない。

- AC1・AC2: `/home/jinno/ComfyUI/.venv/bin/python -m pytest tests-unit/app_test/model_manager_test.py tests-unit/security_test/test_ghsa_779p_02_preview_traversal.py -q` → `23 passed in 1.15s`、exit 0（`/tmp/comfyui-20261023-170524-preview-green.log`）。リテラル名・格納先のカバー画像、`.png` / `.preview.png`、別モデルの黒い画像が混在する場合に白い対象画像が返ることをHTTP応答の画素で確認。既存の traversal・symlink・不正インデックス・空名・NUL の7ケースも通過。
- AC3: `/home/jinno/.local/bin/ruff check app/model_manager.py tests-unit/app_test/model_manager_test.py` → `All checks passed!`、exit 0。`git diff --check` 成功。
- 証拠 SHA-256: `app/model_manager.py` = `9e0ce83ef6704c0f341b8693e54e09fa76b90d8ced94abe94412f63bfc444061`、`tests-unit/app_test/model_manager_test.py` = `7ee02d5dfaa1a538793a990d9531bd7035451e1cc5d37d94d4f2ab153d08236b`。

AC4 ペルソナレビュー: `.claude/skills/persona-review/SKILL.md` に従い、Codex が要求、実装、HTTP応答と回帰テストを直接照合した視点別自己レビュー。独立した人物・モデルのレビューではない。

| 視点 | 反応・粗指摘 | 適用した処置 |
| --- | --- | --- |
| ローカル生成ワークフロー利用者 | 「プレビューが表示されても、別モデルの画像なら判断を誤る。200と画像形式だけでは不十分。」 | 通常名の既存テストも画素を検査するよう強化し、特殊文字を含む名前には黒い別モデルのカバー、対応ファイルには白い画像を置いて返却内容を確認した。 |
| デバイス・回帰テスト保守者 | 「Linuxで有効な `?`・`*` はWindowsでファイルを作れない。共通CIで作成自体が失敗するテストを入れないでほしい。」 | 該当するファイル・ディレクトリ名のケースだけ `os.name == 'nt'` でスキップ。`[]` と通常名のケースは維持した。Windows・macOS実機は未検証。 |

wiki index に確認済みの挙動とテストへのリンクを追加し、relations の index 証拠ハッシュを更新した。リポ間の責務・依存関係・既存概念は変更なし。実モデル生成・GPU推論は検証対象外。

全体gateの実行条件: 変更前に起動した `make test PYTHON=/home/jinno/ComfyUI/.venv/bin/python` は動画変換テストまで進行し、修正済み内容での最終gateへ切り替えるため、自分の pytest PID 1111258 に SIGTERM を送って終了した（make exit 2、`/tmp/comfyui-20261023-170524-baseline.log`）。この中断を成功として数えない。最終gateは同じPython・既定のスレッド設定で起動し、追加ケースを含めて検証する。

- AC3 最終gate: `make test PYTHON=/home/jinno/ComfyUI/.venv/bin/python` → exit 0。最終集計行は出なかったため、ANSI色を除去した行末マーカーを数え、収集2031件＝`PASSED` 1957件＋`SKIPPED` 74件、`FAILED`・`ERROR`・`XFAIL`・`XPASS` 各0件を確認した。末尾の websocket テストまで到達。ログ: `/tmp/comfyui-20261023-170524-final-tests.log`。Ruffは上記の同じPython差分に対する成功結果を使用。既定の `make test` の環境不備は修正しておらず、実行時は既存のPythonを指定する。
- AC4 記録検査: 新しいwikiのリンク先3件の実在とlog見出し、relations内の当リポ証拠2件（index・README）のSHA-256一致を確認した。最終 `git diff --check` も成功。成果はプレビュー検索の改善1件で、独立した別改善・upstream操作・merge・push・deployは行っていない。

## 2026-10-23 — fork 履歴の現行計測 pointer を更新

Run: `20261023-190012-301392`。Task: `tas-task-508bebb6a4041f01ead1897a53705607288280ee17b06e7176056628f0451d5e`（AC1–AC5）。LOOP の `make test` は `.venv/bin/python` 不在で exit 2（Makefile:452、recipe error 127）。これはテスト失敗ではなく、D1-1 の条件も venv 不在時は `not_needed` と定めている。次の具体作業として D1-2 を選択し、解析文書と wiki に残った古い fork 件数を、履歴値と再測定方法が区別できるよう更新した。

仮定／反証: `up/master` の lag 0 を現在の upstream 同期状態と扱える、という仮定は、ref の tip が `f6c162ddcfbd7eefb39c06fe5b8d4c46e8d09f40`（2026-06-23）であることに反証される。したがって最新 upstream への遅れは未確認として、文書ではローカル ref の古さを明示した。

計測時刻 `2026-10-23T19:02:33Z`。実行結果:

- `git rev-list --count a402fd40^2..HEAD` → `69`
- `git rev-list --left-right --count origin/main...HEAD` → `22 38`（origin/main 側のみ22、HEAD側のみ38）
- `git rev-list --count HEAD..up/master` → `0`
- `git log -1 --format=%H up/master` → `f6c162ddcfbd7eefb39c06fe5b8d4c46e8d09f40`

`docs/CODEBASE_ANALYSIS.md` は13件を2026-09-20の履歴値と明記し、2026-10-23の計測値と再現コマンドを追記。Wiki index は20 / 43 / 48と、2026-10-22時点のup/master比較を履歴値として保持し、current値を再取得するコマンド群と古いrefの注意を明記した。現行数値の唯一の再現元はGit計測。relationsのindex SHA-256も更新した。

ペルソナレビュー（`.claude/skills/persona-review/SKILL.md`、Codexによる視点別自己レビュー。独立レビューではない）:

| 視点 | 素の反応・粗指摘 | 適用 |
|---|---|---|
| ローカル生成ワークフロー利用者 | 「up/master の lag 0 を見て、ComfyUI upstream に追いついていると誤解しそう。」 | ref の日付とSHAを記録し、現行 upstream の状態を示さないと明記。 |
| デバイス・回帰テスト保守者 | 「件数だけだと追試できない。どの境界を数えたかと作業コピーの状態を分けてほしい。」 | fork固有件数、origin/mainとの差、ローカルup/masterとの差を別コマンドと結果で記録。 |

検証: `make test PYTHON=/home/jinno/ComfyUI/.venv/bin/python` → exit 0（約12分）。RTK保存ログ `/home/jinno/.local/share/rtk/tee/1792782944_make_test_PYTHON__home_jinno_ComfyUI__ve.log` の最終到達テストは websocket feature negotiation。詳細行を数えると 2031件＝PASSED 1957件＋SKIPPED 74件、FAILED / ERROR / XFAIL / XPASS は0件。index のrelations SHA-256を実ファイルから再計算して照合し、`git diff --check` も成功。既定 `make test` は worktree の `.venv/bin/python` 不在で exit 2 だった。コード・依存・外部通信・モデル動作の変更はなく、今回の数値計測はその時点のローカルGit参照に限る。最新 upstream のlag、GPUや実モデル動作は未検証。

## 2026-10-24 — Multidimensional sampler mask bounds

Run: `20261023-193422-189800`。Task: `tas-task-508bebb6a4041f01ead1897a53705607288280ee17b06e7176056628f0451d5e`（AC1–AC4）。LOOP の最優先 gate を先に確認し、既存 ComfyUI venv で `make test` が exit 0（2031 collected: 1957 PASSED, 74 SKIPPED）だったため、次候補の `comfy/samplers.py` に残る `set_area_to_bounds` の `dim != 2` TODO を選んだ。旧 `get_mask_aabb` は2軸の座標だけを返し、resolver も固定4要素の area を生成していた。

`get_mask_aabb` と area 生成を次元数に沿って計算するよう変更。area は従来通り sizes、offsets の順で、2D は既存の8×8最小サイズを保持。3D latent では先行軸の最小サイズを1、末尾2軸を8とし、時間方向に不要な領域を広げない。空 mask の offset は全軸0。テストは `get_area_and_mult` まで通し、3D crop と mask alignment を CPU/CUDA で検査した。

ペルソナレビュー（`.claude/skills/persona-review/SKILL.md`、Codex による視点別自己レビュー。独立レビューではない）:

| 視点 | 素の反応・粗指摘 | 適用 |
|---|---|---|
| ローカル生成ワークフロー利用者 | 「3D mask の時間方向まで最小8にすると、必要以上のフレームを計算しそう。」 | 先行軸は最小1にし、3D の temporal extent を保つ回帰テストを追加。 |
| デバイス・回帰テスト保守者 | 「bounds の tuple だけでは、sampler が同じ範囲で latent と mask を切るか分からない。」 | `get_area_and_mult` の結果 shape、latent crop、mask multiplier を検査。CPU/CUDA で実行。 |

検証: focused `pytest tests-unit/comfy_test/test_sampler_masks.py -q` → `8 passed`（CPU/CUDA）。`ruff check comfy/samplers.py tests-unit/comfy_test/test_sampler_masks.py` と `git diff --check` は成功。最終 gate `make test PYTHON=/home/jinno/ComfyUI/.venv/bin/python` → exit 0、2039 collected: 1965 PASSED + 74 SKIPPED、FAILED / ERROR / XFAIL / XPASS は0件。ログ: `/home/jinno/.local/share/rtk/tee/1792785452_make_test_PYTHON__home_jinno_ComfyUI__ve.log`。既定の `make test` は worktree-local `.venv/bin/python` が無く exit 2、ai-hub 共通 venv は `torch` 不在で利用できなかった。

証拠 SHA-256: `comfy/samplers.py` `62a5b7661039af57a91a3ac03ef7cbf324b8d6978265fa270d2359d60a249875`; `tests-unit/comfy_test/test_sampler_masks.py` `62e7069cc702acdb6fc3c5112ea15ea57b32ae39f5eb5f242aca54a6150d1d96`; `docs/llm-wiki/index.md` `5921d49413303d4939788aadfa8aa694f2026d819fd918f337e53415106d1e66`。relationships memo は repository 間の責務・依存に変更がないため更新なし。フル denoising workflow と CUDA 以外の device backend は未検証。

## 2026-10-24 — chain fix stage 第2走の再検証（修復見送りの維持・追補）

Run: `20261024-103648-847785`。Task: `tas-task-13f824a3f165239b7f91dca20264e16508bb7dd7e18c105c12cd13599ef9ec16`（AC1–AC3）。source run `20261024-042226-078222` の terminal `Final stage evaluation or landing failed` を受ける同 chain の第2 fix stage。**結論（冒頭）: ComfyUI 自体に問題は見つかっておらず、修正対象は本リポに存在しない。fix_applied=false（report-only）。** 前 fix stage（run `20261024-101809-368391`）の完全な検証記録は commit `3bbbde61`（branch `ai/ComfyUI/instruction-20261024-101809-368391`、前エントリ本文の SHA-256 は `bafdf7f532489fddd80eb89a83e027bdaed99624c40666acc189c81868310fe9`）にあるが、この commit は本 worktree の分岐元 `07ce11c3` に含まれず、着地も未確認のため、本追補を本 worktree 側の追跡記録として残す。内容は前エントリの複製でなく相互参照である。

再検証した事実（すべて読み取り専用・本 run 内で再実行、前記録と逐一致）:

- source run dir `/home/jinno/ai-hub/runs/20261024-042226-078222/` は依然不存在（sibling `20261024-04*` 6 件 041132 / 041142 / 042354 / 042606 / 044551 / 045605 は存在）。recovery binding は本 run prompt への注入 JSON `{"phase": "evaluation", "state": "binding_unavailable"}` のまま（`phase: evaluation` まで明記）。元受入条件・候補 commit は復元不能。
- ComfyUI リポに `*042226*` に一致する branch は無く、当該 window の候補着地も無い。ハーネス側 2 ファイルの SHA-256 は前記録値から未変更（末尾の証拠行）＝ 前回検証以降、gate 側ソースに変更はない。
- fleet 側推奨 3 件（失敗 run の `ai-hub runs/<id>/` 証拠保存 / no-configured-test target への明示的 verification outcome 記録 / evaluation gate の fleet 全体見直し）は報告のみのまま変更なし。

ペルソナレビュー（`.claude/skills/persona-review/SKILL.md`、同一エージェントの視点別自己レビュー。独立レビューではない）:

| 視点 | 素の反応・粗指摘 | 適用 |
|---|---|---|
| ローカル生成ワークフロー利用者 | 「また fix stage の記録？ComfyUI を使う側に影響はあるのか、前のエントリと何が違うのか分かりにくい。」 | 結論（ComfyUI 無関係・修復対象なし）を冒頭に明記し、追補が前エントリの複製でなく相互参照である理由（分岐元に commit が含まれない・着地未確認）を記した。 |
| デバイス・回帰テスト保守者 | 「SHA-256 一致だけでは、何を検証したのか・テスト未実行の根拠が分からない。」 | コード変更ゼロゆえテスト未実行（dispatch verification は fallback 経路）を明記し、ai-hub 側ソースはリポ外参照であることを `ai-hub` プレフィックスとハッシュで足場固定した。 |

検証: `ls`（run dir 存在確認）、`git branch --all --list '*042226*'`（候補 branch 不存在）、`git show 3bbbde61:docs/llm-wiki/log.md` からの前エントリ抽出と `sha256sum`、ai-hub 側 2 ソースの `sha256sum` 再計測を本 run 内で実行し、調査報告（20261024-094112-899632）・前 fix stage エントリの記載と一致した。本 run の ComfyUI 側変更は本追補の 1 commit のみ（source / tests / 設定 / `.concept` 無変更）。コード変更ゼロのためテストは未実行で、dispatch verification は前回と同じく fallback 経路になる。未検証: require_tests_pass gate 経路は前回と同じ hypothesis のまま（直接観測には ai-hub 側 dispatch 設定の読み替えが必要で本 run の対象外）。

証拠 SHA-256: ai-hub `tools/harness/runners/chain_orchestrator.py` `314af180c11b93290350e1d5fa1c34f0e85d7657b96073f1fb99a0fecb837127`; ai-hub `tools/harness/core/recovery_binding.py` `e6c9ccb78986027463c4dd2e67f121f8a445b07b4549a51cafa44ce1f7416627`（前 fix stage エントリ記録値と一致）。relations memo はリポ間関係の変更がないため更新なし。deleted run の元受入条件・候補は復元不能のまま（gap として報告）。

## 2026-10-26 — auto_merge_blocked 反復の根本原因検証（修復オーナーは本リポ外の tas_autopilot）

Run: `20261026-142919-061901`。Task: `tas-task-42e250c42d29ef36755b6681f059e36f63cf52102971bd9fad8b5e28a1a2efcb`（AC1–AC3）。investigate stage（`20261026-140924-105242`）の報告を受け、証拠不足で評価 N/A だった前 fix stage（`20261026-142512-752205`）を引き継ぐ fix stage 記録。**結論（冒頭）: ComfyUI 本体に欠陥はなく、修復オーナーは tas_autopilot `tas_autopilot/control_plane/post_dispatch.py` の PR 衝突採用経路。fix_applied=false（report-only）。**

再現（すべて読み取り専用。worktree `/home/jinno/ComfyUI-aihub-20261026-142919-061901`、観測 2026-10-26T14:32–14:34Z、gh 2.46.0）:

- リモート: `origin=jinno2/ComfyUI`、`up`/`upstream=Comfy-Org/ComfyUI`、`jinno=nobu007/ComfyUI`。`.git/config` に gh 既定リポの保存値（gh-resolved 相当）は無く `GH_REPO` も未設定 — 解決は gh の複数リモート解決による。
- `gh repo view --json nameWithOwner`（--repo なし）→ `{"nameWithOwner":"Comfy-Org/ComfyUI"}` — origin でなく upstream 側を既定リポに解決。
- `gh pr list --head tas/auto/4b4cfc7bb619 --base main --state open --json number,url,headRefName,baseRefName,state`（--repo なし）→ `[]`。
- 同クエリに `--repo jinno2/ComfyUI` → PR #46（`state: OPEN`、base `main`、作成 `2026-10-23T14:06:03Z`）— inbox 記録 `a pull request for branch "tas/auto/4b4cfc7bb619" into branch "main" already exists: https://github.com/jinno2/ComfyUI/pull/46` と一致。

ソース非対称（tas_autopilot commit `3dfc7d0f` 時点、ファイル sha256 は末尾の証拠行、行番号はこの時点のもの）:

- `gh_create_pr`（:942）は `_origin_repo_slug`（:932）で origin slug を計算し `args.extend(["--repo", repo_slug])`（:982）で `pr create` をピン留めする。直上のコメントに「fork checkout では gh が fork 親を既定リポに昇格させる（2026-10-23 Roo-Code-Auto の archived 親リポ事例）」という既知挙動への対処としての rationale が明記されている。
- 一方、衝突回収は `_adopt_existing_pr`（:886）→ `gh_list_open_pr`（:229）へ委譲し、`pr list` 引数は `args = ["pr", "list", "--head", branch, ...]` と `--repo` なしで組み立てられる。`gh_create_pr` が計算済みの slug は採用照会へ渡されない。
- 効果: 衝突検出後の採用照会だけが upstream（Comfy-Org/ComfyUI）を検索して `None` を返し、`gh_create_pr` は `PostDispatchError(kind="auto_merge_blocked")` を raise する。既存 PR を採用できるはずの正常な再 dispatch まで偽陽性エスカレーションとして inbox に記録される — 本件が反復する構造。

修復方針（本リポ外。tas_autopilot lane のフォローアップ）: `gh_create_pr` の計算済み `repo_slug` を `_adopt_existing_pr` / `gh_list_open_pr` へ渡し、`pr list` 引数に `["--repo", slug]` を追加する（:982 と同一の fork 親ピン留め rationale）。upstream リモートを持つ fork 構成を模した回帰テストを推奨。LOOP.md の対象外リポ編集禁止により本 run では実装せず、relations memo に完了条件付きフォローアップを追補した。実用上の注意: この checkout で素の `gh pr` 系コマンドは upstream 側を既定解決するため、fork 側を扱う場合は `--repo jinno2/ComfyUI` か `GH_REPO` の明示が必要。既存 PR #46 自体は OPEN のまま有効であり、本件は偽陽性エスカレーションであって PR 側の異常ではない。

ペルソナレビュー（`.claude/skills/persona-review/SKILL.md`、同一エージェントの視点別自己レビュー。独立レビューではない）:

| 視点 | 素の反応・粗指摘 | 適用 |
|---|---|---|
| ローカル生成ワークフロー利用者 | 「この checkout で `gh pr list` を素で叩くと upstream を見るという利用上の落とし穴は？ PR #46 自体はどうなるのか分からない。」 | gh 既定解決の実用上の注意（`--repo` / `GH_REPO` 明示）と、PR #46 は有効なまま・本件は偽陽性エスカレーションであることを本文に追記した。 |
| デバイス・回帰テスト保守者 | 「行番号と gh の解決挙動は時点・バージョン依存では？ 追試できる形にしてほしい。」 | 行番号を tas_autopilot commit `3dfc7d0f` とファイル sha256 に紐付け、gh 2.46.0 と `.git/config` 既定値なし（ヒューリスティック解決の裏取り）を記録した。 |

検証: `git remote -v`、`git config --local --list`（gh 既定値なし）、`gh repo view` 1 件と `gh pr list` 2 パターン（上記の通り）、`grep -n` によるシンボル位置と `--repo` 追加箇所の確認、外部ソースの `sha256sum` を本 run 内で実行。本 run の ComfyUI 側変更は本エントリと relations 追補の 1 commit のみ（source / tests / 設定 / `.concept` 無変更）で、コード変更ゼロのため ComfyUI 側テストは未実行。未検証: tas_autopilot 側の修正適用とその回帰（修復 lane の担当）。

証拠 SHA-256: tas_autopilot:tas_autopilot/control_plane/post_dispatch.py `2fa168013ddd7a4fe7b8a3581d81d52c6d730a8f28410d2a5ae2a1215f15a7a4`（観測時点・commit 3dfc7d0f）。

## 2026-10-26 — auto_merge_blocked 修復の検証（tas_autopilot a7b32ab、衝突採用クエリの origin ピン留め）

Run: `20261026-151359-308869`。Task: `tas-task-42e250c42d29ef36755b6681f059e36f63cf52102971bd9fad8b5e28a1a2efcb`（AC1, AC2）。fix stage（`20261026-150152-218452`）が tas_autopilot 側に残した修復 commit を検証した記録。**結論（冒頭）: 修復は実在し検証に合格 — tas_autopilot commit `a7b32ab`（branch `tas/auto-care/20261026`、2026-10-26T15:11Z 作成）。fork 親リポ構成での PR 衝突採用クエリが origin slug でピン留めされ、fork 親回帰テスト 2 件を含む `test_post_dispatch.py` 全 148 件がパス。ただし main（`3dfc7d0f`）には未マージで、着地は tas_autopilot 自身の PR 経路の担当。ComfyUI 側の変更は本 wiki 記録のみ。**

修復内容（`a7b32ab` の diff を実読。investigate stage `20261026-140924-105242` の修正方針に一致）:

- `gh_list_open_pr` が `repo_slug` 引数を新設し、指定時 `pr list` 引数へ `["--repo", slug]` を追加。
- `_adopt_existing_pr` も `repo_slug` を受けて採用照会へ伝播。
- `gh_create_pr` の衝突回収パスが計算済みの `repo_slug` を `_adopt_existing_pr` へ渡す（`pr create` の既存ピン留めと同一の fork 親 rationale）。slug 未導出時は従来どおり gh 既定解決。

検証（読み取り専用。観測 2026-10-26T15:23Z）: `git archive a7b32ab` を空の一時ディレクトリへ展開し、tas_autopilot の venv pytest で実行。`tests/unit/control_plane/test_post_dispatch.py` 全体 148 collected・全パス（exit 0）。`GhCreatePRAdoptionTests` 10 件パス。新規回帰 2 件 — `GhCreatePRAdoptionTests::test_fork_parent_adoption_query_pins_origin_repo`（origin+upstream リモートの fork checkout で採用クエリが `--repo jinno2/ComfyUI` を持ち PR #46 を採用）と `::test_adoption_query_without_slug_omits_repo_flag`（slug 無しでは `--repo` を付けない）— を個別指定でも 2 件パス。ハーネスのテストキャプチャは ComfyUI worktree 基準のため tas_autopilot 側セレクタを収集できず（前 fix stage で matched=0）、本検証は上記コマンドの実行記録による。

未検証・残課題: `a7b32ab` は `tas/auto-care/20261026` に停まっており tas_autopilot main への着地は未確認（本 run では push/merge を行わない）。relations memo の当該フォローアップは検証済みとしてチェックし、着地を完了条件付きの新フォローアップに分割した。偽陽性エスカレーションが実際に止まるかの観測（着地後の再 dispatch）は将来の run で確認する。

ペルソナレビュー（`.claude/skills/persona-review/SKILL.md`、同一エージェントの視点別自己レビュー。独立レビューではない）:

| 視点 | 素の反応・粗指摘 | 適用 |
|---|---|---|
| ローカル生成ワークフロー利用者 | 「main に未マージなら、この checkout の偽陽性エスカレーションはまだ続くのでは？」 | 冒頭と残課題に「main 未マージ・着地は tas_autopilot の PR 経路」を明記し、relations memo に着地フォローアップを新設した。 |
| デバイス・回帰テスト保守者 | 「148 件パスは一時展開ツリーでの結果。実 gh 呼び出しではなくモック単体では？」 | 検証元を `git archive a7b32ab` の展開（commit 内容そのもの）と明記し、回帰テストが `gh_runner` をモックした単体テストであることを記録。実 gh での再現は前 investigate stage 記録を参照（本 run では再実行せず）。 |

証拠 SHA-256: tas_autopilot:tas_autopilot/control_plane/post_dispatch.py（a7b32ab 時点）`3a15807d6432bf5ea0bc8b9ed35f6bdb403903c9a52bab397381700541a88af3`、tas_autopilot:tests/unit/control_plane/test_post_dispatch.py（同時点）`11f929b4ee9dd9a29c92ee279842f851223094df48d27ff4e390200cae9e84fe`。

## 2026-10-27 — chain fix stage 第4走の再検証（task_outcome unverified ゲートの一次確認・未着地候補 a8eb8bf は回収可能）

Run: `20261027-100223-919601`。Task: `tas-task-2ce4c9716dce3b620f73a7af2eacab93bba64a8973749c781a479df0df9b598d`（AC1, AC2）。alert-remediation ミッション（run `run-cbb2a1fb5bb3`、trigger: consecutive-run-failures）の fix stage。**結論（冒頭）: ComfyUI 側に修復対象は存在しない（fix_applied=false、report-only）。source run `20261027-090453-090835` の候補 commit `a8eb8bf8`（直上の「第3走」エントリ）は実在し、その内容は source AC を満たす（investigate stage `20261027-094339-074520` の判定: AC2 は claude_stdout で検証済み、AC1 は commit 内に実在）。回収（着地）はハーネスの通常 publication gate の担当であり、本 run が実行してよい修復ではない。修復オーナーは ai-hub ハーネス。**

再検証した事実（すべて読み取り専用・本 run 内で再実行）:

- source run 自身の失敗点を一次確認: `eval/20261027-090453-090835/eval.json` は `task_outcome.status = unverified`・judge score `96.0`（閾値以上）。criterion 行の reason は前向きな判定文と `criterion_lacks_observation_evidence`。つまり stage 失敗はスコア不足ではなく task_outcome ゲート due to citation 検証による格下げ。ai-hub `tools/harness/core/chain_execution.py` の `_evaluate_with_llm`（:534）は `task_outcome_unmet`（:539）をスコアゲート（:547）より先行させ、`tools/harness/runners/chain_mission_contract.py` の `accepted()`（:197、:205）も `task_outcome_unmet` に従属する。`data/chain_runs/bug_fix_cycle/error_context_20261027-090453-090835.json` も quality_score=0.93 / tests_passed=True / reasoning 前向きで「Stage evaluation failed」を記録。
- 格下げ機構の実在: ai-hub `tools/eval/criterion_outcomes.py` が `evidence_quote_mismatch`（:217）/ `invalid_criterion_evidence`（:232）/ `criterion_lacks_observation_evidence`（:252）を raise し、`_criterion`（:296）はこれらの例外を status `unverified` + reason 文字列へ落とす。訂正: investigate 報告のパス `tools/harness/runners/criterion_outcomes.py` は実在せず、実パスは `tools/eval/`。同日再発分 `eval/20261027-092317-170191/eval.json` は `unverified`・4 criterion 全行 `invalid_criterion_evidence` を直接示す。
- 第3走エントリ（a8eb8bf8、未着地）内の「score gate が原因」（`chain_execution.py:547`）の診断を部分訂正: 同行は実在するが、source run は閾値以上のスコアを持つためスコアゲート単独では説明できず、実際の失敗点はその手前の task_outcome ゲート。criterion citation 検証による機械的 `unverified` 格下げが原因（2026-10-24/27 エントリの score-gate-only 診断の精緻化）。
- 候補の回収可能性と binding: `git branch -a --contains a8eb8bf` は `ai/ComfyUI/instruction-20261027-090453-090835` のみ（未着地）。同 commit は本 worktree の分岐元 `728ad7bf` に含まれず、本エントリは log.md 末尾追記での相互参照（内容重複なし）。recovery binding 注入は `{"phase": "evaluation", "state": "binding_unavailable"}`。ただし 2026-10-24 事例（run dir 削除で候補不能）と異なり、今回は source run dir・eval・候補 commit がいずれも実在し identity は解決済み — 不足しているのは binding 証拠そのものであり、回収済みとは主張しない。

修復方針（本リポ外。ai-hub ハーネス lane のフォローアップ。investigate 報告の候補を転記）: (a) citation 検証による格下げをハードな stage 失敗でなく judge-retry（unverified 用の judge_resume 経路が既存）として扱う、(b) worker 最終回答を harness 観測チャネルに含め `authorized_observation` 基準に独立証拠源を与える、(c) task_outcome status で「judge 出力不良」と「task 基準未達」を区別する。LOOP.md の対象外リポ編集禁止により本 run では実装せず。

ペルソナレビュー（`.claude/skills/persona-review/SKILL.md`、同一エージェントの視点別自己レビュー。独立レビューではない）:

| 視点 | 素の反応・粗指摘 | 適用 |
|---|---|---|
| ローカル生成ワークフロー利用者 | 「第3走も第4走も結局何も直っていないのでは？ a8eb8bf はどこへ行ったのか。」 | 冒頭に候補の実在・回収可能性・着地担当（ハーネス）を明記し、本エントリは追跡記録で機能変更ゼロであることを記した。 |
| デバイス・回帰テスト保守者 | 「investigate 報告のパス間違い（runners/ vs eval/）を鵜呑みにしていないか。行番号は時点依存では？」 | 実パスを実読で特定して訂正を明記し、gate 行・例外理由の行番号を本 run 内の `grep -n` で確認した上で、ai-hub 側 4 ソースの現行 `sha256sum` を末尾に足場固定した。 |

検証: `sed`/`grep -n` による gate 行（:534/:539/:547、:197/:205）と例外理由（:217/:232/:252、:296）の実読、`eval/20261027-090453-090835/eval.json` と `eval/20261027-092317-170191/eval.json` および error_context JSON の実読、`git branch -a --contains`、`git show a8eb8bf8 --stat`、ai-hub 側 4 ソースの `sha256sum` を本 run 内で実行。コード変更ゼロのため ComfyUI 側テストは未実行（dispatch verification は fallback 経路になる）。未検証: ai-hub 側の修復適用とその回帰、a8eb8bf8 の着地（いずれも修復/着地 lane の担当）。

証拠 SHA-256: ai-hub `tools/harness/core/chain_execution.py` `0c93bcded5c2bc5ca3b69e9dc6b7d42b7f16c320f720f707155101d16956b924`; ai-hub `tools/harness/runners/chain_mission_contract.py` `63676e95bba88ff23dbce4762f58dd1485269eeba249d3a15c3995192b601359`; ai-hub `tools/eval/criterion_outcomes.py` `3900f6e0b872e96302dbe403e5cf1ef86af81bfbe26083af9b59c5dc35e99fc7`; ai-hub `data/chain_runs/bug_fix_cycle/error_context_20261027-090453-090835.json` `a41475c56e729e09c2318df7b37b396f32de756d7c570468eedcc7a94d9ba877`（いずれも 2026-10-27 観測時点）。
