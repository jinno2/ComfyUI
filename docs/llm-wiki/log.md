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

## 2026-10-30 — charter MS-003 を現 .concept 追跡構成へ整合（WP-C1）

milestones.md 実行波 WP-C1。820d2ae4 (#43) 後の実態に合わせ、charter MS-003 の deliverables を「固定 14 ファイル構成」から手管理シード 3 ファイル（charter.yml / autopilot.yml / ontology_budget.yml）+ 生成ランタイム非追跡ガード（tests-unit/concept_metadata_tracking_test.py）へ更新した。intent の不存在参照（autopilot 品質基準 Q1-Q8 — 現行 autopilot.yml には存在しない）も除去。status は継続活動のため active のまま。

- **Verification**: `git ls-files .concept`（3 seeds）と deliverables 記載の一致、`.venv/bin/python -c "import yaml; yaml.safe_load(open('.concept/charter.yml'))"` 成功、`pytest tests-unit/concept_metadata_tracking_test.py` 15 passed。

## 2026-10-30 — S2 実行波（LOOP 接続の評価）を milestones.md に再計画

S1 波（M-A/M-C）の完了条件「完了後に S2（LOOP 接続の評価）を次の波候補として再計画する」に従い、docs/plan/milestones.md に S2 波を WP-S2-1（LOOP run の plan 由来候補接続の評価）/ WP-S2-2（評価結果に応じた維持・是正方針の確定）として定義した。long-term-direction.md の現在地・段階表を「S2 再計画待ち」から「S2 計画済み・実行待ち」へ更新。本再計画自体が、plan 完了条件由来の候補を LOOP run が拾った最初の証拠となり、WP-S2-1 の判定入力になる。

- **Verification**: `.concept/charter.yml` の yaml parse 成功（docs-only 変更で charter 無影響）、milestones.md の S2 依存（WP-S2-1 → WP-S2-2）と long-term-direction.md 段階表 S2 行の突合、S1 全 WP 着地 commit の確認（d633a060 / 1d188bb9 / c102509a / 07ab2fba を git log で実在照合）。
