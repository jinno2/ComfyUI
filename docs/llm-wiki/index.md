# LLM Wiki

長期圧縮コンテキスト。原則: contracts `llm-wiki-discipline`（手本: defuddle
`docs/llm-wiki/`）。正本を複製せず、検証済み知識を出典付きで圧縮する。

## Verified Knowledge

- 成果物: 上流 comfyanonymous/ComfyUI（モジュラー型 AI コンテンツ生成エンジン）のローカル fork/ワーキングコピー。README は上流本文のまま。（出典: README.md、上流 GitHub リポ表示）
- カスタマイズ: fork 固有は約 20 commits（jinno author 実測）。Makefile 標準化とクロスプラットフォーム対応、Woodpecker gate 追加と upstream テスト workflow のガード、safe_linear のデバイス別フォールバック、seedvr2 テスト順依存修正、CODEBASE_ANALYSIS.md・AUTOMATION.md。先行 515 の大半は upstream merge による上流新規分。（出典: git log up/master..HEAD 515 commits / a402fd40^2..HEAD = 20 commits）
