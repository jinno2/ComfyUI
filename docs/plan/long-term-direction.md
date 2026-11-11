# ComfyUI fork — 長期方針の見直し

<!-- BEGIN: GENERATED -->

計画確認日: 2026-10-21 13:05 WAT。基準: jinno2/ComfyUI @ 4c0788db9379bfe8013093b8339436b0175622c4。
再観測日: 2026-11-11（基準 commit 1f2eaea7）。下表の現状・証拠は再観測日の実測値。未着地の成果は「未着地」と明記し、main にあると記さない。
文書の役割: ゴール・マイルストーン・非目標の正本は `.concept/charter.yml`。本書はその見直し記録と現在地の観測であり、現状・AC・作業一覧の正本を増やさない。実行波の正本は [milestones.md](milestones.md)。

## 目的と変更してはいけない条件

- 目的: charter `product_goal.north_star` — モジュラーなノードグラフ型 AI コンテンツ生成エンジンとして、上流に自動追従しない恒久自律開発で安定提供する ComfyUI fork であり続ける（推定）
- 最終的な成果と判定範囲: MET-001（`make test` 0 failed 維持）、MET-002（Woodpecker の Ruff + tests-unit が green）。判定はリポ内テストと CI gate。
- 保護制約・資源・権限: AGENTS.md（No Internet Requests、最小変更、互換シム削除）、LOOP.md の禁止事項（push/履歴改変/deploy/外部送信/対象外リポ編集の禁止）、AUTOMATION.md（上流取り込みは所有者の明示指示時のみ）。権限の出典は TAS dispatch の task packet。
- 他担当/外部システムとの責務境界: TAS が driver/dispatch/着地、Woodpecker が CI gate、所有者が upstream merge と driver 変更を担当。upstream (Comfy-Org/ComfyUI) は読み取り対象のみ。

## 全体構造と現在地

|実際の経路/責務|コード・契約|実装/受入/運転の状態|証拠と観測日|残る原因|
|---|---|---|---|---|
|ノードグラフ実行エンジン|comfy/, comfy_execution/, execution.py, server.py, nodes.py|実装あり（上流継承、fork 固有は局所修正。現候補の実機運転は未観測）|docs/llm-wiki/index.md（git log 実測、2026-09-26 時点で fork 固有 20 commits）|fork 固有修正の upstream 追従は所有者指示時のみ（非ゴール領域）|
|fork 基盤（Makefile/CI gate）|Makefile, .woodpecker.yml, AUTOMATION.md|履歴上の受入済み・最新稼働は未観測|charter MS-001 status: done。AUTOMATION.md（2026-09-27 時点で TAS timer 有効・Woodpecker 有効・GitHub Actions 無効）|なし（維持）|
|アセット永続化|app/assets/database/, alembic_db/|実装済み（main）。受入証拠は未取得|WP-A1/WP-A2 の成果（6d8fbffd / ae41a228）は未着地ブランチにのみ存在し、main の alembic_db/README.md は 4 行のまま。models.py に 6 テーブル、versions 0001..0008（2026-11-11 再観測）|WP-A1/WP-A2 の成果が default へ着地していない（着地で解消方針）。着地まで MS-002 は active のまま|
|.concept 同期|.concept/（charter.yml, autopilot.yml, ontology_budget.yml の 3 ファイル）|受入済み（WP-C1 は 2026-11-03 の eadbeeeb で main 着地）|820d2ae4 (#43) で runtime metadata を非追跡化、charter MS-003 の deliverables を現構成へ修正。追跡3ファイル / yaml parse 3/3 OK / runtime 12 ファイルの check-ignore 12/12 / ガードテスト tests-unit/concept_metadata_tracking_test.py（2026-11-11 再観測）|MS-003 の残は WP-C2（MET-001 の再観測）|
|自律改善ループ|LOOP.md（loop-md:spec v4、管理印付き。2026-11-10 観測 @ b3aed15a、基準時点 2026-10-21 は v2）|契約定義済み（TAS dispatch の 1 run = 1 改善。定義だけでは運転実績にならない）|LOOP.md 本体|LOOP の候補順位と本計画の残課題が未接続（接続評価の再計画案も未着地ブランチのみで main 未反映）|

## 優先順・依存・出口条件・次の一手

優先順・出口条件・受入条件の正本は charter（[.concept/charter.yml](../../.concept/charter.yml)）で、本書は参照と現在地のみを保持する（重複管理しない）。

|MS|優先順（charter priority が正本）|依存|出口条件（charter exit_criteria への参照）|次の一手|
|---|---|---|---|---|
|MS-001|P0|なし|`make test` 0 failed と Woodpecker gate green を維持（charter exit_criteria 2 項）|維持のみ。新規の成果を追加しない|
|MS-002|P1|WP-A1 → WP-A2|a) 隔離した一時 DB で `alembic upgrade head` が exit 0、b) README の手順が versions 0001..0008 と一致、c) `make test` が同一候補で 0 failed（charter exit_criteria 3 項）|WP-A1/WP-A2 の成果の default 着地を確認。未着地の間は active を維持|
|MS-003|P2|なし（WP-C2 は WP-C1 と独立）|a) `.concept/*.yml` の yaml parse 成功、b) 追跡3ファイルと runtime 12 ファイルの check-ignore（charter exit_criteria 2 項）|WP-C2: `make test` を1回だけ実測して MET-001 の記載を更新（約30分）|

