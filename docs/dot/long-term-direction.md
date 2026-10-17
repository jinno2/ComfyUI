# ComfyUI — 長期方針の見直し

<!-- BEGIN: GENERATED -->

計画確認日: 2026-10-17（UTC）。基準: ComfyUI worktree HEAD `33dce3db`
（branch `ai/ComfyUI/instruction-20261017-184230-709258`）/ 参照 `origin/main` `4c0788db`。
文書の役割: 既存正本（[`PURPOSE.md`](../../PURPOSE.md) / [`.concept/charter.yml`](../../.concept/charter.yml) /
[`LOOP.md`](../../LOOP.md) / [`AGENTS.md`](../../AGENTS.md) /
[`AUTOMATION.md`](../../AUTOMATION.md)）のレビュー索引である。
**目的・AC・作業一覧の正本を本ファイルに作らない** — 現行の実行波は
[milestones.md](milestones.md)、Dot の指示書は [worker-instructions.md](worker-instructions.md) が正本。

## 目的と変更してはいけない条件

- 目的: 上流 comfyanonymous/ComfyUI のローカル fork を、画像生成研究のためにローカルで安定稼働させ続ける
  （出典: [`.concept/charter.yml`](../../.concept/charter.yml) `product_goal.north_star` —
  値に「（推定）」と明記されており、所有者確認は未了）。
- 最終的な成果と判定範囲: `make test` が green であることと、fork 固有コミット数が
  新鮮計測で把握されていること（charter `MET-001` / `MET-002`）。
- 保護制約・資源・権限: LOOP.md の禁止事項（push / 履歴改変 / リリース / deploy / 秘密の読み出し /
  1 run で 2 つ目の改善に着手）と不変条件 `INV-LOOP-001` / `INV-LOOP-002` / `INV-GATE-001` /
  `INV-STYLE-001`（出典: [`LOOP.md`](../../LOOP.md), [`.concept/invariants.yml`](../../.concept/invariants.yml)）。
  AGENTS.md の `No Internet Requests` は core ComfyUI への外向き通信追加を恒久に禁じる。
- 他担当/外部システムとの責務境界: 開発 dispatch と再試行・停滞検知は TAS 制御平面、
  lint / 単元テスト gate は Woodpecker（出典: [`AUTOMATION.md`](../../AUTOMATION.md)）。
  upstream 取り込みは所有者の明示指示時のみ（同行）。worktree/branch の後処理は TAS の責務（同行）。

## 全体構造と現在地

|実際の経路/責務|コード・契約|実装/受入/運転の状態|証拠と観測日|残る原因|
|---|---|---|---|---|
|自律改善の実行単位（1 run = 1 改善）|[`LOOP.md`](../../LOOP.md) / `INV-LOOP-001`|運転確認済み|TAS timer 有効、Woodpecker 有効、GitHub Actions 無効（AUTOMATION.md「Status」2026-09-27）|—|
|変更前ゲート `make test`|`Makefile:451`（`python -m pytest tests-unit -v`）/ `INV-GATE-001`|**運転確認済み（局所領域）／実証待ち（完走）**|2026-10-17T07:44-08:11Z の full run が video transcode まで error/failure なしで通過したが、40 分予算で `EXIT=143`（`.concept/claims.ndjson` run `2026-10-17T08:11:00Z`）|スイート wall time が 1 run の予算を超過。CI は `--maxfail=1`、ローカル `make test` は無指定のため差も未判定|
|CI gate（lint + 単元テスト）|`.woodpecker.yml`（`ruff check .` と `pytest tests-unit -q --maxfail=1`）|運転確認済み（push/PR で発火）|`.woodpecker.yml` `when:` ブロック（2026-10-17T18:45Z 読取）|—|
|fork 固有コミット数の可視化|charter `MET-002` / `AUTO:ForkUpstreamSync.count:git_recency`|証拠不足（文書側が古い）|実測 40（`git rev-list --count a402fd40^2..HEAD`, 2026-10-17T18:47Z）。文書値は `docs/CODEBASE_ANALYSIS.md:5` = 13件（2026-09-20 観測）、`docs/llm-wiki/index.md` = 約20 commits / 先行515（2026-09-26 観測）|実測値を反映する wiki / 分析 doc の更新が未実施|
|上流との同期状況|`git rev-list --count HEAD..up/master`|証拠不足（参照が陳腐化）|0（2026-10-17T18:47Z 実測）。`.concept/decisions.md` は tip `f6c162dd`(2026-06-23) を stale と記録、`docs/llm-wiki/index.md` の「先行 515」は現在成立しない|`up/master` リモート ref の fetch 戦略が未定義|
|コードの不変条件・設計規約|[`AGENTS.md`](../../AGENTS.md)（387 行）|実装済み・運転確認済み|上流 fork 由来、fork 固有の改変なし（`git diff --stat` は docs 追加のみ）|—|
|ソース内 TODO/FIXME|LOOP.md 候補源 #2|証拠不足（優先度付けなし）|205 件（2026-10-17T18:50Z grep）。大半は upstream 由来の調査メモで、fork の改善候補として未選定|候補選定表が無い|
|文書と実装の不一致|LOOP.md 候補源 #3 / charter `MS-003`|未着手（本次計画の対象）|上記 fork 件数の3文書不一致、`docs/llm-wiki/index.md` の upstream 記述 2 箇所|`MS-003` が charter で `planned` のまま|

