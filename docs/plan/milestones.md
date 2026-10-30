# ComfyUI fork — マイルストーンと小作業

<!-- BEGIN: GENERATED -->

計画基準: 2026-10-21 13:05 WAT / 4c0788db9379bfe8013093b8339436b0175622c4。S2 波の再計画: 2026-10-30（S1 波 M-A/M-C の全 WP 着地後）。
長期方針: [.concept/charter.yml](../../.concept/charter.yml)（見直し記録は [long-term-direction.md](long-term-direction.md)）。実装・受入正本: AGENTS.md、LOOP.md、app/assets/database/、alembic_db/。
専任ワーカー: [dot-worker.md](dot-worker.md)。
状態はこの基準時点の観測であり、実行時にmain/PR/runから再確認する。

## 構造と実行する範囲

実行経路と責務の対応は long-term-direction.md の「全体構造と現在地」が正。現在の実行波は S2（LOOP 接続の評価）で、S1 波（M-A/M-C）は全 WP 着地済み（WP-A1/A2: c102509a、WP-C1: 1d188bb9、WP-C2: d633a060）のため触らない。S2 は charter MS の受入作業ではなく、長期方針段階表の「LOOP の候補選択が plan の残課題を拾う」の評価と確定に限定する。他担当の進行中 PR（#42 #41 #35 #33 #31）の範囲には着手しない。

## マイルストーン

|ID|利用者が得る能力・成果|対象WP|完了ゲート|標準作業枠|
|---|---|---|---|---|
|M-S2|LOOP の候補選択が plan の残課題を拾うことが証拠付きで判定され、維持・是正方針が確定する|WP-S2-1, WP-S2-2|判定と方針が docs/plan/ に記録され、実際の default へ着地している|2枠|

依存: WP-S2-1 → WP-S2-2 のみ。（S1 波の依存 WP-A1 → WP-A2 は実行済み、WP-C1 と WP-C2 は独立として完了済み。）

独立して進められる作業: なし（S2 波は WP-S2-1 → WP-S2-2 の直列依存。判定記録が S2-2 の入力のため並行進行しない）。
2枠×約30分は標準枠の単純和。外部待ち・追加修正・実走超過は別で、暦時間保証や大ゴールの残工数ではない。

## 作業カード

### WP-S2-1 | LOOP run の plan 由来候補接続の評価（約30分）

- **状態**: done（2026-10-30 実行。判定は本カード直後の「WP-S2-1 判定記録」参照）
- **主旨**: S2 の中核判定。TAS dispatch の LOOP run が docs/plan/（本書の残 WP・「完了と再計画」の後続条件、long-term-direction.md の段階表）を候補源として参照し、plan 由来の残課題を実際に拾っているかを着地済み証拠から評価する。
- **ゴール・成果物**: 判定記録 1 件（接続の有無・根拠 commit/run・不足がある場合の解除条件）を docs/plan/ 内に残す（1 commit）。
- **入力・対象**: 着地済み main の LOOP run 由来 commit（d633a060 / 1d188bb9 / c102509a、S2 再計画 commit）、TAS run の最終出力、LOOP.md の候補順、docs/plan/ の残課題。
- **作業**: 各 run 由来 commit の選択対象を照合し、plan 由来候補が LOOP の候補比較に現れているかを判定表にする。S2 再計画自体が S1 完了条件（plan 由来）を候補として拾った事実も証拠に含める。コード・charter は変更しない。
- **完了条件（事前AC）**: 判定と証拠（commit SHA・参照文書）が記録されている。機能していないと判定した場合は不足内容と解除条件を残し、機能している場合は維持で足りる根拠を記録する。判定だけを MS-0X や charter の done に読み替えない。
- **必要検証・証拠**: 判定表の各根拠が `git log` で実在参照可能なこと。
- **依存・着手条件**: なし。S2 再計画 commit を入力にする。
- **担当・変更範囲**: 読み取り中心。書き込みは docs/plan/milestones.md（判定の記録）または docs/llm-wiki/log.md への追記のみ。
- **待ち・失敗・再開**: run 最終出力が参照不能なら commit 側の着地証拠だけで判定し、限界を記録する。
- **条件付き不要の判定**: なし（S2 の中核）。

#### WP-S2-1 判定記録（2026-10-30 実行）

**判定: 接続は機能している。維持で足りる。** 根拠は下の判定表と集計（2026-10-30 観測）。本判定は charter の MS status（MS-003 等）を done へ読み替えるものではなく、charter は変更していない。

