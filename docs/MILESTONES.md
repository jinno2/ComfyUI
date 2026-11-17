# Milestones — ComfyUI fork（実行用分解）

Plan-Status: in_progress

正本: [.concept/charter.yml](../.concept/charter.yml)（目的・非目標・成功指標・マイルストーンの定義）
長期方針の見直し記録と現在地: [docs/plan/long-term-direction.md](plan/long-term-direction.md)
現行の実行波（約30分の作業枠とWPカード）: [docs/plan/milestones.md](plan/milestones.md)

本書は charter のマイルストーンを実行可能な単位へ分解した索引であり、定義と正本状態は charter 側にある（charter の `done` / `active` は本書の `achieved` / `in_progress` と同義）。WP カードの実装手順・依存表は `docs/plan/milestones.md` が保持し、本書では重複して保持しない。各項目は charter の同一 ID（MS-001..MS-003）を引き継ぐ。

## 継続更新の回路

- 目標・マイルストーンを変更するときは charter を更新し、本書と `docs/plan/milestones.md` の参照を整合させる。
- `REPO_METADATA.json` は charter と `docs/plan/milestones.md` の投影であり、原本を変えたら `source_hash`（git blob ID）と `updated_at` を更新する。
- 受入証拠は commit と run 出力に置く。計画 MD に実行ログを複製しない。

## 直近の一枠（約30分・現在 ready）

# Milestones — ComfyUI fork（実行用分解）

Plan-Status: in_progress

正本: [.concept/charter.yml](../.concept/charter.yml)（目的・非目標・成功指標・マイルストーンの定義）  
長期方針の見直し記録と現在地: [docs/plan/long-term-direction.md](plan/long-term-direction.md)  
現行の実行波（約30分の作業枠とWPカード）: [docs/plan/milestones.md](plan/milestones.md)

本書は charter のマイルストーンを実行可能な単位へ分解した索引であり、定義と正本状態は charter 側にある（charter の `done` / `active` は本書の `achieved` / `in_progress` と同義）。WP カードの実装手順・依存表は `docs/plan/milestones.md` が保持し、本書では重複して保持しない。各項目は charter の同一 ID（MS-001..MS-003）を引き継ぐ。

## 継続更新の回路

- 目標・マイルストーンを変更するときは charter を更新し、本書と `docs/plan/milestones.md` の参照を整合させる。
- `REPO_METADATA.json` は charter と `docs/plan/milestones.md` の投影であり、原本を変えたら `source_hash`（git blob ID）と `updated_at` を更新する。
- 受入証拠は commit と run 出力に置く。計画 MD に実行ログを複製しない。

## 直近の一枠（約30分・現在 ready）

- 対象: WP-A2 — CFLT-ASSETPERSIST-001 解消判定と charter MS-002 更新（カード全文は [docs/plan/milestones.md](plan/milestones.md)）
- 前提: WP-A1 の実行記録は取得済み（[docs/plan/evidence/wp-a1-alembic-chain.md](plan/evidence/wp-a1-alembic-chain.md)、着地 commit 0075fd4f、2026-11-07 観測）。既存 venv（`make install` 済み）
- 検証可能な行動: `alembic_db/README.md` の手順と versions 0001..0008 の実態一致を判定表にし、同一候補の make test 証拠（既存 CI 証拠の再利用可）と合わせて charter MS-002 の status を確定する
- 完了判定: 判定と根拠の記録、成功時は charter 更新の実際の default 着地まで
- 戻り先: WP-C2 — make test 再観測と MET-001 実測の更新（独立着手可、charter 編集は直列化）

## MS-001: Fork infrastructure stability

Outcome: 無人稼働の阻害要因を排除した fork 固有基盤（Makefile 標準ターゲット、Woodpecker gate、GitHub Actions 無効の運用）が維持され、CI gate が PR と main push で機能する  
Acceptance: `make test` が 0 failed（記録: 2026-10-10 1930 passed / 0 failed / 74 skipped）、`.woodpecker.yml` の Ruff + tests-unit 選別が PR と main push で green（出典: charter MS-001 acceptance、MET-001、MET-002）  
Evidence: charter MS-001 status=done と acceptance（make test）。Makefile の install/build/run/start/test/lint ターゲットと `.woodpecker.yml` gate の存在（2026-11-03 観測）。GitHub Actions 無効・Woodpecker 有効の運用記録は AUTOMATION.md Status  
Status: achieved  
依存: なし  
次の一手: 維持のみ（新規の改善は LOOP.md の候補順に従う）。MET-002 の green は Woodpecker 側の実観測でのみ更新する