## 以前の計画から変える判断

|以前の前提・順序|最新の事実|維持/変更/後回し/理由・影響先|
|---|---|---|
|`docs/llm-wiki/index.md`「fork 固有は約 20 commits」「先行 515」（2026-09-26 観測）|fork 固有 40（2026-10-17T18:47Z 実測）。`HEAD..up/master` = 0|**変更**。履歴値はその観測日と併記して保持し、現行値への pointer を置く。影響先: `docs/llm-wiki/index.md`、`docs/llm-wiki/log.md`、charter `MET-002` の達成判定材料。docs の役割は複製ではなく圧縮なので、値の所在は git 計測に委ね、正本には pointer だけ置く|
|`docs/CODEBASE_ANALYSIS.md:5`「フォーク独自コミットは13件」（2026-09-20 観測）|同上|**変更**。日付付きで現行値へ更新。分析 doc の他章は上流fork 内容の話なので触らない|
|`AUTO:UnitTestGate.scope:unit_only`（gate は `make test` のみ、integration は任意）|`make test` の wall time が 40 分超で未完走|**維持**（gate の定義は変えない）。ただし「gate が 1 run 予算内に収まる」ことは未検証であり、次の実行波把它を測定する（→ `milestones.md` MS-D1）。TTL 20 runs 到達前に失効予定なので、**維持判断の再確認は次の実行波の起点**にする|
|TAS が `make test` を 1 run 内で完走できる前提（LOOP.md「1 run は 15〜30 分が目安」）|2026-10-17 の full run は 40 分で中断|**変更**。ゲート完全走査の完走判定は専用の長時間枠（起動と回収を分離）で取り、1 run 内の通常改善とは別管理にする。影響先: `LOOP.md` の時間分割規則 [`milestones.md`](milestones.md) MS-D1|
|upstream への自動追従|upstream `up/master` は HEAD に完全包含（lag 0）|**維持**（charter non-goals「upstream への push/PR/issue 操作」、AUTOMATION.md「明示指示時のみ取り込み」）|—|
|GitHub Actions 無効化|`AGENTS.md` / AUTOMATION.md の記述と `.github/workflows/` の残存が不一致の可能性|**後回し**。本次の業務外の追加調査であり、D1 の成果が出るまで再評価しない|

## 到達状態から逆算した段階

|段階|利用者が得る成果|必要な証拠|未達原因・依存|次の実行波に進む条件|
|---|---|---|---|---|
|S1 変化の安全性|「1 run の改善は既存 gate を壊さない」という主張を裏付ける|`INV-GATE-001` の test evidence、直前の green run|完走 run が無い（40 分で中断した記録のみ）|**進行中**。MS-D1 の成果で判定|
|S2 現在地の可信度|fork 固有コミット数と上流 lag を文書と実際の両方で説明できる|新規 git 計測値と、その値の pointer を置いた文書|文書の値が 13 / 20 / 515 と陳腐化|**進行中**。MS-D1 の成果で判定|
|S3 実行可能性|次の改善（LOOP.md の候補 1〜3）が「どのファイルに何を」まで解決済みの具体的作業として提示できる|候補選定表（候補源・採用理由・対象外理由）|TODO/FIXME 205 件の優先度付けが未実施|**未着手**。S1/S2 の判定後に分割する。遠い段階の実装詳細はこの時点では創作しない|

目的・保護条件と既存正本の役割を守ったまま、S3 の詳細は入力が確定した時に分割する。
目的・保護条件以外の計画を変えるときは理由、影響する依存、再検証範囲を
[milestones.md](milestones.md) と `.concept/claims.ndjson` に残す。

<!-- END: GENERATED -->
<!-- BEGIN: HUMAN -->
<!-- END: HUMAN -->