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