## MS-002: Asset persistence layer integrity

Outcome: アセット永続化レイヤ（models.py の 6 テーブル、alembic_db 0001..0008、alembic_db/README.md）が実態と一致し、マイグレーション連鎖が隔離環境で実行可能であることが証拠で示される  
Acceptance: 隔離した一時 DB で `alembic upgrade head` が exit 0、`alembic current` が単一 head と一致、README の手順が versions 0001..0008 の実態と一致（CFLT-ASSETPERSIST-001 の解消）、`make test` が 0 failed  
Evidence: `app/assets/database/models.py` に 6 テーブル、`alembic_db/versions` に 0001..0008 の連鎖（いずれも 2026-11-03 観測）。WP-A1 の隔離実行証拠は取得済み: `docs/plan/evidence/wp-a1-alembic-chain.md`（run 20261107-235007-331852、着地 commit 0075fd4f — upgrade head が exit 0、heads/current とも単一 `0008_missing_content_age` に一致、2026-11-07 観測）。README 実態一致の判定と make test 同一候補証拠は未取得（WP-A2）  
Status: in_progress  
依存: WP-A1 は完了済み。WP-A2 の残りは README 判定と make test 証拠で、charter の編集は直列化する  
次の一手: WP-A2 を約30分枠で実行 — README と versions 0001..0008 の実態一致を判定し、同一候補の make test 証拠と合わせて charter MS-002 の status を確定する

## MS-003: Concept synchronization

