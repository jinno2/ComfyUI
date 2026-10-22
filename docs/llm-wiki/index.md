# LLM Wiki

長期圧縮コンテキスト。原則: contracts `llm-wiki-discipline`（手本: defuddle
`docs/llm-wiki/`）。正本を複製せず、検証済み知識を出典付きで圧縮する。

## Verified Knowledge

- 成果物: 上流 comfyanonymous/ComfyUI（モジュラー型 AI コンテンツ生成エンジン）のローカル fork/ワーキングコピー。README は上流本文のまま。（出典: README.md、上流 GitHub リポ表示）
- カスタマイズ: fork 固有コミット数は自律ループの作業で増え続けるため、現行値は `git rev-list --count a402fd40^2..HEAD` で都度計測する（2026-09-26 観測 20、2026-10-22T05:10Z 観測 43、2026-10-22T20:18Z 観測 48）。2026-10-22T20:18Z のローカル `up/master`（f6c162dd、2026-06-23）比較は ahead 543、lag 0。この ref は stale で upstream の最新状態を示さない。fork 固有の内容: Makefile 標準化とクロスプラットフォーム対応、Woodpecker gate 追加と upstream テスト workflow のガード、safe_linear のデバイス別フォールバック、seedvr2 テスト順依存修正、CODEBASE_ANALYSIS.md・AUTOMATION.md。（出典: git a402fd40^2..HEAD 計測 / 2026-09-26 fork カスタマイズ調査）
