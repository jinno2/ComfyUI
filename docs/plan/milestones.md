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

独立して進められる作業: WP-A1 の実走と WP-C1/C2 の読み取り調査は独立。ただし WP-A2/C1/C2 は同じ charter.yml を変更するため、反映は最新候補を確認して直列化する。異なる行でも同時編集を安全とは見なさない。
4枠×約30分は標準枠の単純和。外部待ち・追加修正・実走超過は別で、暦時間保証や大ゴールの残工数ではない。

## 作業カード

### WP-A1 | alembic マイグレーション連鎖の受入確認（約30分）

- **主旨**: MS-002 の中核（0001..0008 の連鎖）が実環境で動くことの証拠を作る。実装済みと実証待ちを分ける境界。
- **ゴール・成果物**: マイグレーション連鎖の実行記録（コマンド・exit code・`alembic heads` 出力）1件。
- **入力・対象**: alembic_db/（0001_assets.py .. 0008_missing_content_age.py）、app/assets/database/models.py の 6 テーブル。既存の venv と Makefile の install 済み環境を使う。
- **作業**: 一時 DB ファイルに対し `alembic upgrade head` を実行し、`alembic heads` / `alembic current` を確認する。新規依存・コード変更はしない。
- **完了条件（事前AC）**: 隔離した一時 DB だけを対象に upgrade head が exit 0 で完了し、alembic current が単一 head と一致することを確認する。本番・既存 DB の設定を継承しない。
- **必要検証・証拠**: 実行ログ（コマンドと exit）。raw ログは既存 run の永続証拠へ残し、計画 MD には再取得可能な run ID・保存先参照のみ。最終出力だけを永続保存と仮定しない。
- **依存・着手条件**: なし。alembic がインストールされた環境（`make install` 済み）で実行。
- **担当・変更範囲**: リポへの書き込みなし（観測 WP）。実行環境は Dot のセッション。
- **待ち・失敗・再開**: 環境不足で実行不能なら waiting にし、不足内容を報告して WP-C1/C2 へ進む。失敗した連鎖はスタック全文を証拠に残す。
- **条件付き不要の判定**: alembic 実行環境がホストに構築不能な場合、本 WP は waiting（証拠収集不能）とし、必要環境・解除条件を残す。WP-A2 は未解消の調査記録を作れるが、MS-002 の AC は未達のまま。

### WP-A2 | CFLT-ASSETPERSIST-001 解消判定と charter MS-002 更新（約30分）

- **主旨**: charter の MS-002 deliverables「alembic_db/README.md の実態一致（CFLT-ASSETPERSIST-001 の解消）」を証拠付きで判定し、active 維持か done かを確定させる。
- **ゴール・成果物**: charter MS-002 の status/acceptance 更新（1 commit）。
- **入力・対象**: .concept/charter.yml、alembic_db/README.md、WP-A1 の実行記録。
- **作業**: README の手順（models.py 更新 → `alembic revision --autogenerate`）と versions 実態（0001..0008）の一致を判定表にする。README の文書整合だけで done にしない。WP-A1 成功に加え MS-002 の既存 acceptance（make test）を同一候補の有効な証拠で満たした場合のみ done とし、未解消なら active のまま原因と解除条件を残す。
- **完了条件（事前AC）**: 判定と根拠を記録し、成功時は実際の default 着地まで確認する。失敗・観測不能を記録しただけでは MS-002 や受入確認 WP の完了にならない。
- **必要検証・証拠**: charter.yml の yaml parse 成功 + git diff の確認。
- **依存・着手条件**: WP-A1 の実行記録（失敗・不能なら未解消の診断だけ可能。受入完了には成功証拠が必要）。
- **担当・変更範囲**: .concept/charter.yml の MS-002 部分のみ。
- **待ち・失敗・再開**: WP-A1 waiting 中は本 WP も waiting。解除条件は WP-A1 の証拠確定。
- **条件付き不要の判定**: なし（本波の中核判定）。

### WP-C1 | charter MS-003 を現 .concept 構成へ整合（約30分）

