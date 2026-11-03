# GoalDev Log

永続的決定と完了記録を追記する。各エントリに日付と検証を必ず付ける
（原則: contracts `llm-wiki-discipline` の log-is-append-with-correction）。

## 2026-09-26 — llm-wiki スキャフォールド

contracts の llm-wiki-discipline 原則に基づき `docs/llm-wiki/` を新設した。

- **Verification**: 原則 `registry/principles/llm-wiki-discipline.yaml`（contracts リポ commit 3ab5768）。

## 2026-09-26 — fork カスタマイズ調査（upstream Comfy-Org/ComfyUI）

参照のある upstream リモートは `up`（upstream リモートは未 fetch で参照なし）のため `up/master` と比較。先行 515 件の大半は a402fd40 の upstream merge による上流新規分で、fork 固有は a402fd40^2..HEAD の 20 commits（jinno author 18 件）。内容: Makefile 標準化・クロスプラットフォーム対応（dev/test/lint/service、launchd 例、WAI-ANIMA セットアップ）、Woodpecker gate 追加と upstream テスト workflow のガード、safe_linear matmul の per-device フォールバック、seedvr2 テストの順依存修正、CODEBASE_ANALYSIS.md / AUTOMATION.md、ブランチ名 master→main 変更。

- **Verification**: git log up/master..HEAD = 515 commits（うち a402fd40^2..HEAD = 20 commits が fork 固有）、jinno author = 18 commits, diff --stat 654 files +174245/-20123。

## 2026-09-26 — 親の確定（jinno確定）
- relations.md の階層関係を草案から確定版へ更新。親: business_operation_notes。
- Verification: contracts registry `organization/repositories/comfyui.yaml` の spec.parent（ecbc226）と突合し一致を確認。

## 2026-10-21 — 計画スパイン新設（dot-milestone-loop 適用、docs-only）

`docs/plan/` に長期方針の見直し・約30分実行波・Dot 向けワーカー指示書を新設した。charter MS-003 の「固定 14 ファイル構成」が 820d2ae4 (#43) 後の追跡 3 ファイル構成と乖離していることを観測し、実行波 WP-C1 で charter 整合を計画。MET-001 の実測（2026-10-10）は観測時点の記録として保持し、再観測を WP-C2 で計画。スキル適用は計画整備までで、Dot の起動は含まない。

- **Verification**: 観測基準 4c0788db9379bfe8013093b8339436b0175622c4。.concept/ 追跡 3 ファイル（ls 実測）、models.py 6 テーブル、alembic versions 0001..0008（本日観測）。テスト実測は未取得（docs-only のため製品 suite は再実行せず、WP-C2 として計画）。

## 2026-11-03 — 長期計画・マイルストーン整備（所有者指示 OI-20261103-32）

所有者の長期計画整備指示に従い、既存の正本（`.concept/charter.yml`）を基準に実行用の分解を整備した。`docs/MILESTONES.md` を新設し、charter の MS-001..MS-003 を `## MS-00X:` 形式（Outcome / Acceptance / Evidence / Status・依存・次の一手）で実行可能な単位として索引化し、直近の約30分枠（WP-A1: alembic upgrade head の実走）を明記した。charter には planning 入口（long-term-direction / milestones / MILESTONES）、各 milestone の depends_on・exit_criteria・next_action・evidence を追加し、旧記載だった MS-003 deliverables「固定 14 ファイル構成」を現構成（追跡3ファイル + runtime 非追跡ガード）へ修正した。`REPO_METADATA.json` は charter と `docs/plan/milestones.md` の投影として source_hash（git blob ID）・updated_at・verified_at を再計算した。

- **Verification**: 指定構造検証スクリプト（`VERIFY_PLANNING`）が `planning structure verified; semantic acceptance remains separate` で exit 0。charter は yaml parse 成功。追跡構成は `git ls-files .concept` で charter.yml / autopilot.yml / ontology_budget.yml の 3 ファイルを確認。
- 未了: MS-002 の alembic 実走証拠（WP-A1）と README 実態一致判定（WP-A2）、MET-001 の再観測（WP-C2）は未実行・未取得。MS-002 / MS-003 は in_progress、MS-001 は achieved（charter status=done と MET-001 記録 2026-10-10 が根拠）。
