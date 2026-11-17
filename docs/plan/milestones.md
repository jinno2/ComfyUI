# ComfyUI fork — 現行実行波

目的・状態の正本: [`.concept/charter.yml`](../../.concept/charter.yml)。長期方針: [long-term-direction.md](long-term-direction.md)。実行用分解: [docs/MILESTONES.md](../MILESTONES.md)。この文書は現在の WP とその依存だけを持つ。

## 現行状態

- 優先順: P1 の MS-002 WP-A2 → P2 の MS-003 WP-C2。両方が charter を更新するため直列に行う。
- WP-A1 は完了。隔離 DB の `upgrade head` と `current` が単一 `0008_missing_content_age` になった証拠は [wp-a1-alembic-chain.md](evidence/wp-a1-alembic-chain.md) にある。
- WP-A2 は main で README と migration の整合、同一候補 test の証拠が未確認。詳細は `docs/MILESTONES.md` MS-002。
- WP-C1 は着地済み（2026-11-03、`eadbeeeb`）。WP-C2 の新鮮な MET-001 実測は未取得。
- WP-S2-1 / WP-S2-2 の記録は、plan 由来候補の参照（14 run 中13）と選択・実行（14 run 中10）を根拠に、TAS dispatch の接続を現状維持とした。追加の LOOP 変更は不要との判断で、LOOP 管理印は変更しない。
- WP-S2 の記録コミット `8bb2cfcc` / `eb51e196` は現在の default HEAD `f3fbf32f` の祖先ではない。記録の実行結果と方針はあるが、default 着地は未確認のため M-S2 は verifying。

## 次の一枠 — WP-A2（約30分）

- 目的: CFLT-ASSETPERSIST-001 の main 上の状態を確認し、MS-002 を証拠に基づいて確定する。
- 作業: `alembic_db/README.md` と versions 0001〜0008 を照合する。必要なら隔離 DB で `alembic upgrade head` / `alembic current` を確認し、同一候補に対する有効な `make test` 結果を確認する。
- Acceptance: migration 実行が exit 0、単一 head が一致、README が実装と一致、同一候補の `make test` が 0 failed。確認できない項目は pending とする。
- 依存: WP-A1 の証拠取得済み。WP-C2 は同じ charter の編集を避けるため後続。
- 完了時: charter と `docs/MILESTONES.md` の MS-002 を証拠に合わせて更新し、metadata formatter を再実行する。

## 後続 — WP-C2（約30分）

- `make test` を一度実行し、passed / failed / skipped と対象 SHA を記録する。MET-001 をその実測へ合わせ、MS-003 の状態は charter の exit criteria と証拠に従って確定する。
- WP-A2 の charter 更新後に着手する。過去の観測値は現在値へ転用しない。

## 計画接続の判定 — WP-S2-1 / WP-S2-2

判定: dispatch の候補比較経路は plan 由来の作業を選択できており、LOOP.md への候補源追加は不要。2026-10-30 の記録では plan 参照 13/14 run、plan 由来候補の比較 12/14 run、選択・実行 10/14 run、waiting 2 run、成果着地 5 commit。WP-S2-1 の結果は `8bb2cfcc`、WP-S2-2 の現状維持方針は `eb51e196` に記録された。default 着地を確認するまでは、この記録を確定完了として扱わない。
