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
