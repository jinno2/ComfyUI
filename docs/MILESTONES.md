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
- 注記: WP-A1 / WP-A2 の成果は未着地ブランチ（6d8fbffd / ae41a228）にのみ存在する。MS-002 は当該成果が default へ着地するまで active のまま据え置く（main には alembic upgrade head の実走証拠も README 実態一致の判定も未取得）

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
Evidence: `app/assets/database/models.py` に 6 テーブル、`alembic_db/versions` に 0001..0008 の連鎖（2026-11-11 再観測）。main の `alembic_db/README.md` は4行のままで、隔離一時 DB への `alembic upgrade head` 実走の証拠と README 実態一致の判定は main には未取得（WP-A1 / WP-A2 の成果は未着地ブランチ 6d8fbffd / ae41a228 にのみ存在）
Status: in_progress
依存: なし。WP-A2 は WP-A1 の実行記録に依存し、charter の編集は直列化する
次の一手: WP-A1 / WP-A2 の成果が default へ着地したかを確認し、着地であれば charter MS-002 の status を evidence 付きで done へ更新する（未着地なら active を維持し、解除条件として「成果の着地」を残す）

## MS-003: Concept synchronization

Outcome: .concept/ の記述が実コード・テスト・追跡構成から乖離せず、autopilot 品質基準（Q1-Q8）を満たす状態が保たれる
Acceptance: `.concept/*.yml` の yaml parse が成功し、`git ls-files .concept` が charter.yml / autopilot.yml / ontology_budget.yml の 3 ファイルと一致し、非追跡の runtime 12 ファイルが check-ignore される（MET-001 の再観測は WP-C2 で charter へ反映）
Evidence: 820d2ae4 (#43) で runtime 生成物 12 ファイルの Git 追跡を解除して追跡は 3 ファイルになり、ガードテスト `tests-unit/concept_metadata_tracking_test.py` が追跡/除外を検査する。旧記載だった deliverables「固定 14 ファイル構成」は 2026-11-03 に現構成へ修正した。2026-11-11 再観測: `git ls-files .concept` = 3 ファイル、`.concept/*.yml` の yaml parse 3/3 OK、runtime 12 ファイルすべて check-ignore
Status: in_progress
依存: なし。WP-C1（charter deliverables を現構成へ整合）は 2026-11-03 の eadbeeeb で main へ着地済み（2026-11-11 確認）、残りは WP-C2。同じ charter を触るため反映は直列化する
次の一手: WP-C2 を約30分枠で実行 — `make test` を1回だけ走らせ MET-001 の実測（passed/failed/skipped と対象 SHA）を記録し、charter の MET-001 記載を実測値へ更新する