- **評価範囲**: TAS dispatch の `bounded_improvement` stage（LOOP run）で ComfyUI を対象にした run のうち、計画スパイン（`docs/plan/`。465db8db で着地）が正本として存在する 2026-10-23 以降の 14 run。証拠は各 run の `~/ai-hub/runs/<run_id>/claude_stdout.txt`・`accepted_work.json` と main の git log。
- **接続の実体**: 接続は LOOP.md 自体ではなく dispatch mission の指示で成立する。mission は「LOOP.md and all other relevant repository task sources on every selection, including its purpose, plans, issues, specs, source, tests, docs, ...」（各 run の `prompt.md`）を要求し、LOOP.md 10-13 行の候補順（①make test の失敗 ②TODO/FIXME ③README/docs の手順と実装の不一致）自体は計画ソースを含まない。選択は候補源の優先順位ではなく価値・緊急度・依存の比較で決まり、plan は LOOP 項目と同列の追加候補源として扱われる。
- **判定表**:

|run_id|plan 参照|plan 由来候補の比較|選択結果|根拠 commit|着地|
|---|---|---|---|---|---|
|20261023-221515-995678|あり|あり（WP-A1 は環境未達で不選択 → WP-C1 を選択）|WP-C1|ca8d3d82|未着地|
|20261024-042226-078222|あり|あり（WP-C1）|WP-C1|ab1abc55|未着地|
|20261026-153352-460865|あり（docs/MILESTONES.md）|あり（次候補は MS-002 / WP-A1）|調査のみ（venv 不在で waiting）|なし|—|
|20261027-082355-034909|あり|あり（WP-C2）|WP-C2 waiting（venv 不在）|なし|—|
|20261029-230727-883012|あり|あり（WP-C2）|WP-C2|d633a060|着地|
|20261029-233715-643981|あり|あり（WP-A1/WP-A2）|WP-A1+WP-A2|7004c49e|未着地|
|20261030-001418-213762|あり|あり（WP-C1）|WP-C1|1d188bb9|着地|
|20261030-003957-209557|あり|あり（WP-A1/WP-A2）|WP-A1→WP-A2|762c79b3|未着地|
|20261030-010847-523518|あり|あり（M-A）|WP-A1→WP-A2|86cc64fe|未着地|
|20261030-022229-254289|あり|あり（M-A の残作業）|WP-A1→WP-A2|c102509a|着地|
|20261030-024733-230902|なし|なし（docs 不整合 C1-C4 を自発発見）|Woodpecker gate への fork suite 追加|0b46de87|未着地|
|20261030-033123-255278|あり（次波 S2 を認識）|なし（比較対象は plan 由来外の MET-002 整合）|charter MET-002 整合|ce66a68d|未着地|
|20261030-050738-755039|あり|あり（plan 現在地の乖離）|long-term-direction.md の現在地更新|07ab2fba|着地|
|20261030-051929-484490|あり|あり（S1 完了条件由来の S2 再計画）|S2 波の再計画|858c337b|着地|

- **集計**: plan ソース参照 13/14 run、plan 由来候補の比較 12/14 run、plan 由来候補の選択・実行 10/14 run、waiting 2 run（20261026-153352-460865 / 20261027-082355-034909、venv 不在）。着地 5 commit（d633a060 / 1d188bb9 / c102509a / 07ab2fba / 858c337b）はいずれも plan 由来作業の成果物（WP-C2 / WP-C1 / WP-A1+A2 / 現在地反映 / S2 再計画）で、`accepted_work.json` の candidate_sha と一致する。
- **根拠の実在照合**: `git log --no-walk d633a060 1d188bb9 c102509a 07ab2fba 858c337b` で着地 5 commit の実在を確認、`git merge-base --is-ancestor <sha> HEAD` で未着地 7 commit が HEAD に含まれないことを確認。各 run の `accepted_work.json`（`candidate_sha`・`base_sha`・`acceptance_status: passed`）と判定表の run_id 対応を突合。
- **維持で足りる根拠**: 接続は既に実効しており、LOOP.md の候補順（①→②→③）を弱めていない。20261030-033123-255278 は plan の次波（S2）を認識したうえで plan 由来でない候補を選んだが、これは mission の「queue や class が空になるのを待って止めるな／候補源は優先順位の phase gate ではない」指示と整合する挙動であり、接続の欠落ではない。よって (b) LOOP.md の候補源へ docs/plan/ を追加する（管理印 `loop-md:spec v3` の削除＝手動管理切替を伴う owner 判断）は、判定上は必要なし。WP-S2-2 はこの判定を前提に (a) 現状維持／(b)／(c) を確定する作業。
- **観測した gap（いずれも接続の不在ではない）**:
  - G1 重複並列: 同一 plan 由来 WP（MS-002 の WP-A1/WP-A2）へ 3 run（20261029-233715-643981 / 20261030-003957-209557 / 20261030-010847-523518）が同時着手し、3 つの別 commit（7004c49e / 762c79b3 / 86cc64fe）が未着地のまま残る。着地は 1 件（c102509a、run 20261030-022229-254289）のみ。解除条件: dispatch 側で plan 由来 WP の排他 claiming を持ち、同一 WP への同時着手を 1 件に絞る。本波では着手しない。
  - G2 実行環境: plan 由来候補を正当に比較した 2 run が worktree に .venv が無く waiting へ転じた。解除条件: worktree での `make install` または利用可能な既存 venv（docs/plan/dot-worker.md の資源制約に従う）。
  - G3 未着地候補の残置: 未着地 7 commit（ca8d3d82 / ab1abc55 / 7004c49e / 762c79b3 / 86cc64fe / 0b46de87 / ce66a68d）が各 run ブランチに残存。解除条件: harness/TAS 側の landing 判定。
