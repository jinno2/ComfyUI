# ComfyUI fork — マイルストーンと小作業

<!-- BEGIN: GENERATED -->

計画基準: 2026-10-21 13:05 WAT / 4c0788db9379bfe8013093b8339436b0175622c4。
長期方針: [.concept/charter.yml](../../.concept/charter.yml)（見直し記録は [long-term-direction.md](long-term-direction.md)）。実装・受入正本: AGENTS.md、LOOP.md、app/assets/database/、alembic_db/。
専任ワーカー: [dot-worker.md](dot-worker.md)。
状態はこの基準時点の観測であり、実行時にmain/PR/runから再確認する。

## 構造と実行する範囲

実行経路と責務の対応は long-term-direction.md の「全体構造と現在地」が正。本波は charter MS-002（Asset persistence layer integrity）と MS-003（Concept synchronization）の受入証拠確定に限定する。fork 基盤（MS-001）は done なので触らない。他担当の進行中 PR（#42 #41 #35 #33 #31）の範囲には着手しない。

## マイルストーン

|ID|利用者が得る能力・成果|対象WP|完了ゲート|標準作業枠|
|---|---|---|---|---|
|M-A|MS-002 の受入状態が証拠付きで確定する（実装済み/実証待ちの区別が charter に反映）|WP-A1, WP-A2|charter MS-002 が証拠参照付きで status 更新されている|2枠|
|M-C|charter の記載が現実（.concept 構成・テスト実測）と一致する|WP-C1, WP-C2|charter の MS-003 deliverables と MET-001 観測が 2026-10-21 時点の実測と一致|2枠|

依存: WP-A1 → WP-A2 のみ。WP-C1 と WP-C2 は独立。M-A 系と M-C 系は相互に並行進行できる。

独立して進められる作業: WP-A1 / WP-C1 / WP-C2 は互いにファイル競合しない（WP-A2 だけ charter を WP-A1 の証拠付きで書く）。charter.yml への書き込みは WP-A2 と WP-C1/C2 で行が分かれるため、同一 run で複数 WP を消化する場合は charter への commit を WP 単位で分ける。
4枠×約30分は標準枠の単純和。外部待ち・追加修正・実走超過は別で、暦時間保証や大ゴールの残工数ではない。

## 作業カード

### WP-A1 | alembic マイグレーション連鎖の受入確認（約30分）

- **主旨**: MS-002 の中核（0001..0008 の連鎖）が実環境で動くことの証拠を作る。実装済みと実証待ちを分ける境界。
- **ゴール・成果物**: マイグレーション連鎖の実行記録（コマンド・exit code・`alembic heads` 出力）1件。
- **入力・対象**: alembic_db/（0001_assets.py .. 0008_missing_content_age.py）、app/assets/database/models.py の 6 テーブル。既存の venv と Makefile の install 済み環境を使う。
- **作業**: 一時 DB ファイルに対し `alembic upgrade head` を実行し、`alembic heads` / `alembic current` を確認する。新規依存・コード変更はしない。
- **完了条件（事前AC）**: upgrade head が exit 0 で完了し、単一 head であることが出力で確認できる。
- **必要検証・証拠**: 実行ログ（コマンドと exit）。raw ログは run の最終出力に残し、計画 MD には参照のみ。
- **依存・着手条件**: なし。alembic がインストールされた環境（`make install` 済み）で実行。
- **担当・変更範囲**: リポへの書き込みなし（観測 WP）。実行環境は Dot のセッション。
- **待ち・失敗・再開**: 環境不足で実行不能なら waiting にし、不足内容を報告して WP-C1/C2 へ進む。失敗した連鎖はスタック全文を証拠に残す。
- **条件付き不要の判定**: alembic 実行環境がホストに構築不能な場合、本 WP は「証拠収集不能」として閉じ、WP-A2 は未解消を記録して終了する（永久 ready にしない）。

### WP-A2 | CFLT-ASSETPERSIST-001 解消判定と charter MS-002 更新（約30分）

- **主旨**: charter の MS-002 deliverables「alembic_db/README.md の実態一致（CFLT-ASSETPERSIST-001 の解消）」を証拠付きで判定し、active 維持か done かを確定させる。
- **ゴール・成果物**: charter MS-002 の status/acceptance 更新（1 commit）。
- **入力・対象**: .concept/charter.yml、alembic_db/README.md、WP-A1 の実行記録。
- **作業**: README の手順（models.py 更新 → `alembic revision --autogenerate`）と versions 実態（0001..0008）の一致を判定表にする。解消と判定できたら charter MS-002 を証拠参照付きで done へ、未解消なら残る原因を deliverables に 1 行で追記する。
- **完了条件（事前AC）**: charter MS-002 の status と根拠が 1 commit で更新され、判定表が run の最終出力に残る。
- **必要検証・証拠**: charter.yml の yaml parse 成功 + git diff の確認。
- **依存・着手条件**: WP-A1 の実行記録（成功・失敗・不能のいずれでも可）。
- **担当・変更範囲**: .concept/charter.yml の MS-002 部分のみ。
- **待ち・失敗・再開**: WP-A1 waiting 中は本 WP も waiting。解除条件は WP-A1 の証拠確定。
- **条件付き不要の判定**: なし（本波の中核判定）。

