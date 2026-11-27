# Milestones — ComfyUI fork

Plan-Status: in_progress

正本: [`.concept/charter.yml`](../.concept/charter.yml)（目的・非目標・指標・マイルストーン）  
長期方針と現在地: [long-term-direction.md](plan/long-term-direction.md)  
実行波と WP: [milestones.md](plan/milestones.md)

本書は charter MS-001〜MS-005 の実行用分解。定義・優先順位・状態は charter が正本で、WP の手順と依存は実行波に置く。`achieved` は受入条件に対する記録済み証拠を示す。未確認の実行や最新 CI は pending のままにする。

## 停止時評価 — 2026-11-27

制御平面の停止観測は前回評価済みの `run-5707669ae112`（`failed` / reason `unknown`、2026-11-18 評価）のまま変化なし。2026-11-23 の停止時評価は PR #67 として 2026-11-24T04:10:24Z に着地済み（main `f5536936`）。最新の失敗は 2026-11-24T09:38Z の bug-fix run `20261124-093848-120294` で、worker は `[push_denied]` 403（`denied to nobu007`）の root-cause 調査を完了し commit `48a929c2` を保存済み worktree に残したが、着地が merge 前に blocked（evaluation-or-landing-failed）。停止原因はすべて repo 外: 403 はホスト GitHub 資格層（グローバル `insteadOf` 資格埋め込み + 自動化アカウント資格の注入）で `setup` commit `65a2fae` により是正済み、着地 blocked の構造原因は tas_autopilot `_REQUIRED_CHECK_*` テーブルへの `jinno2/ComfyUI` 未登録による全 PR auto-merge block。repo 内に残る欠陥は確認されていない（charter parse を本評価時に再確認、exit 0）。長期目的と現状の差（MS-002 WP-A2 の main 上の証拠が未取得）に変化はなく、計画は維持、milestone の状態・優先順・次の一枠（WP-A2）は変更しない。未解決依存は tas_autopilot 側の登録修正、commit `48a929c2` と `9b073fbc` の着地（いずれも既存 TAS 経路で処理、本 run では再作成しない）。再開条件は登録完了後に着地 blocked が再発しないこと。詳細な根拠と再開条件は[長期方針の停止時評価](plan/long-term-direction.md#停止時評価--2026-11-27)と[現行実行波の停止時評価](plan/milestones.md#停止時評価--2026-11-27)を参照。

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