- **主旨**: 820d2ae4 (#43) 後の追跡 3 ファイル構成（charter.yml, autopilot.yml, ontology_budget.yml）に charter MS-003 の deliverables を合わせ、正本の乖離を解消する。
- **ゴール・成果物**: charter MS-003 deliverables の修正（1 commit）。
- **入力・対象**: .concept/charter.yml、.concept/ の実ファイル一覧、820d2ae4 の変更内容、tests-unit/concept_metadata_tracking_test.py。
- **作業**: 「固定 14 ファイル構成」「ontology/invariants/mappings の保守」を現構成（手管理 3 ファイル + 生成物の非追跡ガード）に書き換える。MS-003 の status は証拠（820d2ae4 とガードテスト）を参照して確定する。
- **完了条件（事前AC）**: charter の追跡対象記載と `git ls-files .concept` が一致する。ディスク上の非追跡 runtime 生成物の存在は追跡構成に数えない。
- **必要検証・証拠**: charter.yml の yaml parse + git diff。
- **依存・着手条件**: なし。
- **担当・変更範囲**: .concept/charter.yml の MS-003 部分のみ。
- **待ち・失敗・再開**: WP-A2 と同じファイルを触るため、行が異なっても最終反映を直列化し、最新候補と競合を確認する。
- **条件付き不要の判定**: なし。

### WP-C2 | make test 再観測と MET-001 観測の更新（約30分）

- **主旨**: MET-001 の記録が 2026-10-10 のままであるため、現時点の実測を取り charter の観測を更新する。古い実測値を現在値として転記しないための再観測。
- **ゴール・成果物**: `make test` の実測記録と charter MET-001 の更新（1 commit、または失敗時は LOOP 候補の記録）。
- **入力・対象**: tests-unit/ 全体、Makefile の test ターゲット。
- **作業**: まず同一候補・実行条件・範囲を満たす成功 CI 証拠を再利用する。不足する場合だけ `make test` を 1 回実行し、passed/failed/skipped と対象 SHA を記録する。0 failed なら charter MET-001 の実測と観測日を 実際の観測日時・対象 SHA の値へ更新する。失敗があるなら charter は触らず、失敗 1 件を LOOP.md の優先候補として run の最終出力に記録する（本波で修復しない）。
- **完了条件（事前AC）**: 必要な範囲の成功実測と charter の更新が実際に default へ着地している。失敗の引継ぎは有用な中間成果だが、本 AC や M-C の完了にはしない。
- **必要検証・証拠**: テスト実行のサマリ行。
- **依存・着手条件**: なし。実行環境（make install 済み venv）が必要。
- **担当・変更範囲**: .concept/charter.yml の MET-001 部分（成功時のみ）。テストコードは触らない。
- **待ち・失敗・再開**: 実走が 30 分を超える場合は起動と結果回収を別 run に分け、結果未取得の間は waiting。
- **条件付き不要の判定**: 実行環境が構築不能な場合はwaiting（観測不能）とし、必要環境・解除条件を記録する。charter の観測日は実際の既存観測日のまま維持する（欠測を 0 で埋めない）。

## 完了と再計画

- 1WPは1振る舞い・1課題・1境界。設計が成果のWPを除き、設計だけで実装をdoneにしない。
- pending/ready/in_progress/waiting/done/not_neededを区別する。doneにはACと必要な配達ゲートが要る。
- 長い実走は起動と結果回収を分け、結果未取得はwaiting。完了taskと有効証拠を再利用する。
- 条件付き前段がnot_neededの場合の後段経路: WP-A1 が証拠収集不能なら waiting。WP-A2 は未解消の診断を記録できるが、受入ゲートを閉じない。他の WP に波及しない。
- 同条件比較が必要な場合の対照取得・判定WP: なし（本波に比較 AC はない）。
- 実行時刻・commit/hash・PR・run・backend等は実行元から取得する。欠測を0で埋めない。
- runtime進捗とraw証拠は 既存の run 最終出力と git commit/PR に置く（新しい台帳・進捗ファイルを作らない）。
- 追加修正片は親WPに束縛し、目的・成果・AC・依存を保つ。無関係なbacklogを増やさない。
- 目的・資源・保護制約を守り、計画変更の理由と影響する再検証を残す。
- 現在の実行波の終了条件: M-A と M-C の全 WP（4件）の AC を満たし、必要な更新が実際の default へ着地したこと。waiting・失敗・PR 引継ぎだけを完了にしない。完了後に S2（LOOP 接続の評価）を次の波候補として再計画する。

<!-- END: GENERATED -->
<!-- BEGIN: HUMAN -->
<!-- END: HUMAN -->
