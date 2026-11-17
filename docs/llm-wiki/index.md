# LLM Wiki

長期圧縮コンテキスト。原則: contracts `llm-wiki-discipline`（手本: defuddle
`docs/llm-wiki/`）。正本を複製せず、検証済み知識を出典付きで圧縮する。

## Verified Knowledge

- モデルプレビューの検索はパス全体を `glob.escape` し、モデル名・格納先の `[]`・`?`・`*` を文字として扱う。対応画像と safetensors 内のカバー画像をHTTP応答の画素で確認し、既存のパス・symlink防御も検証。出典: [`get_model_previews`](../../app/model_manager.py)、[回帰テスト](../../tests-unit/app_test/model_manager_test.py)、[検証記録](log.md#2026-10-23--モデルプレビュー検索でglob特殊文字をリテラルに扱う)。`?`・`*` を含むファイルの実検証はLinux上（Windowsでは作成不可）。

- `set_area_to_bounds` resolves mask bounds across the sampler's latent dimensions. The resulting area stores sizes followed by offsets; leading dimensions keep a minimum size of 1 and the final two spatial dimensions keep the existing minimum of 8. An all-zero mask remains a no-op. See [`resolve_areas_and_cond_masks_multidim`](../../comfy/samplers.py), [regression tests](../../tests-unit/comfy_test/test_sampler_masks.py), and [verification record](log.md#2026-10-24--multidimensional-sampler-mask-bounds).

- `safe_linear` の全 GPU 一括切替と「テストゼロ」という旧指摘は解消済み。現行のデバイス別状態・エラー解放先と6件の CPU・モック回帰テスト、実機検証の限界は [解析文書の2.2節](../CODEBASE_ANALYSIS.md#22-モデル管理サンプリング層) を参照（2026-10-23、コードとテストを照合）。

- 成果物: 上流 comfyanonymous/ComfyUI（モジュラー型 AI コンテンツ生成エンジン）のローカル fork/ワーキングコピー。README は上流本文のまま。（出典: README.md、上流 GitHub リポ表示）
# LLM Wiki

長期圧縮コンテキスト。原則: contracts `llm-wiki-discipline`（手本: defuddle
`docs/llm-wiki/`）。正本を複製せず、検証済み知識を出典付きで圧縮する。

## Verified Knowledge

- モデルプレビューの検索はパス全体を `glob.escape` し、モデル名・格納先の `[]`・`?`・`*` を文字として扱う。対応画像と safetensors 内のカバー画像をHTTP応答の画素で確認し、既存のパス・symlink防御も検証。出典: [`get_model_previews`](../../app/model_manager.py)、[回帰テスト](../../tests-unit/app_test/model_manager_test.py)、[検証記録](log.md#2026-10-23--モデルプレビュー検索でglob特殊文字をリテラルに扱う)。`?`・`*` を含むファイルの実検証はLinux上（Windowsでは作成不可）。

- `set_area_to_bounds` resolves mask bounds across the sampler's latent dimensions. The resulting area stores sizes followed by offsets; leading dimensions keep a minimum size of 1 and the final two spatial dimensions keep the existing minimum of 8. An all-zero mask remains a no-op. See [`resolve_areas_and_cond_masks_multidim`](../../comfy/samplers.py), [regression tests](../../tests-unit/comfy_test/test_sampler_masks.py), and [verification record](log.md#2026-10-24--multidimensional-sampler-mask-bounds).

- `safe_linear` の全 GPU 一括切替と「テストゼロ」という旧指摘は解消済み。現行のデバイス別状態・エラー解放先と6件の CPU・モック回帰テスト、実機検証の限界は [解析文書の2.2節](../CODEBASE_ANALYSIS.md#22-モデル管理サンプリング層) を参照（2026-10-23、コードとテストを照合）。

- 成果物: 上流 comfyanonymous/ComfyUI（モジュラー型 AI コンテンツ生成エンジン）のローカル fork/ワーキングコピー。README は上流本文のまま。（出典: README.md、上流 GitHub リポ表示）

- カスタマイズ: fork 固有コミット数は自律ループ作業で変わるため、現行値は `git rev-list --count a402fd40^2..HEAD` で都度計測する。記録された値には、2026-09-26の20、2026-10-22T05:10Zの43、2026-10-22T20:18Zの48がある（最後の計測時点のローカル `up/master` は ahead 543 / lag 0）。別の2026-10-21調査では `a402fd40^2..HEAD` が20、`up/master..HEAD` が515で、その大半は upstream merge による上流新規と記録された。計測範囲・時点が異なる値を混同しない。`up/master` は f6c162dd（2026-06-23）の古い参照で、これらの比較は現在の upstream 状態を示さない。fork 固有の内容: Makefile 標準化とクロスプラットフォーム対応、Woodpecker gate 追加と upstream テスト workflow のガード、safe_linear のデバイス別フォールバック、seedvr2 テスト順依存修正、CODEBASE_ANALYSIS.md・AUTOMATION.md。（出典: git 計測 / 2026-09-26 fork カスタマイズ調査、2026-10-21調査。計測時は `git rev-list --count a402fd40^2..HEAD`、`git rev-list --left-right --count origin/main...HEAD`、`git rev-list --count HEAD..up/master`、`git log -1 --format=%H up/master` を実行）

- 計画スパイン: 長期方針の見直し・約30分の実行波・Dot 向けワーカー指示書は `docs/plan/`（long-term-direction.md / milestones.md / dot-worker.md）。ゴールの正本は charter のまま、見直し記録と実行波のみを保持。（出典: docs/plan/、2026-10-21 @ 4c0788db 観測）
# LLM Wiki

長期圧縮コンテキスト。原則: contracts `llm-wiki-discipline`（手本: defuddle
`docs/llm-wiki/`）。正本を複製せず、検証済み知識を出典付きで圧縮する。

## Verified Knowledge

- モデルプレビューの検索はパス全体を `glob.escape` し、モデル名・格納先の `[]`・`?`・`*` を文字として扱う。対応画像と safetensors 内のカバー画像をHTTP応答の画素で確認し、既存のパス・symlink防御も検証。出典: [`get_model_previews`](../../app/model_manager.py)、[回帰テスト](../../tests-unit/app_test/model_manager_test.py)、[検証記録](log.md#2026-10-23--モデルプレビュー検索でglob特殊文字をリテラルに扱う)。`?`・`*` を含むファイルの実検証はLinux上（Windowsでは作成不可）。

- `set_area_to_bounds` resolves mask bounds across the sampler's latent dimensions. The resulting area stores sizes followed by offsets; leading dimensions keep a minimum size of 1 and the final two spatial dimensions keep the existing minimum of 8. An all-zero mask remains a no-op. See [`resolve_areas_and_cond_masks_multidim`](../../comfy/samplers.py), [regression tests](../../tests-unit/comfy_test/test_sampler_masks.py), and [verification record](log.md#2026-10-24--multidimensional-sampler-mask-bounds).

- `safe_linear` の全 GPU 一括切替と「テストゼロ」という旧指摘は解消済み。現行のデバイス別状態・エラー解放先と6件の CPU・モック回帰テスト、実機検証の限界は [解析文書の2.2節](../CODEBASE_ANALYSIS.md#22-モデル管理サンプリング層) を参照（2026-10-23、コードとテストを照合）。

- 成果物: 上流 comfyanonymous/ComfyUI（モジュラー型 AI コンテンツ生成エンジン）のローカル fork/ワーキングコピー。README は上流本文のまま。（出典: README.md、上流 GitHub リポ表示）

- カスタマイズ: fork 固有コミット数は自律ループ作業で変わるため、現行値は `git rev-list --count a402fd40^2..HEAD` で都度計測する。記録された値には、2026-09-26の20、2026-10-22T05:10Zの43、2026-10-22T20:18Zの48がある（最後の計測時点のローカル `up/master` は ahead 543 / lag 0）。別の2026-10-21調査では `a402fd40^2..HEAD` が20、`up/master..HEAD` が515で、その大半は upstream merge による上流新規と記録された。計測範囲・時点が異なる値を混同しない。`up/master` は f6c162dd（2026-06-23）の古い参照で、これらの比較は現在の upstream 状態を示さない。fork 固有の内容: Makefile 標準化とクロスプラットフォーム対応、Woodpecker gate 追加と upstream テスト workflow のガード、safe_linear のデバイス別フォールバック、seedvr2 テスト順依存修正、CODEBASE_ANALYSIS.md・AUTOMATION.md。（出典: git 計測 / 2026-09-26 fork カスタマイズ調査、2026-10-21調査。計測時は `git rev-list --count a402fd40^2..HEAD`、`git rev-list --left-right --count origin/main...HEAD`、`git rev-list --count HEAD..up/master`、`git log -1 --format=%H up/master` を実行）

- 計画スパイン: 長期方針の見直し・約30分の実行波・Dot 向けワーカー指示書は `docs/plan/`（long-term-direction.md / milestones.md / dot-worker.md）。ゴールの正本は charter のまま、見直し記録と実行波のみを保持。（出典: docs/plan/、2026-10-21 @ 4c0788db 観測）

- 実行用マイルストーン索引: `docs/MILESTONES.md` が charter の MS-001..MS-003 を Outcome / Acceptance / Evidence / Status・依存・次の一手の形で実行可能な分解として持ち、正本 `REPO_METADATA.json` は charter と `docs/plan/milestones.md` の投影（source_hash は git blob ID）。charter MS-003 の deliverables は 2026-11-03 に追跡3ファイル構成へ修正。計画は「default に着地した証拠」と「未着地ブランチにのみ存在する証拠」を区別して記述し、未着地の受入証拠で milestone を達成扱いしない。（出典: docs/MILESTONES.md、.concept/charter.yml、REPO_METADATA.json、2026-11-11 観測）

- WP-A1 受入証拠: alembic 連鎖 0001..0008 は空の一時 SQLite DB に exit 0 で全適用され、単一 head `0008_missing_content_age` に一致（隔離 ini、`user/comfyui.db` 不使用）。証跡は `docs/plan/evidence/wp-a1-alembic-chain.md`。旧 run 20261107-233514-229391 の証拠窓欠損（authorized_observation は構造的に検証不能）に対する recovery で永続化。（出典: docs/plan/evidence/wp-a1-alembic-chain.md、run 20261107-235007-331852 実測）

- Q3 test-inventory audit (2026-10-23 snapshot, before the API logger regression tests): a source qualifies when a `test_*` function/method contains `assert`, a unittest `assert*` call, `pytest.raises`, or `pytest.fail`. This syntactic rule includes helper/tooling tests that assert behavior; it measures extraction eligibility, not invariant coverage. All 188 Python test sources at that audit have a recorded file hash, test symbol, and expectation line(s). Only 1/188 files were referenced by invariants, below 50%. Later test additions are outside that snapshot. See [the per-file audit](test-constraint-inventory.ndjson) and `.concept/ontology_metrics.json`.
