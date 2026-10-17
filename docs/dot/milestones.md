# ComfyUI — マイルストーンと小作業

<!-- BEGIN: GENERATED -->

計画基準: 2026-10-17（UTC） / HEAD `33dce3db`（`origin/main` `4c0788db`）。
長期方針: [long-term-direction.md](long-term-direction.md)。実装・受入正本:
[`LOOP.md`](../../LOOP.md)、[`.concept/charter.yml`](../../.concept/charter.yml)、
[`.concept/invariants.yml`](../../.concept/invariants.yml)、[`AGENTS.md`](../../AGENTS.md)。
専任ワーカー: [worker-instructions.md](worker-instructions.md)。
状態はこの基準時点の観測であり、実行時に main/PR/run から再確認する。

## 構造と実行する範囲

本リポが直接担う責務は「ローカル fork のコードと、その変更可否を判定する単元テスト gate」だけである。
実行driver（dispatch・再試行・停滞検知）は TAS 制御平面が、CI gate（lint + 単元テスト）は Woodpecker が担う
（[AUTOMATION.md](../../AUTOMATION.md)）。Dot はこの 2 つの外側で **変更・計測・文書化だけ**を行い、
driver の設定・通知経路・cron/daemon には触れない。
upstream `Comfy-Org/ComfyUI` への push/PR/issue 操作と deploy は charter non-goals により常に範囲外。

## マイルストーン

|ID|利用者が得る能力・成果|対象WP|完了ゲート|標準作業枠|
|---|---|---|---|---|
|MS-D1|現在の実行波: 「gate が完走するか」と「fork の現在地」が、正本と実際の両方で説明できる状態になる|D1-1, D1-2, D1-3|gate の完走/所要時間が新規計測で確定し、fork 固有コミット数と upstream lag の現行値が文書（pointer）にも反映されている|約90分（3枠）|
|MS-D2|次の実行波: LOOP.md 候補源 1〜3 から「どのファイルに何を」まで解決済みの具体的作業が提示できる状態になる|（未分割）|MS-D1 の各 WP が done で、かつ `AUTO:UnitTestGate.scope:unit_only` の TTL（20 runs）失効前で再確認できたこと|未着手。S3 の到達状態と次の実行波への条件を [long-term-direction.md](long-term-direction.md) が定義済み。**この段階の実装詳細は分割しない**|—|

依存グラフ:

```text
D1-1 ──┐
       ├──> MS-D1
D1-2 ──┘
D1-3 ── depends on: D1-1（所要時間が CAP 式に効くため）
D1-1 ── depends on: なし（ただしホスト負荷の空きを要確認）
D1-2 ── depends on: なし
```

独立して進められる作業: D1-1（計測・長時間を要する）と D1-2（文書更新・短時間）は別々の書き込み先を触るため並行可。
D1-2 は `docs/llm-wiki/` と `docs/CODEBASE_ANALYSIS.md` のみ、D1-1 は `.concept/` と一時ログのみを書き込み、
**競合しない**。D1-3 は D1-1 の成果に依存するため直列。
3枠×約30分は標準枠の単純和であり、暦時間保証でも大ゴール（MS-D2）までの残工数でもない。

## 作業カード

### D1-1 | `make test` フルスイートの完走可否と所要時間を新規計測する（起動と結果を別枠に分ける）（約30分）

- **主旨**: 2026-10-17 の full run は video transcode 領域まで error/failure なしで通過したが 40 分予算で
  `EXIT=143` に切られ、**「`make test` が完走する」ことと所要時間が未検証**のまま残っている
  （`.concept/claims.ndjson` run `2026-10-17T08:11:00Z`）。これが決まらないと `INV-GATE-001` を根拠に
  「既存テストを壊していない」ことを毎回主张できない。
- **ゴール・成果物**: `pytest tests-unit -v` の 1 回フル実行を非同期 job として起動し、
  job の PID / log パス / 開始時刻（UTC）を記録した状態を残し終えること。
  **このWPでは完走も失敗判定も行わない。** 判定は D1-3。
- **入力・対象**: `Makefile:451`（`test: $(PYTHON) -m pytest tests-unit -v`）、
  `.woodpecker.yml` の `unit-tests` step、`tests-unit/`、既存の venv（`make test` が使う `$(PYTHON)`）。
- **作業**:
  1. `make -n test` で実際の pytest コマンドと Python 実体を確定する。
  2. ホストに他の dispatch が走っていないことを既存のプロセス観測で確認する（LOOP.md は他リポの
     並列枠を塞がないことを要求している）。塞がっているなら **起動せず waiting** として次枠へ回す。
  3. リポジトリ外の一時領域（`/tmp`）に log を出力和 `setsid`/nohup でバックグラウンド起動する。
     `timeout` は本 run の残予算を上限にしない。
  4. job ID（PID）と log パスを成果として記録する。**この時点で結果は読まない。**
