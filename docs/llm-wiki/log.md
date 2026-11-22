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

## 2026-10-21 — 計画スパイン新設（dot-milestone-loop 適用、docs-only）

`docs/plan/` に長期方針の見直し・約30分実行波・Dot 向けワーカー指示書を新設した。charter MS-003 の「固定 14 ファイル構成」が 820d2ae4 (#43) 後の追跡 3 ファイル構成と乖離していることを観測し、実行波 WP-C1 で charter 整合を計画。MET-001 の実測（2026-10-10）は観測時点の記録として保持し、再観測を WP-C2 で計画。スキル適用は計画整備までで、Dot の起動は含まない。

- **Verification**: 観測基準 4c0788db9379bfe8013093b8339436b0175622c4。.concept/ 追跡 3 ファイル（ls 実測）、models.py 6 テーブル、alembic versions 0001..0008（本日観測）。テスト実測は未取得（docs-only のため製品 suite は再実行せず、WP-C2 として計画）。

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

| 視点 | 素の反応・粗指摘 | 適用した処置 |
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

## 2026-10-30 — charter MS-003 を現 .concept 追跡構成へ整合（WP-C1）

milestones.md 実行波 WP-C1。820d2ae4 (#43) 後の実態に合わせ、charter MS-003 の deliverables を「固定 14 ファイル構成」から手管理シード 3 ファイル（charter.yml / autopilot.yml / ontology_budget.yml）+ 生成ランタイム非追跡ガード（tests-unit/concept_metadata_tracking_test.py）へ更新した。intent の不存在参照（autopilot 品質基準 Q1-Q8 — 現行 autopilot.yml には存在しない）も除去。status は継続活動のため active のまま。

- **Verification**: `git ls-files .concept`（3 seeds）と deliverables 記載の一致、`.venv/bin/python -c "import yaml; yaml.safe_load(open('.concept/charter.yml'))"` 成功、`pytest tests-unit/concept_metadata_tracking_test.py` 15 passed。

## 2026-10-30 — S2 実行波（LOOP 接続の評価）を milestones.md に再計画

S1 波（M-A/M-C）の完了条件「完了後に S2（LOOP 接続の評価）を次の波候補として再計画する」に従い、docs/plan/milestones.md に S2 波を WP-S2-1（LOOP run の plan 由来候補接続の評価）/ WP-S2-2（評価結果に応じた維持・是正方針の確定）として定義した。long-term-direction.md の現在地・段階表を「S2 再計画待ち」から「S2 計画済み・実行待ち」へ更新。本再計画自体が、plan 完了条件由来の候補を LOOP run が拾った最初の証拠となり、WP-S2-1 の判定入力になる。

- **Verification**: `.concept/charter.yml` の yaml parse 成功（docs-only 変更で charter 無影響）、milestones.md の S2 依存（WP-S2-1 → WP-S2-2）と long-term-direction.md 段階表 S2 行の突合、S1 全 WP 着地 commit の確認（d633a060 / 1d188bb9 / c102509a / 07ab2fba を git log で実在照合）。

## 2026-10-30 — LOOP run の plan 由来候補接続を判定（WP-S2-1）

milestones.md 実行波 WP-S2-1。TAS dispatch の LOOP run が docs/plan/ を候補源として参照し plan 由来の残課題を実際に比較・選択・実行しているかを、2026-10-23 以降の `bounded_improvement` stage 14 run の出力（`~/ai-hub/runs/<run_id>/claude_stdout.txt`・`accepted_work.json`）と着地済み commit から判定した。判定は「接続は機能している（維持で足りる）」。plan ソース参照 13/14 run、plan 由来候補の比較 12/14 run、選択・実行 10/14 run、waiting 2 run。着地 5 commit（d633a060 / 1d188bb9 / c102509a / 07ab2fba / 858c337b）はいずれも plan 由来作業の成果物で accepted_work.json の candidate_sha と一致する。接続経路は LOOP.md の候補順ではなく dispatch mission の候補源比較であり、LOOP.md への docs/plan/ 追加（管理印削除＝owner 判断）は判定上不要。判定記録・判定表・観測 gap（同一 WP への重複並列 / venv 不在による waiting / 未着地候補の残置）と解除条件は docs/plan/milestones.md に記載。charter の MS status は変更していない（判定は MS の done に読み替えない）。

- **Verification**: `git log --no-walk d633a060 1d188bb9 c102509a 07ab2fba 858c337b` で 5 commit の実在照合、`git merge-base --is-ancestor` で未着地 7 commit（ca8d3d82 / ab1abc55 / 7004c49e / 762c79b3 / 86cc64fe / 0b46de87 / ce66a68d）が HEAD に含まれないことを確認、各 run の `accepted_work.json` の candidate_sha と判定表の run_id 対応を突合。

## 2026-10-30 — LOOP 候補接続の維持方針を現状維持に確定（WP-S2-2）

milestones.md 実行波 WP-S2-2。WP-S2-1 の判定（接続は機能している・維持で足りる、commit 8bb2cfcc）に基づき、plan 残課題を LOOP 候補集合へ継続的に取り込む経路の方針を (a) 現状維持 に確定した。LOOP.md の候補源への docs/plan/ 追加（b）は管理印（loop-md:spec v3）削除＝owner 判断を伴うが判定上不要のため起こさず、接続不全時の是正案（c）は対象事象が観測されていないため成立しない。owner 判断事項は発生していない。観測 gap G1（重複並列 claiming・dispatch 側）/ G2（worktree venv・runner 側）/ G3（未着地候補・harness/TAS 側）は解除条件つきで milestones.md に記録し、本波では着手しない。S2 波は両 WP の記録完了で着地待ち。着地後は plan 由来残課題の有無を確認して LOOP の通常候補順へ戻り、S3 は所有者の明示指示が前提。charter の MS status は変更していない。

- **Verification**: LOOP.md・.concept/charter.yml の無変更を git diff で確認（loop-md:spec v3 印は残存）、方針記録と AUTOMATION.md の driver 構成（TAS が dispatch と着地、Woodpecker が CI gate）の突合で矛盾なし、milestones.md の「WP-S2-2 方針記録」と long-term-direction.md の現在地・段階表 S2 行の突合。

## 2026-10-30 — CODEBASE_ANALYSIS.md を現行コードと同期（解決済み欠陥の台帳反映）

fork の欠陥台帳 `docs/CODEBASE_ANALYSIS.md` について、オープンと記載されていた指摘のうち 6 件（H1 認証ヘッダ平文ログ、H2 prompt_worker 例外ガード、H3 /interrupt TOCTOU、H6 マイグレーション前ロック、H7 LoadImage 無音フレーム破棄、M4 progress_state 再送レート制限）が現行コードで解決済みであることを実コード再読と `git log -S` で裏取りし、根拠 commit（`fd7bfcd3` フォーク対応 / `985fb9d6` 上流 #14774 / `c8b61a95` / `19e1058f` #16295）付きで解決記載に更新した。現存は unblockedEvent 無タイムアウト待ち（`graph.py:290`）と audio 系 F821 2件（`audio/dit.py:190` / `audio/autoencoder.py:94`）のみ。H8 は `sub_quadratic_attention.py` 削除済みのため対象縮小、`flux/model.py` の旧指摘行は上流書き換えで要再確認と記録。フォーク固有コミット数は 63（`a402fd40^2..HEAD`、2026-10-30 実測）、unit スイート実測は 1923 passed / 0 failed / 72 skipped（`make test` 約6分）。コード・charter・LOOP.md は変更していない。

- **Verification**: `make test` で 1923 passed / 0 failed / 72 skipped（1995 collected）、`git log -S "keeping the worker alive" -- main.py` 等で解決 commit の実在照合、`sed` による `server.py` / `comfy_api_nodes/util/request_logger.py` / `app/database/db.py` / `comfy_execution/graph.py` / `comfy/ldm/audio/*.py` の現行コード再読、`git diff` で変更が `docs/CODEBASE_ANALYSIS.md` と本ログのみであることを確認。

## 2026-10-30 — CODEBASE_ANALYSIS.md の flux/model.py 旧指摘を現行コードで再確認

前エントリで「要再確認」と記録した flux/model.py の旧指摘（死に lambda + zeros 初期化依存の脆弱な順序）を、現行コード再読と git 履歴で判定した。(1) 死に lambda（`lambda a: 0 if a == 0 else a + txt.shape[1]` の式文、結果を捨てる）は上流 44f1246c（#12905 flux 2 klein kv cache）が導入し、fork 5bceba74（PR #7、2026-09-27）が除去済み。現行ファイルの唯一の lambda は `:268` で map 結果を `modulation_dims_combined` に格納して使用しており指摘対象外 → **解決済み**。(2) zeros 初期化依存の脆弱な順序は `process_img` の現行 `:337-341` に**現存** — `img_ids[:,:,0]` を ch1 がゼロの状態で読むため、行順序の入れ替えで ch0 が暗黙に h 位置 + index に変わる（現行動作は正しい、潜在リスク）。upstream 継承のため台帳方針通り upstream PR 経路で追跡し、本リポではコード変更しない。台帳 §2.3 row 4 / H8 行 / §3 Low 死にコード除去行 / ヘッダ更新行に反映。

- **Verification**: `git log -S "lambda a: 0 if a == 0 else a + txt.shape[1]" -- comfy/ldm/flux/model.py` で 44f1246c（追加）/ 5bceba74（除去）を実在照合、`git show 5bceba74 -- comfy/ldm/flux/model.py` で除去 diff を確認、現行 `sed` による `comfy/ldm/flux/model.py:268-269` / `:337-341` の再読、`make test`（docs-only のため回帰なし裏取り）。

## 2026-11-03 — 長期計画・マイルストーン整備（所有者指示 OI-20261103-32）

所有者の長期計画整備指示に従い、既存の正本（`.concept/charter.yml`）を基準に実行用の分解を整備した。`docs/MILESTONES.md` を新設し、charter の MS-001..MS-003 を `## MS-00X:` 形式（Outcome / Acceptance / Evidence / Status・依存・次の一手）で実行可能な単位として索引化し、直近の約30分枠（WP-A1: alembic upgrade head の実走）を明記した。charter には planning 入口（long-term-direction / milestones / MILESTONES）、各 milestone の depends_on・exit_criteria・next_action・evidence を追加し、旧記載だった MS-003 deliverables「固定 14 ファイル構成」を現構成（追跡3ファイル + runtime 非追跡ガード）へ修正した。`REPO_METADATA.json` は charter と `docs/plan/milestones.md` の投影として source_hash（git blob ID）・updated_at・verified_at を再計算した。

- **Verification**: 指定構造検証スクリプト（`VERIFY_PLANNING`）が `planning structure verified; semantic acceptance remains separate` で exit 0。charter は yaml parse 成功。追跡構成は `git ls-files .concept` で charter.yml / autopilot.yml / ontology_budget.yml の 3 ファイルを確認。
- 未了: MS-002 の alembic 実走証拠（WP-A1）と README 実態一致判定（WP-A2）、MET-001 の再観測（WP-C2）は未実行・未取得。MS-002 / MS-003 は in_progress、MS-001 は achieved（charter status=done と MET-001 記録 2026-10-10 が根拠）。

## 2026-11-07 — WP-A1 alembic 受入証拠の永続化（recovery run 20261107-235007-331852）

TAS run-853297c93e02（child 20261107-233514-229391）は WP-A1 を実行したが、定義が
`authorized_observation`（評価器構造上 supported にできず）＋ run レポートが worker
stdout のみで全 criteria unverified・評価 40 となった。本 recovery run で隔離一時 DB
（/tmp、ini 上書き、`user/comfyui.db` は実行前後とも不在）に対する実行を実施し直し、
コマンド・exit code・heads/current 出力・stepwise 8-revision トレース・DB 終状態を
`docs/plan/evidence/wp-a1-alembic-chain.md` として永続化した。MS-002 の charter 反映
（WP-A2）は別枠のまま。

- **Verification**: `upgrade head` exit 0（DB ファイル不在確認後の空 DB から）、
  `heads`/`current` = `0008_missing_content_age (head)`、stepwise 8×`upgrade +1`
  exit 0、`alembic_version` 行 = 0008、テーブル 6+alembic_version。元 run の失敗分類は
  評価証拠窓であって連鎖自体の失敗ではない。

## 2026-11-11 — 長期計画・マイルストーン整備（所有者指示 OI-20261111-12）

計画スパインを main で再観測した事実に合わせて更新した。長期方針（`docs/plan/long-term-direction.md`）に「優先順・依存・出口条件・次の一手」の節を追加し、`.concept` 同期行の旧乖離記載（旧「固定 14 ファイル構成」）は WP-C1（2026-11-03 の eadbeeeb で着地済み）で解消済みと記載を改めた。アセット永続化行と `docs/MILESTONES.md` の MS-002 は、WP-A1/WP-A2 の成果（6d8fbffd / 886ec49a / ae41a228）が未着地ブランチにのみ存在し main には無いことを明記し、status は据え置いた（MS-002 は charter どおり active）。直近の約30分枠は WP-A1 から WP-C2（`make test` の1回実測と MET-001 記載更新）へ更新。`REPO_METADATA.json` は `repository_metadata_format.py` の refresh / check で source_hash と verified_at を再生成した。

- **Verification**: `VERIFY_PLANNING` が `planning structure verified; semantic acceptance remains separate` で exit 0、`repository_metadata_format.py check` / `check-index` が success。観測事実: `git ls-files .concept` = 3 ファイル、`.concept/*.yml` の yaml parse 3/3 OK、runtime 12 ファイルの check-ignore 12/12、`alembic_db/versions` に 0001..0008、main の `alembic_db/README.md` は 4 行。
- 未了: MET-001 の再観測（WP-C2）は未実行。MS-002 の受入証拠は未着地のままで、default 着地までは active。charter の status は変更していない。

## 2026-11-23 — PR #63 auto_merge_blocked の原因は tas_autopilot 側チェック登録漏れ

inbox-care 調査（run 20261122-175820-206928）で PR #63 の「failed CI」通報を検証した。
PR の CI は実際には green（`ci/woodpecker/pr/woodpecker` SUCCESS、head
f7139216 一致、producer tas-bot）。`auto_merge_blocked` は tas_autopilot
`post_dispatch.py` が origin slug `jinno2/ComfyUI` を required-check 登録テーブルに
持たず、未登録リポの PR CI を failed 扱いにするため（PR が `.woodpecker.yml` を
base→head で変更しているため CI 期待判定も真）。登録は repo 外のため
`docs/llm-wiki/relations.md` の tas_autopilot 節に follow-up を記録し、証拠
（gh 出力・出典 excerpt・sha256）は
`docs/plan/evidence/20261123-pr63-outcome-check-registration.md` に永続化した。
あわせて MS-003 `intent:` 行のインデクト欠落で不通だった `.concept/charter.yml`
を修復（yaml parse exit 0）。

- **Verification**: `gh pr view 63` rollup SUCCESS / `gh api .../status` combined
  success（GraphQL creator=tas-bot）/ `git diff --stat base head -- .woodpecker.yml`
  = 5 insertions, 21 deletions / `yaml.safe_load('.concept/charter.yml')` exit 0。
- 境界: tas_autopilot の登録テーブル修正は本リポの書込範囲外（follow-up 参照）。
