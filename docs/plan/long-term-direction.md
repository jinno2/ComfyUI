# ComfyUI fork — 長期方針の見直し

<!-- BEGIN: GENERATED -->

計画確認日: 2026-10-22。基準候補: jinno2/ComfyUI @ 465db8bf811749f978be9489f9a75b91fac5e26b。
文書の役割: ゴール・マイルストーン・非目標の正本は `.concept/charter.yml`。本書はその見直し記録と現在地の観測であり、現状・AC・作業一覧の正本を増やさない。実行分解と受入証拠の正本は [docs/MILESTONES.md](../MILESTONES.md)。

## 目的と変更してはいけない条件

- 目的: charter `product_goal.north_star` — モジュラーなノードグラフ型 AI コンテンツ生成エンジンとして、上流に自動追従しない恒久自律開発で安定提供する ComfyUI fork であり続ける（推定）
- 最終的な成果と判定範囲: MET-001（`make test` 0 failed 維持）、MET-002（Woodpecker の Ruff + tests-unit が green）。判定はリポ内テストと CI gate。
- 保護制約・資源・権限: AGENTS.md（No Internet Requests、最小変更、互換シム削除）、LOOP.md の禁止事項（push/履歴改変/deploy/外部送信/対象外リポ編集の禁止）、AUTOMATION.md（上流取り込みは所有者の明示指示時のみ）。権限の出典は TAS dispatch の task packet。
- 他担当/外部システムとの責務境界: TAS が driver/dispatch/着地、Woodpecker が CI gate、所有者が upstream merge と driver 変更を担当。upstream (Comfy-Org/ComfyUI) は読み取り対象のみ。

## 全体構造と現在地

|実際の経路/責務|コード・契約|実装/受入/運転の状態|証拠と観測日|残る原因|
|---|---|---|---|---|
|ノードグラフ実行エンジン|comfy/, comfy_execution/, execution.py, server.py, nodes.py|実装あり（上流継承、fork 固有は局所修正。現候補の実機運転は未観測）|docs/llm-wiki/index.md（git log 実測、2026-09-26 時点で fork 固有 20 commits）|fork 固有修正の upstream 追従は所有者指示時のみ（非ゴール領域）|
|fork 基盤（Makefile/CI gate）|Makefile, .woodpecker.yml, AUTOMATION.md|履歴上の受入済み・最新稼働は未観測|charter MS-001 status: done（同一候補の受入 run 記録は未確認のため、現計画では verifying）。AUTOMATION.md（2026-09-27 時点で TAS timer 有効・Woodpecker 有効・GitHub Actions 無効）|なし（維持）|
|アセット永続化|app/assets/database/, alembic_db/|実装済み・受入証拠待ち|models.py に 6 テーブル、versions 0001..0008（2026-10-21 観測）|README 実態一致と CFLT-ASSETPERSIST-001 解消の証拠が記録に残っていない|
|.concept 同期|.concept/（charter.yml, autopilot.yml, ontology_budget.yml の 3 ファイル）|限定受入|820d2ae4 (#43) で runtime metadata を非追跡化、ガードテスト tests-unit/concept_metadata_tracking_test.py 追加（2026-10-15 前後）|charter MS-003 の「固定 14 ファイル構成」記載が現構成と乖離|
|自律改善ループ|LOOP.md（loop-md:spec v2、管理印付き）|契約定義済み（TAS dispatch の 1 run = 1 改善。定義だけでは運転実績にならない）|LOOP.md 本体|LOOP の候補順位と本計画の残課題が未接続|

## 以前の計画から変える判断

|以前の前提・順序|最新の事実|維持/変更/後回し/終了|理由・影響先|
|---|---|---|---|
|MS-003 は「固定 14 ファイル構成」と ontology/invariants/mappings の保守|820d2ae4 (#43) で生成物 12 ファイルを Git 追跡から除外し、追跡は 3 ファイルになった|変更|charter MS-003 の deliverables を現構成へ修正する（WP-C1）|
|MET-001 の実測 1930 passed / 0 failed / 74 skipped（2026-10-10）|基準 commit 以降も更新が継続（2026-10-01 以降 21 commits）。現値は未観測|維持（観測時点の記録として保存）|本値を現在値として転記しない。同一候補・条件の既存 CI 証拠を先に確認し、足りない場合だけ WP-C2 で観測する|
|MS-002 を active として継続|中核成果物（6 テーブル・マイグレーション 0001..0008）は実装済み。残るのは受入証拠と文書整合|変更（実装追加入口から受入証拠確定へ寄せる）|WP-A1 / WP-A2|
|進行中 PR（#42 #41 #35 #33 #31、2026-10-12〜15 に open）|他担当 run 由来の tas/auto ブランチ|後回し|本計画では内容を複製せず、着地後の再評価のみ。重複発行しない|

古い成功・失敗はその候補/条件の記録として保持する。現在の仕様・実績へ付け替えない。

## 到達状態から逆算した段階

|段階|利用者が得る成果|必要な証拠|未達原因・依存|次の実行波に進む条件|
|---|---|---|---|---|
|S1 受入証拠の確定|MS-001 の過去の done 記録と現候補の test/CI 証拠を照合し、MS-002 / MS-003 の status も証拠付きで確定する|`make test` と Woodpecker の同一候補記録、alembic upgrade head の成功記録、README 実態一致の判定、charter 更新 commit|WP-V1 / WP-A1 / WP-A2 / WP-C1 / WP-C2（WP-A2 は WP-A1 に依存、同じ charter の最終編集は直列化）|全WPの AC 充足 + charter 更新の実際の default 着地。観測不能・失敗は未完了|
|S2 継続運転の安定|LOOP の候補選択が plan の残課題を拾う|LOOP run の最終出力に plan 由来候補の記録|S1 完了後に評価|次の実行波で WP 再計画を行う|
|S3 上流追従の準備|所有者指示時に upstream merge を安全に実行できる状態|merge リハーサルの記録|所有者の明示指示が前提（自動追従は非ゴール）|指示到着時に分割する|

現在の実行波は [docs/MILESTONES.md](../MILESTONES.md) に約30分単位で定義する。
遠い段階の実装詳細は、入力・必要性が確定した時に分割する。
目的・保護条件以外の計画を変えるときは理由、影響する依存、再検証範囲を残す。

<!-- END: GENERATED -->
<!-- BEGIN: HUMAN -->
<!-- END: HUMAN -->
