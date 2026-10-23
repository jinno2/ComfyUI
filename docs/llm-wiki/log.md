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

## 2026-10-22 — fork 固有コミット数の pointer 化（Dot D1-2）

docs/CODEBASE_ANALYSIS.md と本 wiki index の fork 数値（13 件 / 約 20 commits・先行 515）を観測日付きの履歴値として明記し、現行値への pointer（`git rev-list --count a402fd40^2..HEAD`）を追記した。値の唯一の所在は git 計測で、文書側は pointer に留める（charter MET-002・CFLT-FORK-001 解決方針に整合）。

- **Verification**: 2026-10-22T05:10Z、worktree efad1d1b で計測: `git rev-list --count a402fd40^2..HEAD` = 43、`up/master..HEAD` = 538、`HEAD..up/master` = 0（up/master f6c162dd 2026-06-23 は merge a402fd40 で完全包含）、`origin/main...HEAD` = 22/12。

## 2026-10-22 — fork 状態の再計測

fork 固有コミット数とローカル upstream ref との差分を最新 HEAD で再計測し、`.concept/` と wiki index の履歴値を更新した。`up/master` は 2026-06-23 の stale ref のため、この ahead 数は upstream の最新状態を表さない。

- **Verification**: 2026-10-22T20:18Z、worktree c6904572 で計測: `git rev-list --count a402fd40^2..HEAD` = 48、`up/master..HEAD` = 543、`HEAD..up/master` = 0（ローカル `up/master` f6c162dd、2026-06-23）。


## 2026-10-23 — Q3 test-inventory evidence audit

Moved the per-file test audit out of `.concept/`, whose schema is a fixed 14-file set, and replaced category-only classifications with a testable eligibility rule. A Python source qualifies when a `test_*` function or method contains `assert`, a unittest `assert*` call, `pytest.raises`, or `pytest.fail`; each of the 188 rows records the source SHA-256, matching test symbol, and exact expectation line(s). This establishes extraction eligibility, not that the invariant has already been captured. The prior 185/188 split excluded three tests without support under that criterion, so Q3 now uses all 188 files. Existing invariant evidence still covers one unique file (1/188, 0.53%); Q3 remains below its 50% target.

- **Verification**: Exact path-set, per-file AST expectation, line and SHA-256 checks passed (188/188); all `.concept` YAML, JSON and JSONL parsed, and its 14 files match the fixed schema. `git diff --check` passed. `rtk test make test VENV_BIN=/home/jinno/ComfyUI/.venv/bin` exited 0; RTK retained only the last five log lines, so this run's output did not include a pytest count.

## 2026-10-23 — concept snapshot cleanup

Removed dated fork-count samples from ontology, invariant, ambiguity, and resolved-conflict SOT records. Historical measurements remain in the append-only claims ledger; the latest observation stays in the decisions cache. Q3 remains 1/188 and FAIL under its active decision; no threshold or coverage claim was changed.

- **Verification**: At HEAD `984d68f4`, `a402fd40^2..HEAD` = 64, `up/master..HEAD` = 559, `HEAD..up/master` = 0. All `.concept` YAML, JSON, and JSONL parsed; 14 `.concept` files remain; budget counts are within limits; `git diff --check` passed. `make test` was interrupted after 20m20s (exit 130), with no pytest summary; no pass/fail result is claimed.
