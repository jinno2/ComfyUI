# ComfyUI — マイルストーン実行分解

この文書は[長期計画の正本](../.concept/charter.yml)を実行可能な段階へ分解する投影です。長期方向と出口条件は[見直し記録](plan/long-term-direction.md)、実行手順は[Dot worker](plan/dot-worker.md)、概念マイルストーンのID・目的・優先度は charter を正本とし、ここでは受入条件と現在の実行波を管理します。

既存の実行波グループID `M-A` / `M-C` と作業ID `WP-A1` / `WP-A2` / `WP-C1` / `WP-C2` を維持します。charter の `done` は過去の状態記録として保護し、過去の達成記録と現候補の受入run証拠を区別します。作業未着手は `planned`、受入確認中は `verifying` とします。

Plan-Status: in_progress

## MS-001: Fork infrastructure stability
Outcome: ComfyUI fork の Makefile、クロスプラットフォーム対応、Woodpecker gate が維持され、テストと CI の受入が証拠で確認できる。
Acceptance: `make test` が exit 0 で、同一候補の Woodpecker が Ruff と tests-unit の両方で green であることを run 記録で確認する。
Evidence: charter は status=done と記録しているが、同一候補のテスト・CI run 記録はこの checkout で未確認（pending）。
Status: verifying
優先度: P0。依存: なし。
次の作業: WP-V1 で利用可能な同一候補の既存 CI 証拠を確認し、再利用できなければ認可された実行環境で `make test` を1回実行して不足を特定する。

## MS-002: Asset persistence layer integrity
Outcome: `app/assets/database` の6テーブル、alembic migration 0001..0008、および README の手順が一致し、スキーマ変更を再現できる。
Acceptance: 隔離した一時DBで `alembic upgrade head` が exit 0、`alembic current` が単一の `alembic heads` と一致し、同一候補の `make test` が0 failedである。README と実ファイルの対応も判定する。
Evidence: 6テーブルと migration 0001..0008 は確認済み。実走および同一候補の test 結果は pending。
Status: planned
優先度: P1。依存: WP-A2 は WP-A1 の実行記録に依存する。
次の作業: WP-A1 で一時DBの migration 連鎖を約30分で確認する。

## MS-003: Concept synchronization
Outcome: 手管理する `.concept` の3ファイルと、runtime 生成物の非追跡ガードが現状と一致し、概念同期の記載が実装可能である。
Acceptance: `git ls-files .concept` が `charter.yml`、`autopilot.yml`、`ontology_budget.yml` の3ファイルを返し、`tests-unit/concept_metadata_tracking_test.py` が通る。charter の deliverables がこの構成と一致する。
Evidence: 2026-10-22 に `git ls-files .concept` が3ファイルを返し、tracking guard test の存在を確認。テスト実行と charter の記載整合は pending。
Status: in_progress
優先度: P2。依存: なし。
次の作業: WP-C1 で追跡対象と charter deliverables を照合する。

## 現在の実行波

実行波グループ `M-A` は MS-002（WP-A1 → WP-A2）、`M-C` は MS-003（WP-C1、WP-C2）に対応します。WP-A1 と WP-C1/C2 の調査は独立です。WP-A2/C1/C2 は同じ `.concept/charter.yml` を編集するため、最新状態を見て反映を直列化します。M-A と M-C は並行可能です。4枠×約30分は標準作業枠の単純和で、暦時間保証ではありません。

### M-A | MS-002 受入状態の確定（既存グループID）
成果: MS-002 の実装済み部分と受入未確認部分が分かれ、証拠付きの状態が charter に反映される。
完了ゲート: WP-A1 の隔離 migration 証拠と README/現状の判定をそろえ、適用条件を満たす場合のみ charter の MS-002 を更新する。
既存根拠: WP-A1/WP-A2 と2枠見積もりを維持。実走証拠は pending。
現在状態: planned
依存: WP-A2 は WP-A1 に依存する。
次の作業: WP-A1。

### M-C | MS-003 記載と現状の整合（既存グループID）
成果: `.concept` の現構成と MET-001 観測が charter に正しく表現される。
完了ゲート: WP-C1 の追跡対象照合と、WP-C2 の同一候補 test 観測がそろった場合だけ該当する charter 部分を更新する。
既存根拠: WP-C1/WP-C2 と2枠見積もりを維持。charter 更新証拠は pending。
現在状態: planned
依存: WP-C1/C2 は M-A 系と独立して進められるが、同じ charter 編集時は直列化する。
次の作業: WP-C1 と WP-C2 の証拠をそれぞれ回収する。

### WP-V1 | MS-001 の既存受入証拠確認（約30分）

- **主旨**: charter に残る `done` と最新の実テスト・CI 状態の対応を証拠で確認する。
- **作業**: 同一候補・実行条件・範囲の Woodpecker 成功記録を再利用する。不足時のみ利用可能な認可済み環境で `make test` を1回実行し、対象 SHA と passed/failed/skipped を記録する。再実行できない場合は不足する証拠を明示し、MS-001 を verifying に保つ。
- **完了条件**: `make test` 0 failed と Woodpecker Ruff + tests-unit green を同一候補の記録で確認する。記録のない推測や charter の `done`、commit/PR の存在のみでは achieved にしない。
- **範囲**: 読み取り中心。テスト実行は同一候補の成功証拠が見つからない場合に限る。コード変更なし。

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
- 現在の実行波の終了条件: WP-V1 と M-A / M-C の全 WP（計5件）の AC を満たし、必要な更新が実際の default へ着地したこと。waiting・失敗・PR 引継ぎだけを完了にしない。完了後に S2（LOOP 接続の評価）を次の波候補として再計画する。

<!-- END: GENERATED -->
<!-- BEGIN: HUMAN -->
<!-- END: HUMAN -->