- **判定の限界**: (1) run 出力に残るのは選択理由と実行結果のみで、比較した全候補の一覧は残っていない。(2) 評価範囲は 2026-10-23 以降の `bounded_improvement` stage 14 run。2026-10-21 の 2 run（20261021-180833-628279 / 20261021-180913-784195）は exit 7 で出力なし、2026-10-22 / 2026-10-23 の 2 run（20261022-101456-865799 / 20261023-022407-465770）は別 stage（概念同期）のため対象外。(3) 未着地 commit は着地証拠として数えていない。
- **WP-S2-2 への引き継ぎ**: 判定は (a) 現状維持を支持する。long-term-direction.md の S2 行の現在地更新と WP-S2-2 の完了記録は WP-S2-2 の書き込み範囲で行う（本 WP の書き込み範囲は本節と docs/llm-wiki/log.md のみ）。

### WP-S2-2 | 評価結果に応じた LOOP 候補接続の維持・是正方針の確定（約30分）

- **状態**: done（2026-10-30 実行。方針確定は本カード直後の「WP-S2-2 方針記録」参照）
- **主旨**: WP-S2-1 の判定に基づき、plan 残課題を LOOP 候補集合へ継続的に取り込む経路の方針を確定させる。選択肢: (a) 現状維持 — dispatch 側 mission が「LOOP.md を優先しつつ全候補源比較」を指示しており LOOP.md は生成仕様のまま, (b) LOOP.md の候補源へ docs/plan/ 追加 — 管理印（loop-md:spec v3）の削除＝手動管理への切替を伴う owner 判断, (c) 接続不全時の是正案を owner 判断待ちとして具体化。
- **ゴール・成果物**: 方針の記録 1 件（1 commit）。owner 判断が必要な場合は対象・選択肢・影響・解除条件を文書化する。
- **入力・対象**: WP-S2-1 の判定記録、LOOP.md（管理印の意味）、AUTOMATION.md の driver 構成。
- **作業**: 判定に応じて (a)/(b)/(c) を選定し、理由と次の実行波の候補選択への影響を記録する。(b) を選んでも管理印は削除せず、owner 判断事項として残す。
- **完了条件（事前AC）**: 方針と理由・影響が記録されている。owner 判断待ちは解除条件（owner の方針指示）が明確。
- **必要検証・証拠**: 方針記録が LOOP.md の現行仕様・AUTOMATION.md と矛盾しないことの確認。
- **依存・着手条件**: WP-S2-1 の判定記録。
- **担当・変更範囲**: docs/plan/ 内の文書（および docs/llm-wiki/log.md）。LOOP.md 本体は触らない。
- **待ち・失敗・再開**: owner 判断待ちは解除条件を残して終了できる。他 WP に波及しない。
- **条件付き不要の判定**: WP-S2-1 が接続機能を高確度で確認し、方針に判断余地がない場合は not_needed（根拠を残す）。

#### WP-S2-2 方針記録（2026-10-30 実行）

**確定方針: (a) 現状維持。** WP-S2-1 の判定（接続は機能している・維持で足りる、記録は WP-S2-1 判定記録・commit 8bb2cfcc）をそのまま採用する。owner 判断事項は発生していない。この判定は charter の MS status を読み替えない（charter は変更していない）。

