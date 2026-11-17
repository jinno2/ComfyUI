# ComfyUI fork — 長期方針

再確認: 2026-11-17（基準: `origin/main` @ `f3fbf32f`）。目的と受入条件の正本は [`.concept/charter.yml`](../../.concept/charter.yml)。本書は現状との差と到達段階を示し、マイルストーン詳細を複製しない。

## 目的と境界

画像生成研究を起点に、画像・動画・3D・音声を扱うモジュラーなノードグラフ型 ComfyUI fork を、上流へ自動追従せず安定提供し続ける（charter の推定 north star）。成功指標は `make test` の失敗ゼロ、Woodpecker CI の green、fork 固有状態の可視化。外部通信、deploy/release、上流への自動追従・操作は非目標。

実装・運用の責務は既存の所有者に従う。ComfyUI はノードグラフと fork 固有変更、TAS は dispatch と着地、Woodpecker は CI、所有者は上流取り込みと driver 変更を担う。権限は現在の task packet が定める。

## 現状と到達点

| ID | 到達点・現状との差 | 状態・根拠 | 優先順・依存・出口 | 次の一手 |
|---|---|---|---|---|
| MS-001 | fork の基盤と CI gate を維持する。標準 Makefile ターゲットと Woodpecker 設定はある。 | achieved。charter の `done`、Makefile、`.woodpecker.yml`。 | P0、依存なし。charter の test と CI gate 条件を維持する。 | 維持。新しい作業は通常候補選択に従う。 |
| MS-002 | アセット永続化の実装はあるが、main 上の README 手順と受入証拠の整合は未確定。WP-A1 の隔離 DB 実行証拠は [`evidence/wp-a1-alembic-chain.md`](evidence/wp-a1-alembic-chain.md) にある。 | in_progress。WP-A2 成果の main 着地と同一候補 `make test` 証拠は未確認。 | P1、WP-A1 → WP-A2。隔離 DB migration、README と versions 整合、同一候補の test acceptance を満たし、charter に証拠を反映する。 | WP-A2 を約30分枠で実施。詳細は [milestones.md](milestones.md)。 |
| MS-003 | `.concept` の追跡構成と runtime 除外は 2026-11-11 に再観測済み。charter の現行値と MET-001 の再観測を揃える作業が残る。 | in_progress。追跡3ファイル、YAML parse 3/3、runtime 12件の check-ignore 12/12（2026-11-11、実行波の記録）。 | P2、構成確認は依存なし。charter の YAML・追跡・除外条件を確認し、MET-001 を新鮮な test run と対象 SHA で記録する。 | WP-C2 は MS-002 の charter 編集後に実施する。 |
| MS-004 | fork 固有コミット数と上流同期状態を新鮮な計測で把握する。現在のローカル upstream ref の鮮度は未確認。 | in_progress。新鮮な計測 claim は pending。 | P1、fresh upstream baseline が必要。charter の ForkUpstreamSync 計測条件を満たす。 | 新鮮な参照を利用できる既存の許可済み作業時に計測し、欠けた入力は unknown のままにする。 |
| MS-005 | docs と実装の不一致を継続して解消する。今回、具体的な未修正の不一致は追加調査していない。 | planned。charter の手動レビュー条件が根拠。 | P2、依存なし。具体的な不一致を特定し、実装と文書を照合して解消する。 | LOOP の通常候補選択で具体的な候補が見つかった時に分解する。 |

MS-001〜MS-005 の定義と状態の正本は charter、実行可能な AC と次の一手は [docs/MILESTONES.md](../MILESTONES.md) に置く。項目の状態は charter の `done` / `active` / `planned` を同ファイルの語彙へ対応させる。

## 計画段階

1. **受入証拠を確定する** — MS-002 の WP-A2 を完了し、MS-003 の現行構成と MET-001 を確定する。共通の charter 更新は直列化する。
2. **計画候補の接続を確認する** — WP-S2-1 / WP-S2-2 の記録は、TAS dispatch が計画候補を比較し、追加の LOOP 変更を要しないという現行方針を示す。14 run 中13 runで計画参照、10 runで計画由来候補の選択・実行を観測した（2026-10-30 の記録）。記録の default 着地は未確認のため、本段階は verifying とする。WP ID と根拠は [milestones.md](milestones.md) を参照。
3. **上流同期の準備** — 自動追従は行わない。所有者の明示指示がある時だけ既存の手順で分割する。

## 更新規則

charter を唯一の目的・マイルストーン正本とし、実行分解、計画入口、`REPO_METADATA.json` を同じ変更で整合させる。観測できない受入条件や参照の鮮度は pending/unknown とし、過去値や未着地ブランチを現在の完了根拠にしない。
