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

