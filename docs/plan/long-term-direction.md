# ComfyUI fork — 長期方針

再確認: 2026-11-17（基準: `origin/main` @ `f3fbf32f`）。目的・成功指標・非目標とマイルストーン状態の正本は [`.concept/charter.yml`](../../.concept/charter.yml)。本書は現状との差、優先順、到達段階を示す。実行可能な受入条件と次の一手は [`../MILESTONES.md`](../MILESTONES.md) を参照し、詳細を重複して管理しない。

## 目的と境界

charter の推定 north star は、画像生成研究を起点に、画像・動画・3D・音声を扱うモジュラーなノードグラフ型 ComfyUI fork を、上流へ自動追従せず安定提供し続けること。成功指標は `make test` が 0 failed であること（MET-001）、Woodpecker の Ruff + `tests-unit` gate が PR と `main` push で green であること（MET-002）、fork 固有状態を可視化すること。外部通信、deploy/release、上流への自動追従・操作は非目標。

実装・運用の責務は既存の所有者に従う。ComfyUI はノードグラフと fork 固有変更、TAS は dispatch と着地、Woodpecker は CI、所有者は上流取り込みと driver 変更を担う。権限は現在の task packet が定める。上流取り込みは所有者の明示指示時のみ行う。

## 現状と到達点

| ID | 到達点・現状との差 | 状態・根拠 | 優先順・依存・出口 | 次の一手 |
|---|---|---|---|---|
| MS-001 | fork の基盤と CI gate を維持する。標準 Makefile ターゲットと Woodpecker 設定がある。 | achieved。charter の `done`、Makefile、`.woodpecker.yml`。 | P0、依存なし。charter の test と CI gate 条件を維持する。MET-001/002 の過去の記録を現在の実測へ読み替えない。 | 維持。新しい作業は通常候補選択に従う。 |
| MS-002 | アセット永続化の実装はあるが、main 上の README 手順と受入証拠の整合は未確定。WP-A1 の隔離 DB 実行証拠は [`evidence/wp-a1-alembic-chain.md`](evidence/wp-a1-alembic-chain.md) にある。 | in_progress。WP-A2 成果の main 着地と同一候補 `make test` 証拠は未確認。 | P1、WP-A1 → WP-A2。隔離 DB migration、README と versions 整合、同一候補の test acceptance を満たし、charter に証拠を反映する。 | WP-A2 を約30分枠で実施。詳細は [milestones.md](milestones.md)。 |
| MS-003 | `.concept` の追跡構成と runtime 除外は 2026-11-11 に再観測済み。charter の現行値と MET-001 の再観測を揃える作業が残る。 | in_progress。追跡3ファイル、YAML parse 3/3、runtime 12件の check-ignore 12/12（2026-11-11、実行波の記録）。 | P2、構成確認は依存なし。charter の YAML・追跡・除外条件を確認し、MET-001 を新鮮な test run と対象 SHA で記録する。 | WP-C2 は MS-002 の charter 編集後に実施する。 |
| MS-004 | fork 固有コミット数と上流同期状態を新鮮な計測で把握する。現在のローカル upstream ref の鮮度は未確認。 | in_progress。新鮮な計測 claim は pending。 | P1、fresh upstream baseline が必要。charter の ForkUpstreamSync 計測条件を満たす。 | 新鮮な参照を利用できる既存の許可済み作業時に計測し、欠けた入力は unknown のままにする。 |
| MS-005 | docs と実装の不一致を継続して解消する。今回、具体的な未修正の不一致は追加調査していない。 | planned。charter の手動レビュー条件が根拠。 | P2、依存なし。具体的な不一致を特定し、実装と文書を照合して解消する。 | LOOP の通常候補選択で具体的な候補が見つかった時に分解する。 |

MS-001〜MS-005 の定義と状態は charter、実行可能な AC と次の一手は [`../MILESTONES.md`](../MILESTONES.md) に置く。項目の状態は charter の `done` / `active` / `planned` を同ファイルの語彙へ対応させる。

## 計画段階

1. **受入証拠を確定する** — MS-002 の WP-A2 を完了し、MS-003 の現行構成と MET-001 を確定する。共通の charter 更新は直列化する。
2. **計画候補の接続を確認する** — WP-S2-1 / WP-S2-2 の記録は、TAS dispatch が計画候補を比較し、追加の LOOP 変更を要しないという現行方針を示す。14 run 中13 runで計画参照、10 runで計画由来候補の選択・実行を観測した（2026-10-30 の記録）。記録の default 着地は未確認のため、本段階は verifying とする。WP ID と根拠は [milestones.md](milestones.md) を参照。
3. **上流同期の準備** — 自動追従は行わない。所有者の明示指示がある時だけ既存の手順で分割する。

## 停止時評価 — 2026-11-18

- 制御平面の観測は `run-5707669ae112` / `prod-conservative` / `failed`、理由 `unknown`。関連する ComfyUI dispatch run `20261118-173303-344644` の評価入力と worker 報告では、期限を過ぎたと誤認して読み取り専用の実行可能性調査を選び、その定義を記録した後に実際の期限内と訂正している。それでも元の bounded-improvement mission とは記録済み定義の範囲が違うため、改善作業・テスト・commitを行わず終了したと報告されている。
- したがって最も具体的な確認結果は、期限の誤認に続く選択タスクの範囲不一致であり、ComfyUI のコード、CI、または実行資源の障害を示す証拠はない。ただし、制御平面の失敗理由を独立して裏付ける outcome 詳細は確認できていないため、制御平面上の reason は `unknown` のまま扱う。
- 目的・既存 milestone は変更せず計画を維持する。未解決依存は、制御平面に独立した失敗分類がないことと、元 mission が未実行であること。停止解除や runtime 再起動は本リポジトリの権限外。
- 再開条件: TAS が既存経路で元の bounded-improvement mission を新しい dispatch として発行し、deadline を UTC で確認したうえで、記録する選択タスクを元 mission の候補選定・1件実行・検証・commit の範囲に一致させる。次の約30分作業はその新 dispatch で LOOP の候補順を確認して最初の適格候補を一つ完了すること。受入条件は当該候補の指定検証が成功し、変更が1 commitにまとまり、push/deployを行わないこと。現在の製品計画の直近 WP-A2 はこの再開を理由に変更しない。

## 更新規則

charter を唯一の目的・マイルストーン正本とし、実行分解、計画入口、`REPO_METADATA.json` を同じ変更で整合させる。観測できない受入条件や参照の鮮度は pending/unknown とし、過去値や未着地ブランチを現在の完了根拠にしない。
