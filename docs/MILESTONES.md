# Milestones — ComfyUI fork

Plan-Status: in_progress

正本: [`.concept/charter.yml`](../.concept/charter.yml)（目的・非目標・指標・マイルストーン）  
長期方針と現在地: [long-term-direction.md](plan/long-term-direction.md)  
実行波と WP: [milestones.md](plan/milestones.md)

本書は charter MS-001〜MS-005 の実行用分解。定義・優先順位・状態は charter が正本で、WP の手順と依存は実行波に置く。`achieved` は受入条件に対する記録済み証拠を示す。未確認の実行や最新 CI は pending のままにする。

## 停止時評価 — 2026-11-18

制御平面の `run-5707669ae112` は `failed` / reason `unknown`。関連する ComfyUI run `20261118-173303-344644` の worker 報告は、期限の誤認後に読み取り専用の実行可能性調査を記録し、訂正後も元 mission と記録済み定義の範囲不一致を理由に実行しなかったとしている。独立した制御平面の失敗分類は未確認のため reason は unknown のまま保持する。計画は維持し、既存 milestone の状態・優先順は変更しない。停止した mission は TAS の新 dispatch で再開する。再開後の約30分作業は LOOP 順で候補を一つ選び、指定検証と1 commitを完了すること。詳細な根拠と再開条件は[長期方針の停止時評価](plan/long-term-direction.md#停止時評価--2026-11-18)と[現行実行波の停止時評価](plan/milestones.md#停止時評価--run-5707669ae112)を参照。

## 直近の一枠（約30分）

- 対象: WP-A2 — `alembic_db/README.md` と migration versions 0001〜0008 の実態を照合し、同一候補の `make test` 結果を確認する。
- 完了条件: 隔離 DB だけに `alembic upgrade head` を実行して exit 0、`alembic heads` と `alembic current` が単一 head で一致し、README の記述が実装と一致する。同一候補の `make test` が 0 failed であることを確認し、検証済み証拠を charter に反映する。証拠が default に着地するまで MS-002 は active のままにする。
- 依存: WP-A1 の隔離 DB 証拠は取得済み。MS-002 と MS-003 の charter 更新は直列化する。

## MS-001: Fork infrastructure stability

Outcome: fork 固有の Makefile、基盤、CI gate、upstream workflow guard を安定して維持し、unit suite の失敗を防ぐ。  
Acceptance: charter に定める `make test` が 0 failed。.woodpecker.yml に PR と main push 向けの Ruff と `tests-unit` gate が定義されている。  
Evidence: charter status=`done`。charter MET-001 に 2026-10-10 の `1930 passed / 0 failed / 74 skipped` を記録。Makefile の標準ターゲットと `.woodpecker.yml` の両 gate は 2026-11-03 に確認。最新 CI run はこの計画更新では再観測していない。  
Status: achieved  
依存: なし。  
次の一手: 維持。新しい作業は通常候補選択に従う。次の受入観測時は対象 SHA と既存 Woodpecker run を照合し、最新 gate の結果を記録する。再実装や pipeline の手動起動はしない。

## MS-002: Asset persistence layer integrity

Outcome: SQLAlchemy schema、migration chain、README の更新手順が実態と一致し、migration を隔離環境で実行できる。  
Acceptance: 一時 DB だけに `alembic upgrade head` を実行して exit 0、`alembic heads` と `alembic current` が単一 head で一致する。README の手順と versions 0001〜0008 が一致し、同一候補の `make test` が 0 failed。  
Evidence: [`WP-A1` 実行証拠](plan/evidence/wp-a1-alembic-chain.md) は `upgrade head` と `current` の単一 `0008_missing_content_age` を記録。WP-A2 の README 判定と同一候補の test 証拠は main の charter で未確認。  
Status: in_progress  
依存: WP-A1 → WP-A2。  
次の一手: 直近の一枠 WP-A2 を実施し、隔離 DB の出力・exit code と対象 commit を含む検証済み証拠だけを charter に反映する。DB 設定を継承せず、本番 DB に接続しない。

## MS-003: Concept synchronization

Outcome: `.concept` の手管理 seed と runtime 除外が実態に一致し、継続的な test gate が保たれる。  
Acceptance: `.concept/*.yml` が parse できる。`git ls-files .concept` が `charter.yml`、`autopilot.yml`、`ontology_budget.yml` の3ファイルを示し、runtime 生成物12ファイルが `check-ignore` される。`pytest tests-unit/concept_metadata_tracking_test.py -q` が成功する。  
Evidence: 2026-11-11 の記録で YAML parse 3/3、追跡3ファイル、runtime 除外12/12。専用テストは seed の追跡と runtime metadata の ignore を確認する。MET-001 の新鮮な実測と専用テストの実行結果は未確認。  
Status: in_progress  
依存: 構成確認はなし。WP-C2 の charter 更新は WP-A2 更新後。  
次の一手: WP-C2 で `make test` を一度実行し、集計と対象 SHA を記録して charter MET-001 を更新する。専用ガードテストの成功も確認して記録する。

## MS-004: フォーク状態の可視化

Outcome: fork 固有コミット数と upstream 同期状態を新鮮な git 計測で把握する。  
Acceptance: `.concept/claims.ndjson` に対象 SHA、基準 ref、計測時点を含む ForkUpstreamSync claim がある。  
Evidence: pending — fresh upstream baseline に基づく claim を未確認。  
Status: in_progress  
依存: 新鮮な upstream baseline。  
次の一手: 既存の許可済み作業で fresh ref が利用できる時に計測し、欠けた入力は unknown と記録する。

## MS-005: Documentation and implementation alignment

Outcome: docs の手順と実装の不一致を具体的な差分単位で解消する。  
Acceptance: 対象手順と実装を照合し、特定した不一致を解消する。今回の計画更新では新しい不一致を調査していない。  
Evidence: pending — 現在の未修正候補は未特定。  
Status: planned  
依存: なし。  
次の一手: LOOP の通常候補選択で具体的な不一致を見つけた時に分解する。
