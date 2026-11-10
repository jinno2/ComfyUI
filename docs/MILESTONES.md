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

- 対象: WP-A1 — alembic マイグレーション連鎖の受入確認（カード全文は [docs/plan/milestones.md](plan/milestones.md)）
- 検証可能な行動: 隔離した一時 DB ファイルに対し `alembic upgrade head` を実行し、exit code 0 と `alembic current` が単一 head と一致することを確認する
- 完了判定: 実行コマンドと exit code、`alembic heads` / `alembic current` の出力を run 出力へ残す（計画 MD への転記は不要）
- 前提: 既存 venv（`make install` 済み）。新規依存の追加とコード変更はしない
- 戻り先: WP-A2 — charter MS-002 の status / acceptance を証拠付きで確定する

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
Evidence: `app/assets/database/models.py` に 6 テーブル、`alembic_db/versions` に 0001..0008 の連鎖（いずれも 2026-11-03 観測）。alembic upgrade head の実行証拠と README 実態一致の判定は未取得（WP-A1 / WP-A2）
Status: in_progress
依存: なし。WP-A2 は WP-A1 の実行記録に依存し、charter の編集は直列化する
次の一手: WP-A1 を約30分枠で実行 — 一時 DB へ `alembic upgrade head` を実行し、exit code と `alembic heads` / `alembic current` を記録する

## MS-003: Concept synchronization

Outcome: .concept/ の記述が実コード・テスト・追跡構成から乖離せず、autopilot 品質基準（Q1-Q8）を満たす状態が保たれる
Acceptance: `.concept/*.yml` の yaml parse が成功し、`git ls-files .concept` が charter.yml / autopilot.yml / ontology_budget.yml の 3 ファイルと一致し、非追跡の runtime 12 ファイルが check-ignore される（MET-001 の再観測は WP-C2 で charter へ反映）
Evidence: 820d2ae4 (#43) で runtime 生成物 12 ファイルの Git 追跡を解除して追跡は 3 ファイルになり、ガードテスト `tests-unit/concept_metadata_tracking_test.py` が追跡/除外を検査する。旧記載だった deliverables「固定 14 ファイル構成」は 2026-11-03 に現構成へ修正した
Status: in_progress
依存: なし。WP-C1（charter deliverables を現構成へ整合）は 2026-11-03 の eadbeeeb で main へ着地済み（2026-11-10 確認）、残りは WP-C2。同じ charter を触るため反映は直列化する
次の一手: WP-C2 を約30分枠で実行 — `make test` を1回だけ走らせ MET-001 の実測（passed/failed/skipped と対象 SHA）を記録し、charter の MET-001 記載を実測値へ更新する