### WP-C1 | charter MS-003 を現 .concept 構成へ整合（約30分）

- **主旨**: 820d2ae4 (#43) 後の追跡 3 ファイル構成（charter.yml, autopilot.yml, ontology_budget.yml）に charter MS-003 の deliverables を合わせ、正本の乖離を解消する。
- **ゴール・成果物**: charter MS-003 deliverables の修正（1 commit）。
- **入力・対象**: .concept/charter.yml、.concept/ の実ファイル一覧、820d2ae4 の変更内容、tests-unit/concept_metadata_tracking_test.py。
- **作業**: 「固定 14 ファイル構成」「ontology/invariants/mappings の保守」を現構成（手管理 3 ファイル + 生成物の非追跡ガード）に書き換える。MS-003 の status は証拠（820d2ae4 とガードテスト）を参照して確定する。
- **完了条件（事前AC）**: charter の記載と `ls .concept/` が一致し、乖離の記述が残らない。
- **必要検証・証拠**: charter.yml の yaml parse + git diff。
- **依存・着手条件**: なし。
- **担当・変更範囲**: .concept/charter.yml の MS-003 部分のみ。
- **待ち・失敗・再開**: WP-A2 と同じファイルを触るため、同一 run で消化する場合は commit を WP 単位で分離する。
- **条件付き不要の判定**: なし。

### WP-C2 | make test 再観測と MET-001 観測の更新（約30分）

- **主旨**: MET-001 の記録が 2026-10-10 のままであるため、現時点の実測を取り charter の観測を更新する。古い実測値を現在値として転記しないための再観測。
- **ゴール・成果物**: `make test` の実測記録と charter MET-001 の更新（1 commit、または失敗時は LOOP 候補の記録）。
- **入力・対象**: tests-unit/ 全体、Makefile の test ターゲット。
- **作業**: `make test` を 1 回実行し、passed/failed/skipped を記録する。0 failed なら charter MET-001 の実測と観測日を 2026-10-21 の値へ更新する。失敗があるなら charter は触らず、失敗 1 件を LOOP.md の優先候補として run の最終出力に記録する（本波で修復しない）。
- **完了条件（事前AC）**: 実測値が記録され、charter が現実と一致するか、失敗が LOOP 候補として引き継がれている。
- **必要検証・証拠**: テスト実行のサマリ行。
- **依存・着手条件**: なし。実行環境（make install 済み venv）が必要。
- **担当・変更範囲**: .concept/charter.yml の MET-001 部分（成功時のみ）。テストコードは触らない。
- **待ち・失敗・再開**: 実走が 30 分を超える場合は起動と結果回収を別 run に分け、結果未取得の間は waiting。
- **条件付き不要の判定**: 実行環境が構築不能な場合は「観測不能」として閉じ、charter の観測日を 2026-10-10 のまま維持する（欠測を 0 で埋めない）。

## 完了と再計画

- 1WPは1振る舞い・1課題・1境界。設計が成果のWPを除き、設計だけで実装をdoneにしない。
- pending/ready/in_progress/waiting/done/not_neededを区別する。doneにはACと必要な配達ゲートが要る。
- 長い実走は起動と結果回収を分け、結果未取得はwaiting。完了taskと有効証拠を再利用する。
- 条件付き前段がnot_neededの場合の後段経路: WP-A1 が「証拠収集不能」で閉じた場合、WP-A2 は未解消の判定を記録して閉じる。他の WP に波及しない。
- 同条件比較が必要な場合の対照取得・判定WP: なし（本波に比較 AC はない）。
- 実行時刻・commit/hash・PR・run・backend等は実行元から取得する。欠測を0で埋めない。
- runtime進捗とraw証拠は 既存の run 最終出力と git commit/PR に置く（新しい台帳・進捗ファイルを作らない）。
- 追加修正片は親WPに束縛し、目的・成果・AC・依存を保つ。無関係なbacklogを増やさない。
- 目的・資源・保護制約を守り、計画変更の理由と影響する再検証を残す。
- 現在の実行波の終了条件: M-A と M-C の全 WP（4件）が done または not_needed（根拠付き）で確定し、charter 更新 commit が TAS 着地経路に渡っていること。完了後に S2（LOOP 接続の評価）を次の波候補として再計画する。

<!-- END: GENERATED -->
<!-- BEGIN: HUMAN -->
<!-- END: HUMAN -->