直近の一手（全体）: WP-C2（`make test` を1回だけ走らせ passed/failed/skipped と対象 SHA を記録し、charter MET-001 の実測値を更新する、約30分）。実行手順は [milestones.md](milestones.md) の WP-C2 カード、MS-### 形式の分解と各項目の状態は [docs/MILESTONES.md](../MILESTONES.md)。

## 以前の計画から変える判断

|以前の前提・順序|最新の事実|維持/変更/後回し/終了|理由・影響先|
|---|---|---|---|
|MS-003 は「固定 14 ファイル構成」と ontology/invariants/mappings の保守|820d2ae4 (#43) で生成物 12 ファイルを Git 追跡から除外し、追跡は 3 ファイルになった|変更（WP-C1 は 2026-11-03 の eadbeeeb で main 着地、2026-11-11 再観測で乖離解消を確認）|charter MS-003 の deliverables を現構成へ修正済み。残は WP-C2|
|MET-001 の実測 1930 passed / 0 failed / 74 skipped（2026-10-10）|基準 commit 以降も更新が継続（2026-10-01 以降 21 commits）。現値は未観測|維持（観測時点の記録として保存）|本値を現在値として転記しない。同一候補・条件の既存 CI 証拠を先に確認し、足りない場合だけ WP-C2 で観測する|
|MS-002 を active として継続|中核成果物（6 テーブル・マイグレーション 0001..0008）は実装済み。WP-A1/WP-A2 の実走・文書整合の成果は未着地ブランチ（6d8fbffd / ae41a228）にのみ存在し、main には未着地|維持（active のまま。着地確認まで status を据え置く）|WP-A1 / WP-A2 の default 着地確認。着地前に done としない|
|進行中 PR（#42 #41 #35 #33 #31、2026-10-12〜15 に open）|他担当 run 由来の tas/auto ブランチ。2026-11-11 時点で、計画・受入証拠に関する未着地の成果（6d8fbffd / 886ec49a / ae41a228、origin/tas/auto/...-tree-6dc74f46 の docs 群）は main に反映されていない|後回し|本計画では内容を複製せず、着地後の再評価のみ。重複発行しない|

古い成功・失敗はその候補/条件の記録として保持する。現在の仕様・実績へ付け替えない。

## 到達状態から逆算した段階

|段階|利用者が得る成果|必要な証拠|未達原因・依存|次の実行波に進む条件|
|---|---|---|---|---|
|S1 受入証拠の確定|MS-002 / MS-003 の status が証拠付きで確定する|`make test` 実測、alembic upgrade head の成功記録、README 実態一致の判定、charter 更新 commit|WP-C1 は 2026-11-03 に着地済。WP-A1 / WP-A2 の成果は未着地ブランチにのみ存在し、WP-C2 は未実施（WP-A2 は WP-A1 に依存、同じ charter の最終編集は直列化）|現在波の AC 充足 + charter 更新の実際の default 着地。観測不能・失敗・未着地は未完了|
|S2 継続運転の安定|LOOP の候補選択が plan の残課題を拾う|LOOP run の最終出力に plan 由来候補の記録|S1 完了後に評価（再計画案も未着地ブランチにのみ存在）|次の実行波で WP 再計画を行う|
|S3 上流追従の準備|所有者指示時に upstream merge を安全に実行できる状態|merge リハーサルの記録|所有者の明示指示が前提（自動追従は非ゴール）|指示到着時に分割する|

現在の実行波は [milestones.md](milestones.md) に約30分単位で定義する。
遠い段階の実装詳細は、入力・必要性が確定した時に分割する。
目的・保護条件以外の計画を変えるときは理由、影響する依存、再検証範囲を残す。

<!-- END: GENERATED -->
<!-- BEGIN: HUMAN -->
手動追記（2026-11-03）: 本書の「全体構造と現在地」が現状との差、「到達状態から逆算した段階」が到達点・依存・出口条件の正本。MS-### 形式の実行用分解と次の一手は [docs/MILESTONES.md](../MILESTONES.md)、目標・マイルストーンの正本は [`.concept/charter.yml`](../../.concept/charter.yml)。
手動追記（2026-11-11）: OI-20261111-12 の計画整備として、main で再観測した事実（追跡 .concept 3 ファイル / yaml parse 3/3 OK / runtime 12 ファイルの check-ignore 12/12 / alembic versions 0001..0008 / main の alembic_db/README.md は 4 行）を現状に反映し、「優先順・依存・出口条件・次の一手」の節を追加した。MS-003 の乖離（旧「固定 14 ファイル構成」記載）は WP-C1 で解消済み、MS-002 の受入証拠（WP-A1/WP-A2）は未着地ブランチにのみ存在するため charter MS-002 は active のまま据え置いた。状態の変更は行っていない。
<!-- END: HUMAN -->
