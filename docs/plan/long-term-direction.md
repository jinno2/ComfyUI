# ComfyUI fork — 長期方針と現在地

計画確認日: 2026-10-24。基準コミット: `5fa1cf5ab0fe5b5fb47968bcddbe3a0960523376`。
目的・成功指標・非目標の正本は [`.concept/charter.yml`](../../.concept/charter.yml)。charter の north star は「推定」と明記された現行記述であり、所有者が別途確定した事業目的として扱わない。本書はその記述を現状証拠と結び、長期の差分・順序・出口を示す。実行項目の唯一の入口は [`../MILESTONES.md`](../MILESTONES.md)。

## 目的と到達点

charter の現行 north star は、上流へ自動追従しない恒久自律開発で、モジュラーなノードグラフ型 AI コンテンツ生成エンジンの ComfyUI fork を安定提供すること（推定）。成功指標は `make test` が 0 failed であること（MET-001）と、Woodpecker の Ruff + `tests-unit` gate が PR と `main` push で green であること（MET-002）。

到達点は、charter の各 milestone の成果と受入証拠が現行実装に一致し、MET-001/002 を対象 commit に結び付く記録で確認でき、次の保守作業を同じ正本から再開できる状態。現時点では全体の達成を宣言しない。

## 現状と差分

|領域|確認済みの現状|未確認・残る差分|
|---|---|---|
|MS-001 Fork infrastructure stability|charter は done。MET-001 に 2026-10-10 の `1930 passed / 0 failed / 74 skipped` が記録され、`.woodpecker.yml` に Ruff と unit gate が定義されている。|最新候補のテスト結果と Woodpecker run の green はこの checkout から確認できていない。記録値を現在の実測へ読み替えない。|
|MS-002 Asset persistence layer integrity|`models.py` に 6 テーブル、`alembic_db/versions/` に 0001..0008 があり、README は autogenerate の手順を記載する。charter status は active。|隔離 DB での `upgrade head` / `current` 実測と、README の手順が現行 migration 群に合うかの判定が未記録。`make test` の新しい実測も未確認。|
|MS-003 Concept synchronization|Git 追跡対象は `.concept/charter.yml`、`autopilot.yml`、`ontology_budget.yml` の3ファイル。runtime metadata を ignore し seeds を追跡するテストがある。|charter の記載を現構成に整合させた。ガードテストと `git ls-files .concept` の再検証結果は未記録。|

## 優先順・依存・出口

1. **P0 — MS-001 を維持する。** charter では既に done で、2026-10-10 の `make test` 記録があるため再実装はしない。charter の milestone 出口は `make test` が 0 failed で、`.woodpecker.yml` に既定 gate が定義されていること。MET-002 の継続運転は別途対象 SHA の green run で確認する。最新 CI 観測はこの checkout では未確認。
2. **P1 — MS-002 の受入証拠を確定する。** まず隔離した一時 DB の migration 連鎖を確認し、その後 README の手順と現行 migration 群、および有効な `make test` 証拠を照合する。WP-A2 の判定は WP-A1 の結果に依存する。全条件が確認できるまで active のままにする。
3. **P2 — MS-003 の構成同期を受入確認する。** MS-002 とは独立。追跡対象が3 seed のみで、runtime metadata が ignore され、専用ガードテストが通ることを確認する。

MS-002 / MS-003 は実装物の存在だけでは出口に達しない。各 milestone は `docs/MILESTONES.md` の Acceptance と Evidence に照らして判定する。観測不能・失敗は pending のまま保持し、commit/PR の存在だけで achieved にしない。全項目の確認後に MET-002 の継続状態を再確認し、目的全体が満たされた証拠がある場合だけ計画を achieved とする。

## 守る境界と次の一手

- charter の目的・非目標と、[`AUTOMATION.md`](../../AUTOMATION.md) の driver 分担を維持する。上流取り込みは所有者の明示指示時のみ。TAS が dispatch / 着地、Woodpecker が CI gate を担当する。
- `AGENTS.md` の No Internet Requests と最小変更方針を守り、外部通信 path、事業目的、権限、予算を計画作業で変更しない。
- 次の一手は **MS-002 / WP-A1**: 既存環境で隔離した一時 DB のみを使い、`alembic upgrade head`、`alembic heads`、`alembic current` の結果と exit code を保存する（約30分）。本番 DB を使わず、実測を得るまでは Evidence を pending にする。

計画の短期投影は [`../../REPO_METADATA.json`](../../REPO_METADATA.json)、履歴を含む前回の実行波は [`milestones.md`](milestones.md) を参照する。後者は 2026-10-21 時点の WP 定義を保持する記録であり、現行状態の管理には使わない。