- **(a) を選ぶ理由**: plan ソース参照 13/14 run・plan 由来候補の選択・実行 10/14 run・着地 5 commit がいずれも plan 由来の成果物で、接続は実効済み。接続経路は LOOP.md の候補順ではなく dispatch mission の候補源比較で成立しており、現状維持は LOOP.md の候補順（①→②→③）も管理印仕様も弱めない。(b) は管理印削除＝owner 判断を伴うが、判定上の必要性が観測されていないため起こさない。(c) は接続不全という対象事象が観測されていないため成立しない。
- **観測 gap の扱い（本波では着手しない。次波以降の選択時の待機理由・判断材料）**:
  - G1 重複並列（同一 plan 由来 WP への複数 run 同時着手）: 責任は dispatch 制御平面（tas_autopilot 側）。解除条件: dispatch 側で plan 由来 WP の排他 claiming を持ち、同一 WP への同時着手を 1 件に絞る owner/制御平面判断。本リポの変更対象外。
  - G2 実行環境（worktree に .venv が無く waiting 化）: 責任は runner 側の実行環境運用。解除条件: worktree での `make install` または利用可能な既存 venv（docs/plan/dot-worker.md の資源制約に従う）。
  - G3 未着地候補の残置: 責任は harness/TAS 側の landing 判定。解除条件: landing 判定の運用。本リポの変更対象外。
- **次の実行波への影響**: S2 波は WP-S2-1・WP-S2-2 の記録が完了（着地は harness 担当）。着地後、plan 由来の残課題の有無を確認し、無ければ LOOP の通常候補順へ戻る。S3（上流追従の準備）は所有者の明示指示が前提のため着手しない。G1〜G3 は解除条件が満たされるまで plan 由来 WP の重複着手や venv 依存候補の選択時に待機理由として参照する。
- **検証**: LOOP.md・.concept/charter.yml の無変更（`git diff` で確認、`loop-md:spec v3` 印は残存）。方針記録と AUTOMATION.md の driver 構成（TAS が dispatch と着地を担当、Woodpecker が CI gate）の突合で矛盾なし。long-term-direction.md の現在地更新は本 WP の書き込み範囲で実施済み。

## 完了と再計画

- 1WPは1振る舞い・1課題・1境界。設計が成果のWPを除き、設計だけで実装をdoneにしない。
- pending/ready/in_progress/waiting/done/not_neededを区別する。doneにはACと必要な配達ゲートが要る。
- 長い実走は起動と結果回収を分け、結果未取得はwaiting。完了taskと有効証拠を再利用する。
- 条件付き前段がnot_neededの場合の後段経路: WP-S2-1 が証拠収集不能でも commit 側の着地証拠で判定を試みる（限界を記録）。WP-S2-2 は判定記録が無い場合は waiting。他の WP に波及しない。（S1 波の経路 WP-A1 → WP-A2 は実行済み。）
- 同条件比較が必要な場合の対照取得・判定WP: なし（本波に比較 AC はない）。
- 実行時刻・commit/hash・PR・run・backend等は実行元から取得する。欠測を0で埋めない。
- runtime進捗とraw証拠は 既存の run 最終出力と git commit/PR に置く（新しい台帳・進捗ファイルを作らない）。
- 追加修正片は親WPに束縛し、目的・成果・AC・依存を保つ。無関係なbacklogを増やさない。
- 目的・資源・保護制約を守り、計画変更の理由と影響する再検証を残す。
- 現在の実行波の終了条件: M-S2 の全 WP（2件）の AC を満たし、判定・方針の更新が実際の default へ着地したこと。waiting・失敗・PR 引継ぎだけを完了にしない。完了後は plan 由来の残課題の有無を確認し、無ければ LOOP の通常候補順へ戻る。S3（上流追従の準備）は所有者の明示指示が前提のため、S2 完了でも着手しない。（S1 波 M-A/M-C は全 WP 着地済みで終了。）
- S2 波の進行（2026-10-30）: WP-S2-1 は done（判定記録は上記「WP-S2-1 判定記録」）。WP-S2-2 も done（方針記録は上記「WP-S2-2 方針記録」。確定方針は (a) 現状維持、owner 判断事項なし）。両 WP の記録が揃ったため、M-S2 の完了ゲートの残りは判定・方針の着地（harness 担当）のみ。着地後は「完了と再計画」の終了条件に従い、plan 由来残課題の有無を確認して LOOP の通常候補順へ戻る。gap（G1 排他 claiming / G2 venv / G3 未着地候補）は「WP-S2-2 方針記録」の解除条件つき記録に移管済みで、本波では着手しない。

<!-- END: GENERATED -->
<!-- BEGIN: HUMAN -->
<!-- END: HUMAN -->