Outcome: .concept/ の記述が実コード・テスト・追跡構成から乖離せず、autopilot 品質基準（Q1-Q8）を満たす状態が保たれる  
Acceptance: `.concept/*.yml` の yaml parse が成功し、`git ls-files .concept` が charter.yml / autopilot.yml / ontology_budget.yml の 3 ファイルと一致し、非追跡の runtime 12 ファイルが check-ignore される（MET-001 の再観測は WP-C2 で charter へ反映）  
Evidence: 820d2ae4 (#43) で runtime 生成物 12 ファイルの Git 追跡を解除して追跡は 3 ファイルになり、ガードテスト `tests-unit/concept_metadata_tracking_test.py` が追跡/除外を検査する。旧記載だった deliverables「固定 14 ファイル構成」は 2026-11-03 に現構成へ修正した。2026-11-11 再観測: `git ls-files .concept` = 3 ファイル、`.concept/*.yml` の yaml parse 3/3 OK、runtime 12 ファイルすべて check-ignore  
Status: in_progress  
依存: なし。WP-C1（charter deliverables を現構成へ整合）は 2026-11-03 の eadbeeeb で main へ着地済み（2026-11-11 確認）、残りは WP-C2。同じ charter を触るため反映は直列化する  
次の一手: WP-C2 を約30分枠で実行 — `make test` を1回だけ走らせ MET-001 の実測（passed/failed/skipped と対象 SHA）を記録し、charter の MET-001 記載を実測値へ更新する

## MS-001: Fork infrastructure stability

Outcome: 無人稼働の阻害要因を排除した fork 固有基盤（Makefile 標準ターゲット、Woodpecker gate、GitHub Actions 無効の運用）が維持され、CI gate が PR と main push で機能する
Acceptance: `make test` が 0 failed（記録: 2026-10-10 1930 passed / 0 failed / 74 skipped）、`.woodpecker.yml` の Ruff + tests-unit 選別が PR と main push で green（出典: charter MS-001 acceptance、MET-001、MET-002）
Evidence: charter MS-001 status=done と acceptance（make test）。Makefile の install/build/run/start/test/lint ターゲットと `.woodpecker.yml` gate の存在（2026-11-03 観測）。GitHub Actions 無効・Woodpecker 有効の運用記録は AUTOMATION.md Status
Status: achieved
依存: なし
次の一手: 維持のみ（新規の改善は LOOP.md の候補順に従う）。MET-002 の green は Woodpecker 側の実観測でのみ更新する

## MS-002: Asset persistence layer integrity

Outcome: アセット永続化レイヤ（models.py の 6 テーブル、alembic_db 0001..0008、alembic_db/README.md）が実態と一致し、マイグレーション連鎖が隔離環境で実行可能であることが証拠で示される
Acceptance: 隔離した一時 DB で `alembic upgrade head` が exit 0、`alembic current` が単一 head と一致、README の手順が versions 0001..0008 の実態と一致（CFLT-ASSETPERSIST-001 の解消）、`make test` が 0 failed
# Milestones — ComfyUI fork（実行用分解）

Plan-Status: in_progress

正本: [.concept/charter.yml](../.concept/charter.yml)（目的・非目標・成功指標・マイルストーンの定義）
長期方針の見直し記録と現在地: [docs/plan/long-term-direction.md](plan/long-term-direction.md)
現行の実行波（約30分の作業枠とWPカード）: [docs/plan/milestones.md](plan/milestones.md)

本書は charter のマイルストーンを実行可能な単位へ分解した索引であり、定義と正本状態は charter 側にある（charter の `done` / `active` は本書の `achieved` / `in_progress` と同義）。WP カードの実装手順・依存表は `docs/plan/milestones.md` が保持し、本書では重複して保持しない。各項目は charter の同一 ID（MS-001..MS-003）を引き継ぐ。

## 継続更新の回路

- 目標・マイルストーンを変更するときは charter を更新し、本書と `docs/plan/milestones.md` の参照を整合させる。
- `REPO_METADATA.json` は charter と `docs/plan/milestones.md` の投影であり、原本を変えたら `source_hash`（git blob ID）と `updated_at` を更新する。
- 受入証拠は commit と run 出力に置く。計画 MD に実行ログを複製しない。

## 直近の一枠（約30分・現在 ready）

- 対象: WP-C2 — `make test` の再観測と MET-001 の記載更新（カード全文は [docs/plan/milestones.md](plan/milestones.md)）
- 検証可能な行動: `make test` を1回だけ実行し、passed / failed / skipped の集計行と対象 SHA を run 出力へ記録する。0 failed なら charter MET-001 の実測値と観測日をその値へ更新する
- 完了判定: テスト実行のサマリ行（passed / failed / skipped）と対象 commit SHA が run 出力に残り、charter MET-001 の記載が実測値と一致する
- 前提: 既存 venv（`make install` 済み）。テストコードは変更しない
- 戻り先: MS-003 の status 判定（charter exit_criteria 2 項の充足状況）
- 注記: WP-A1 の隔離実行証拠は run 20261107-235007-331852、commit 0075fd4f に記録済み。WP-A2 の README 実態一致判定と同一候補の make test 証拠は未取得で、WP-A2 は WP-C2 と独立して着手できる。同じ charter を編集するため、charter の更新は直列化する

## MS-001: Fork infrastructure stability

Outcome: 無人稼働の阻害要因を排除した fork 固有基盤（Makefile 標準ターゲット、Woodpecker gate、GitHub Actions 無効の運用）が維持され、CI gate が PR と main push で機能する
Acceptance: `make test` が 0 failed（記録: 2026-10-10 1930 passed / 0 failed / 74 skipped）、`.woodpecker.yml` の Ruff + tests-unit 選別が PR と main push で green（出典: charter MS-001 acceptance、MET-001、MET-002）
Evidence: charter MS-001 status=done と acceptance（make test）。Makefile の install/build/run/start/test/lint ターゲットと `.woodpecker.yml` gate の存在（2026-11-03 観測）。GitHub Actions 無効・Woodpecker 有効の運用記録は AUTOMATION.md Status
Status: achieved
依存: なし
次の一手: 維持のみ（新規の改善は LOOP.md の候補順に従う）。MET-002 の green は Woodpecker 側の実観測でのみ更新する

## MS-002: Asset persistence layer integrity

Outcome: アセット永続化レイヤ（models.py の 6 テーブル、alembic_db 0001..0008、alembic_db/README.md）が実態と一致し、マイグレーション連鎖が隔離環境で実行可能であることが証拠で示される
Acceptance: 隔離した一時 DB で `alembic upgrade head` が exit 0、`alembic current` が単一 head と一致、README の手順が versions 0001..0008 の実態と一致（CFLT-ASSETPERSIST-001 の解消）、`make test` が 0 failed
Evidence: `app/assets/database/models.py` に 6 テーブル、`alembic_db/versions` に 0001..0008 の連鎖（2026-11-11 再観測）。WP-A1 の隔離実行証拠は `docs/plan/evidence/wp-a1-alembic-chain.md`（run 20261107-235007-331852、着地 commit 0075fd4f — `upgrade head` が exit 0、heads/current とも単一 `0008_missing_content_age` に一致、2026-11-07 観測）。README 実態一致の判定と make test 同一候補証拠は未取得（WP-A2）
Status: in_progress
依存: WP-A1 は完了済み。WP-A2 の残りは README 判定と make test 証拠で、charter の編集は直列化する
次の一手: WP-A2 を約30分枠で実行 — README と versions 0001..0008 の実態一致を判定し、同一候補の make test 証拠と合わせて charter MS-002 の status を確定する

## MS-003: Concept synchronization

Outcome: .concept/ の記述が実コード・テスト・追跡構成から乖離せず、autopilot 品質基準（Q1-Q8）を満たす状態が保たれる
Acceptance: `.concept/*.yml` の yaml parse が成功し、`git ls-files .concept` が charter.yml / autopilot.yml / ontology_budget.yml の 3 ファイルと一致し、非追跡の runtime 12 ファイルが check-ignore される（MET-001 の再観測は WP-C2 で charter へ反映）
Evidence: 820d2ae4 (#43) で runtime 生成物 12 ファイルの Git 追跡を解除して追跡は 3 ファイルになり、ガードテスト `tests-unit/concept_metadata_tracking_test.py` が追跡/除外を検査する。旧記載だった deliverables「固定 14 ファイル構成」は 2026-11-03 に現構成へ修正した。2026-11-11 再観測: `git ls-files .concept` = 3 ファイル、`.concept/*.yml` の yaml parse 3/3 OK、runtime 12 ファイルすべて check-ignore
Status: in_progress
依存: なし。WP-C1 は着地済み（charter MS-003 deliverables を2026-11-03に現構成へ修正、eadbeeebで着地）、残りは WP-C2。同じ charter を触るため反映は直列化する
次の一手: WP-C2 を約30分枠で実行 — `make test` を1回だけ走らせ MET-001 の実測（passed/failed/skipped と対象 SHA）を記録し、charter の MET-001 記載を実測値へ更新する

## MS-003: Concept synchronization

Outcome: .concept/ の記述が実コード・テスト・追跡構成から乖離せず、autopilot 品質基準（Q1-Q8）を満たす状態が保たれる
Acceptance: `.concept/*.yml` の yaml parse が成功し、`git ls-files .concept` が charter.yml / autopilot.yml / ontology_budget.yml の 3 ファイルと一致し、非追跡の runtime 12 ファイルが check-ignore される（MET-001 の再観測は WP-C2 で charter へ反映）
Evidence: 820d2ae4 (#43) で runtime 生成物 12 ファイルの Git 追跡を解除して追跡は 3 ファイルになり、ガードテスト `tests-unit/concept_metadata_tracking_test.py` が追跡/除外を検査する。旧記載だった deliverables「固定 14 ファイル構成」は 2026-11-03 に現構成へ修正した。2026-11-11 再観測: `git ls-files .concept` = 3 ファイル、`.concept/*.yml` の yaml parse 3/3 OK、runtime 12 ファイルすべて check-ignore
Status: in_progress
# Milestones — ComfyUI fork（実行用分解）

Plan-Status: in_progress

正本: [.concept/charter.yml](../.concept/charter.yml)（目的・非目標・成功指標・マイルストーンの定義）
長期方針の見直し記録と現在地: [docs/plan/long-term-direction.md](plan/long-term-direction.md)
現行の実行波（約30分の作業枠とWPカード）: [docs/plan/milestones.md](plan/milestones.md)

本書は charter のマイルストーンを実行可能な単位へ分解した索引であり、定義と正本状態は charter 側にある（charter の `done` / `active` は本書の `achieved` / `in_progress` と同義）。WP カードの実装手順・依存表は `docs/plan/milestones.md` が保持し、本書では重複して保持しない。各項目は charter の同一 ID（MS-001..MS-003）を引き継ぐ。

## 継続更新の回路

- 目標・マイルストーンを変更するときは charter を更新し、本書と `docs/plan/milestones.md` の参照を整合させる。
- `REPO_METADATA.json` は charter と `docs/plan/milestones.md` の投影であり、原本を変えたら `source_hash`（git blob ID）と `updated_at` を更新する。
- 受入証拠は commit と run 出力に置く。計画 MD に実行ログを複製しない。

## 直近の一枠（約30分・現在 ready）

- 対象: WP-C2 — `make test` の再観測と MET-001 の記載更新（カード全文は [docs/plan/milestones.md](plan/milestones.md)）
- 検証可能な行動: `make test` を1回だけ実行し、passed / failed / skipped の集計行と対象 SHA を run 出力へ記録する。0 failed なら charter MET-001 の実測値と観測日をその値へ更新する
- 完了判定: テスト実行のサマリ行（passed / failed / skipped）と対象 commit SHA が run 出力に残り、charter MET-001 の記載が実測値と一致する
- 前提: 既存 venv（`make install` 済み）。テストコードは変更しない
- 戻り先: MS-003 の status 判定（charter exit_criteria 2 項の充足状況）
- 注記: WP-A1 の隔離実行証拠は `docs/plan/evidence/wp-a1-alembic-chain.md` に記録済み（run `20261107-235007-331852`、報告された着地 commit `0075fd4f`、2026-11-07 観測）。ただし、WP-A1 / WP-A2 の成果が default に着地したかは未確認のため、MS-002 は着地確認まで active のまま据え置く。main での README 実態一致の判定は未取得

## MS-001: Fork infrastructure stability

Outcome: 無人稼働の阻害要因を排除した fork 固有基盤（Makefile 標準ターゲット、Woodpecker gate、GitHub Actions 無効の運用）が維持され、CI gate が PR と main push で機能する
Acceptance: `make test` が 0 failed（記録: 2026-10-10 1930 passed / 0 failed / 74 skipped）、`.woodpecker.yml` の Ruff + tests-unit 選別が PR と main push で green（出典: charter MS-001 acceptance、MET-001、MET-002）
Evidence: charter MS-001 status=done と acceptance（make test）。Makefile の install/build/run/start/test/lint ターゲットと `.woodpecker.yml` gate の存在（2026-11-03 観測）。GitHub Actions 無効・Woodpecker 有効の運用記録は AUTOMATION.md Status
Status: achieved
依存: なし
次の一手: 維持のみ（新規の改善は LOOP.md の候補順に従う）。MET-002 の green は Woodpecker 側の実観測でのみ更新する

## MS-002: Asset persistence layer integrity

Outcome: アセット永続化レイヤ（models.py の 6 テーブル、alembic_db 0001..0008、alembic_db/README.md）が実態と一致し、マイグレーション連鎖が隔離環境で実行可能であることが証拠で示される
Acceptance: 隔離した一時 DB で `alembic upgrade head` が exit 0、`alembic current` が単一 head と一致、README の手順が versions 0001..0008 の実態と一致（CFLT-ASSETPERSIST-001 の解消）、`make test` が 0 failed
Evidence: `app/assets/database/models.py` に 6 テーブル、`alembic_db/versions` に 0001..0008 の連鎖（2026-11-11 再観測）。WP-A1 の隔離実行証拠は `docs/plan/evidence/wp-a1-alembic-chain.md` に記録済み（run `20261107-235007-331852`、報告された着地 commit `0075fd4f` — `alembic upgrade head` が exit 0、heads/current とも単一 `0008_missing_content_age` に一致、2026-11-07 観測）。main での README 実態一致の判定は未取得。WP-A1 / WP-A2 の成果が default に着地したかは未確認
Status: in_progress
依存: なし。WP-A1 の実行記録は取得済み。WP-A2 は README 判定と make test 同一候補証拠に依存し、charter の編集は直列化する
次の一手: WP-A1 / WP-A2 の成果が default へ着地したかを確認する。未着地なら active を維持し、WP-A2 で README と versions 0001..0008 の実態一致を判定し、同一候補の make test 証拠と合わせて charter MS-002 の status を確定する

## MS-003: Concept synchronization

Outcome: .concept/ の記述が実コード・テスト・追跡構成から乖離せず、autopilot 品質基準（Q1-Q8）を満たす状態が保たれる
Acceptance: `.concept/*.yml` の yaml parse が成功し、`git ls-files .concept` が charter.yml / autopilot.yml / ontology_budget.yml の 3 ファイルと一致し、非追跡の runtime 12 ファイルが check-ignore される（MET-001 の再観測は WP-C2 で charter へ反映）
Evidence: 820d2ae4 (#43) で runtime 生成物 12 ファイルの Git 追跡を解除して追跡は 3 ファイルになり、ガードテスト `tests-unit/concept_metadata_tracking_test.py` が追跡/除外を検査する。旧記載だった deliverables「固定 14 ファイル構成」は 2026-11-03 に現構成へ修正した。2026-11-11 再観測: `git ls-files .concept` = 3 ファイル、`.concept/*.yml` の yaml parse 3/3 OK、runtime 12 ファイルすべて check-ignore
Status: in_progress
依存: なし。WP-C1 は着地済み（charter MS-003 deliverables を 2026-11-03 に現構成へ修正、eadbeeeb で着地。2026-11-11 確認）。残りは WP-C2。同じ charter を触るため反映は直列化する
次の一手: WP-C2 を約30分枠で実行 — `make test` を1回だけ走らせ MET-001 の実測（passed/failed/skipped と対象 SHA）を記録し、charter の MET-001 記載を実測値へ更新する
次の一手: WP-C2 を約30分枠で実行 — `make test` を1回だけ走らせ MET-001 の実測（passed/failed/skipped と対象 SHA）を記録し、charter の MET-001 記載を実測値へ更新する