- **完了条件（事前AC）**: 起動した pytest の PID と log パスが記録され、起動コマンドが
  `Makefile:451` の定義と一致している（`ps -o args` で確認できる）。
- **必要検証・証拠**: `ps -p <PID> -o args=` の実出力、log ファイルの実在とサイズ増加。
- **依存・着手条件**: 依存なし。ただし「ホスト負荷に空きがある」こと（worktree 外でのみ確認する）。
- **担当・変更範囲**: 書き込みは `.concept/claims.ndjson`（1行追記）と一時ログのみ。
  `tests-unit/` `comfy/` 等のコードは**変更しない**。
- **待ち・失敗・再開**: pytest が起動失敗（venv 不在、import error）した場合は例外終了として
  記録し、D1-3 を not_needed にして D1-2 へ進む。job は kill しない。
- **条件付き不要の判定**: `make -n test` が失敗する、または venv が存在しない場合は
  **不要（not_needed）** とし、理由を `.concept/claims.ndjson` に残す。推測で成功扱いしない。

### D1-2 | fork 固有コミット数と upstream lag の現行値を、実測 pointer として文書へ反映する（約30分）

- **主旨**: 文書内の fork 状態が 3 つの異なる観測値として残されている
  （`docs/CODEBASE_ANALYSIS.md:5` = 13件、`docs/llm-wiki/index.md` = 約20 commits / 先行515、
  `.concept/decisions.md` 検証ログ = 37）。charter `MET-002` は「歴史値と混同しない」ことを
  目標に明示しており、正本側が遅れていると次の自律 run が誤った前提で立つ。
- **ゴール・成果物**: git で計測した現行値と観測日を、既存の3文書の該当行に**日付つきで追記し**、
  値がどこで，取得できるか（pointer）が一意に辿れる状態。
- **入力・対象**: `docs/CODEBASE_ANALYSIS.md`、`docs/llm-wiki/index.md`、`docs/llm-wiki/log.md`。
- **作業**:
  1. `git rev-list --count a402fd40^2..HEAD`、`git rev-list --left-right --count origin/main...HEAD`、
     `git rev-list --count HEAD..up/master`、`git log -1 --format=%H up/master` を実行する。
  2. 計測時刻（UTC）と値を記録する。
  3. `docs/CODEBASE_ANALYSIS.md` の「フォーク独自コミットは13件」に、観測日 2026-09-20 の履歴値である
     ことと現行値（pointer: `git rev-list --count a402fd40^2..HEAD`）を追記する。他章には触れない。
  4. `docs/llm-wiki/index.md` の該当2 bullet に、2026-09-26 観測の歴史値であることと
     現行値への pointer を追記する。**陳腐化した数値をそのまま複製しない** — llm-wiki は圧縮コンテキストであり、
     値の所在は git 計測に委ねるため。
  5. `docs/llm-wiki/log.md` に 1 エントリ（検証コマンドと実測値）を追記する。
- **完了条件（事前AC）**: 3 文書のいずれも、fork 固有コミット数について
  「歴史上の観測日と観測日」および「現行値への pointer」の両方を持つ状態。
  数値の唯一の所在は git 計測であり、文書側は pointer に留める。`MET-002` の fresh 計測が再現できる。
- **必要検証・証拠**: 実行した git コマンドと実測出力（欠測を 0 で埋めない）。
- **依存・着手条件**: 依存なし。D1-1 と並行可。
- **担当・変更範囲**: 上記3ファイルのみ。`.concept/` は D1-1 が使うため触らない（共有書き込みの競合回避）。
- **待ち・失敗・再開**: `a402fd40` が解決できない場合は「起点 commit 不明」と記録し、
  文書更新を保留して理由を残す。upstream ref の fetch 戦略（`up/master` が stale）は
  本WPの範囲外 — 記録のみ。
- **条件付き不要の判定**: 3 文書の該当箇所がいずれも既に pointer 化済みで現行値と矛盾しない場合は
  **不要**。ただし 2026-10-17 時点では 13 / 約20 / 先行515 が未更新なので現時点で該当しない。

### D1-3 | D1-1 の実走結果を回収し、gate の完走可否と所要時間を判定表として記録する（D1-1 完了後）（約30分）

- **主旨**: D1-1 は「起動」而已で、`INV-GATE-001`（既存テストを壊したまま commit しない）を根拠にしうるか
  は判定されていない。job の結果を回収して初めて gate の現状が決まる。
