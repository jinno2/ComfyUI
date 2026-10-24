# ComfyUI fork — Milestones

長期計画: [long-term-direction.md](plan/long-term-direction.md)。目的・成功指標・非目標の正本: [`.concept/charter.yml`](../.concept/charter.yml)。このファイルだけを現行 milestone 状態と次作業の入口として使う。旧 WP の履歴と ID は [`plan/milestones.md`](plan/milestones.md) に保持する。

状態は 2026-10-24 時点の checkout evidence に基づく。`achieved` は受入条件に対する記録済み証拠を示す。未確認の実行や最新 CI は pending のままにする。

## MS-001: Fork infrastructure stability

Outcome: fork 固有の Makefile、CI gate、upstream workflow guard を安定維持し、テスト条件を満たす。
Acceptance: charter に定める `make test` が 0 failed。`.woodpecker.yml` に PR と main push 向けの Ruff と `tests-unit` gate が定義されている。
Evidence: charter MET-001 に 2026-10-10 の `1930 passed / 0 failed / 74 skipped` を記録。`.woodpecker.yml` に両 gate の定義あり。最新 run はこの checkout では未確認。
Status: achieved
依存: なし。charter は本 milestone を done と記録している。現行 CI の継続観測は保守上の確認事項として記録し、歴史値を最新値に読み替えない。
次の作業: 次の受入観測時に対象 SHA と既存 Woodpecker run を照合し、最新の gate 結果を記録する。再実装や pipeline の手動起動はしない。

## MS-002: Asset persistence layer integrity

Outcome: asset schema、0001..0008 migration 連鎖、README の更新手順が一致し、隔離 DB とテストの受入証拠が残る。
Acceptance: 一時 DB だけに `alembic upgrade head` を実行して exit 0、`alembic heads` と `alembic current` が単一 head で一致する。README の autogenerate 手順と migration 実態を照合し、`make test` の有効な成功証拠を確認する。
Evidence: `models.py` に6テーブル、`alembic_db/versions/` に0001..0008を確認。migration実走・現行テスト証拠は pending。
Status: verifying
依存: なし。WP-A2 の done 判定は WP-A1 の成功記録に依存する。
次の作業: WP-A1（約30分）— 隔離した一時 SQLite DB で migration を実走し、3コマンドの出力・exit code と対象 commit を記録する。DB設定を継承せず、本番 DB に接続しない。

## MS-003: Concept synchronization

Outcome: .concept の永続 seed だけを追跡し、生成 runtime metadata を Git 追跡へ戻さない。
Acceptance: `git ls-files .concept` が `charter.yml`、`autopilot.yml`、`ontology_budget.yml` の3件を示し、`pytest tests-unit/concept_metadata_tracking_test.py -q` が成功する。
Evidence: 現在の `git ls-files .concept` は3 seed。専用テストは seed の追跡と runtime metadata の ignore を確認する。テスト実行結果は pending。
Status: verifying
依存: なし。MS-002 と独立。
次の作業: 対象 checkout で上記の追跡一覧と専用ガードテストを確認し、結果を記録する。