- **ゴール・成果物**: `pytest tests-unit -v` の 1 回フル実行について、
  **所要時間・最終テスト到達点・失敗/エラー件数・exit code** を含む判定表が `.concept/claims.ndjson`
  に 1 エントリとして残ること。
- **入力・対象**: D1-1 が記録した PID と log パス、`.concept/claims.ndjson`（claim 形式は同ファイルの既存行に従う）。
- **作業**:
  1. job が終了しているかを確認し、終了していなければ **waiting** として D1-2/独立作業へ進む
     （`INV-LOOP-001` の「1 run = 1 改善」を壊さない）。
  2. 終了していれば log から exit code・所要時間・最後の reached test・failure/error 件数を抽出する。
  3. 判定: (a) 完走 + 0 failures → `MET-001` の局所実測として「green」、
     (b) 完走 + failures → **赤**. LOOP.md 手順 1 の最優先候補そのものなので、以降の候補選定を止め、
     **最初の失敗を 1 件だけ**直す問題に分解する（1 run で複数改善に着手しない）。
     (c) 未完走 → 結果を記録し、次回は長い実走の**起動と回収を別 run に分ける**運用を候補に残す。
  4. `.concept/decisions.md` の `AUTO:UnitTestGate.scope:unit_only` に、この実測が TTL 到達前に
     合意できるなら、観測時刻を追記して妥当性を再確認する。**判断を変えない。**
- **完了条件（事前AC）**: 上記4項目の値がすべて埋まった claim 行が1件存在する。
  未完走・欠測は 0 や green で補完せず「未完走」「不明」と書く。
- **必要検証・証拠**: 実際の log の該当行と process の終了状態。
- **依存・着手条件**: D1-1 が done（または waiting で job ID が確定）していること。
- **担当・変更範囲**: `.concept/claims.ndjson` と `.concept/decisions.md` のみ。コードは変更しない。
- **待ち・失敗・再開**: job が長時間実行中の場合、blocking wait は60秒以内に留め、
  成果（PID・経過）と解除条件（job 終了）を保存して別 WP へ進む。
  同一原因の再試行は3回で保留し、その後は独立作業へ移る。
- **条件付き不要の判定**: D1-1 が not_needed（起動失敗）なら **不要** とし、
  理由を `LOOP.md` 手順 1 の候補「`make test` の失敗」に再登録する。

## 完了と再計画

- 1WPは1振る舞い・1課題・1境界。設計が成果のWPを除き、設計だけで実装をdoneにしない。
- pending/ready/in_progress/waiting/done/not_neededを区別する。doneにはACと必要な配達ゲートが要る。
  本3 WP はいずれも docs/`.concept/` の記録のみが成果で、`make test`（gate）を通す。
- 長い実走は起動と結果回収を分け、結果未取得はwaiting。完了taskと有効証拠を再利用する。
- 条件付き前段がnot_neededの場合の後段経路: **D1-1 が not_needed → D1-3 は not_needed とし、
  MS-D1 は D1-2 だけで閉じ、未解決事項を `LOOP.md` 手順 1 の候補として明示して残す。**
  D1-2 が not_needed の場合は D1-1 の結果だけを残し、文書変更なしとして中断レポートへ進む。
  どちらの場合も後段が永久に ready にならない依存を作らない。
- 同条件比較が必要な場合の対照取得・判定WP: **現Waveでは不要**。D1-3 は CI（`.woodpecker.yml` の
  `--maxfail=1`）とローカル（`make test` の無指定 maxfail）の比較を**成果に含めない**。
  両者の差が gate の所要時間に効くかは、次の実行波で独立WPとして割り当てる。
- 実行時刻・commit/hash・PR・run・backend等は実行元から取得する。欠測を0で埋めない。
- runtime進捗とraw証拠は既存の [`.concept/claims.ndjson`](../../.concept/claims.ndjson) と
  `.concept/decisions.md` の検証ログに置く。**新しい台帳・driver・ログファイルを作らない。**
- 追加修正片は親WPに束縛し、目的・成果・AC・依存を保つ。無関係なbacklogを増やさない。
- 目的・資源・保護制約を守り、計画変更の理由と影響する再検証を `.concept/claims.ndjson` に残す。
- 現在の実行波の終了条件: **D1-1, D1-2, D1-3 が done または not_needed で、MS-D1 の完了ゲート
  （gate の完走/所要時間が確定し、fork 現状値が pointer として文書反映）が判定できた時点。**
  その時点で MS-D2 への分割は行わず、[long-term-direction.md](long-term-direction.md) の S3 を
  次の水平線として次の run に渡す。

<!-- END: GENERATED -->
<!-- BEGIN: HUMAN -->
<!-- END: HUMAN -->