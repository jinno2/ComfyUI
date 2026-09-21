# ComfyUI フォーク コードベース分析レポート

- 日付: 2026-09-20
- 対象: jinno2/ComfyUI(tracked 961ファイル、Python 約9.3MB ≒ 約230万トークン)
- 手法: 6領域に分解した並列エージェント分析(実行エンジン / モデル管理 / ldm アーキテクチャ / ノード定義 / API ノード / 開発インフラ・フォーク独自部分)。主要指摘8件は本体セッションで実コードを再読して裏取り検証済み(§4)。
- 性格: このフォークはほぼ最新の upstream ComfyUI(最終同期 2026-06-20 頃)。フォーク独自コミットは13件で、実質的に Makefile 群・`scripts/`・`comfy/ops.py` の `safe_linear`・Pipfile/mise・docs のみ。

---

## 0. エグゼクティブサマリ

**総評**: 全体として設計品質は高い。実行エンジンは「単一ワーカースレッド + プロンプト毎の独立イベントループ + `call_soon_threadsafe` 経由の通信」で並行性問題を構造的に回避しており、キャッシュ無効化のセマンティクス(IS_CHANGED 署名、NaN ポイズニング)も堅牢。ノードバリデーション(`execution.py:834-1235`)は型・範囲・循環を網羅する。`comfy/ldm/` の重複は upstream 参照実装との diff 可能性を保つ意図的な戦略で、一概に負債とは言えない。

**一方で、横断的な課題が4系列ある**:

| 系列 | 最重要項目 |
|---|---|
| セキュリティ | API 認証ヘッダが無マスクで平文ログ化(`comfy_api_nodes/util/client.py:701` → `request_logger.py:103`)。/ws の clientId 乗っ取り(`server.py:270-278`) |
| 信頼性 | `prompt_worker` に例外ガードが無く、ワーカー永久死滅 → キュー詰まり(`main.py:337-407`)。`/interrupt` のTOCTOU(`server.py:1136-1148`) |
| フォーク保守性 | `safe_linear` のプロセス全局フラグはマルチGPUで過剰退化(`ops.py:1150/1214`)。マルチGPUcond経路の230行重複(`samplers.py:357`) |
| テスト | 既知レッド1件が `continue-on-error: true` で隠蔽(`test-unit.yml:15`)。`comfy/ldm/` と `safe_linear` のテストゼロ |

---

## 1. リポジトリ全体像

```
規模: Python 9.3MB / 約640k行規模感(主要ファイル: model_base 2549行, model_patcher 2052行,
      model_management 2027行, supported_models 2342行, server.py 1445行, execution.py 1399行)

comfy/            4.04MB  コア(モデル管理・パッチ・サンプリング・ldm・text_encoders)
comfy_extras/     1.52MB  拡張ノード118ファイル(約109がV3 schema方式)
comfy_api_nodes/  1.68MB  外部APIノード36ファイル + リクエスト基盤 util/client.py(990行)
comfy_api/        0.22MB  バージョン付き公開SDK(latest/v0_0_2/v0_0_1)
app/              0.31MB  ユーザ管理・アセット(SQLAlchemy+Alembic)・サブグラフ管理
ルート .py         0.27MB  main / server / execution / nodes / protocol / folder_paths
tests-unit/       0.51MB  61テストファイル(実測 918 passed / 1 failed / 10 skipped / 約30秒)
tests/            0.20MB  統合テスト660件(実サーバ起動型)
blueprints/       3.9MB   サブグラフテンプレートJSON 90個
```

依存の流向: `main` → `server` → `execution` → `comfy_execution.{graph,caching,progress}` → `nodes`(NODE_CLASS_MAPPINGS が全層から参照されるレジストリ)。モデル検出は `comfy/model_detection.py:44-1105` の state_dict フィンガープリント → `supported_models` の `matches()` 照合。

---

## 2. コンポーネント別分析

### 2.1 実行エンジン・サーバ層

**構成**: `prompt_worker`(main.py:312-407)が PromptQueue から取り出し `PromptExecutor.execute` で実行。スケジューリング(`comfy_execution/graph.py`: トポロジカルソート + 非同期ノードの external block)、キャッシュ(`caching.py`: CLASSIC/LRU/NONE/RAM_PRESSURE、RAM圧迫時は OOMスコア = RAM使用量 × 1.3^(世代齢) で退避)、HTTP(`server.py`: aiohttp + /ws)。

**評価**: 非同期ノードの external block 機構(`graph.py:168-176` + `unblockedEvent` 待ち)は単一消費者順序を保ちつつ非同期を許すエレガントな設計。jobs API のTOCTOU処理(`jobs.py:443-488`)は文書化込みで模範的。キャッシュ無効化は健全(検証と IS_CHANGED が prompt dict を**変異させる**点 `execution.py:977-991` と、既知のサブグラフUI値キャッシュ問題 `execution.py:405-408` は疣)。

**重大な欠陥(裏取り済み)**:
1. `prompt_worker` のループ本体に try/except が**存在しない**。想定外の例外が1回でも `e.execute` 外に出るとワーカースレッドが永久死滅し、HTTP はジョブを受け付け続けるが誰も捌かない
2. `/interrupt` は `get_current_queue()` スナップショット → ミューテックス外で `interrupt_processing()` の非原子構造(`server.py:1136-1148`)。ギャップで**別のプロンプトをキャンセルし得る**。原子版 `interrupt_if_running`(`execution.py:1311-1328`)は既に実装済みだが jobs API からしか使われていない
3. DB マイグレーションがマルチプロセスファイルロック取得**前に**走る(`app/database/db.py:151-184`)。同時起動で SQLite マイグレーション競合の可能性
4. /ws は既存 clientId を名乗るだけでソケットを奪取できる(認証なし、`server.py:270-278`)。LAN 露出時は結果/プレビューが偽装者へ流れる
5. 非同期ノードのタスクが永远に解決しないと `unblockedEvent.wait()` がタイムアウト・割り込み不可でパイプラインを恒久ブロック(`graph.py:241-245`)

**性能**: `progress_state` がノードの全ステップ毎にノード状態マップ全体を再送(O(nodes×steps)、`progress.py:160-185`)。`send_sync` は逐次 fan-out のため、読まない websocket クライアント1つが全体の配信を遅延させ得る。

### 2.2 モデル管理・サンプリング層

**構成**: `model_management.py`(デバイス/メモリ権威、VRAMState、pin バジェット)、`model_patcher.py`(共有 nn.Module を clone-fork するパッチ状態管理、LowVramPatch、DynamicVRAM 版 `ModelPatcherDynamic`)、`ops.py`(dtype/fp8/quantized op ファクトリ + フォーク独自 `safe_linear`)、`samplers.py`(cond バッチング、スケジューラ、マルチGPU スレッドプール)。

**評価**: managed-weight 抽象(共有モジュール + `patches_uuid` でフォーク、weakref ライフサイクル)は意図が良いが、`ModelPatcher` は2000行のゴッドクラス。数値衛生は良好(推論結果は fp32 で返す `model_base.py:238`、fp8 書き込みは seeded stochastic rounding)。

**フォーク改変 `safe_linear` の評価(裏取り済み)**: `ops.py:1146-1215`。cuBLAS のリトライ可能エラー2種のみを捕捉(allowlist 方式で保守的、ホットパスのオーバーヘドゼロ、matmul 置換は数学的に同型で数値健全)。問題は:
- `CUDA_LINEAR_FORCE_MATMUL` が**プロセス全局・永続**。マルチGPU対応フォークで、GPU1 の一時的障害が全 GPU の GEMM を恒久退化させる
- `discard_cuda_async_error()` がカレントデバイスに投げるため、テンソルの実デバイスとズレると sticky-error 解放が別 GPU に向かう(推測レベル)
- フォーク最大のリスク改変でありながら**テストゼロ**

**構造的負債**:
- レガシーVRAM管理と DynamicVRAM(AIMDO)の**二重体制**。`ModelPatcherDynamic` は hook 系を `assert False` / 例外で拒否(`model_patcher.py:2035,2041`)し、hooks 付き conds は `CFGGuider` が静かに非 dynamic clone へ委譲(`samplers.py:1197-1198`) — 挙動がサイレントに切り替わる
- `_calc_cond_batch` と `_calc_cond_batch_multigpu` の**約230行重複**、「keep in sync」コメント付き(`samplers.py:357-361`)
- `CastWeightBiasOp.weight_function/bias_function` がクラスレベル可変リスト(`ops.py:406-409`)。インスタンス属性が未設定の経路(特に highvram フルロード)では全モジュールでリスト共有 → クロスモデル汚染の疑い(要ランタイム検証)
- `current_loaded_models`・STREAM・PINNED 系のモジュールグローバルは無ロック(現状はデバイス分離+GIL+queue 同期で安全だが、暗黙の happens-before に依存)

### 2.3 拡散アーキテクチャ実装(comfy/ldm + text_encoders)

**構成**: 147ファイル・約54.8k行・37+ ファミリ毎ディレクトリ。共通カーネルは `optimized_attention` バックエンドディスパッチ(`modules/attention.py`, 49ファイルが利用)と `pick_operations`(`ops.py:1536`)。プラグイン経路: `detect_unet_config`(1060行の if-chain)→ `supported_models.matches()`。

**評価**: 重複(census 測定)は FeedForward 12件、PatchEmbed 7件、TimestepEmbedding 6件、timestep_embedding 関数9件、RoPE apply 8件。ただし**これは意図的戦略** — 各ポートは upstream ベンダーリポジトリのミラーになっておりベンダーリリースと diff できる(`flux/model.py:1` のヘッダコメント)。税はブロック本体でなくヘルパー関数に集中。text_encoder 側は `sd1_clip.py` の基底継承で本物の再利用が機能している。

**実バグ(全て upstream 継承、noqa 付き = 既知の受容済み負債)**:
1. `sub_quadratic_attention.py:170-179` — OOM回復経路が壊れている: try で `del attn_scores` した後、except が未定義の `attn_scores` を参照 → OOM 時に NameError(裏取り済み、`# noqa: F821` 付き)
2. `audio/dit.py:194` — RoPE スケーリング有り時の NameError
3. `audio/autoencoder.py:94` — antialias=True 時の NameError
4. `flux/model.py:268` — 結果を捨てる死んでいる lambda、`:339-341` は zeros 初期化依存の脆弱な順序

**設計リスク**: `supported_models.models` のリスト順が load-bearing(部分集合マッチのため、先に広いクラスがあると後の狭いクラスが影を落とす)。 specificity の強制が何もない。

### 2.4 ノード定義層

**構成**: ノード契約は V2(`INPUT_TYPES`/`RETURN_TYPES`, nodes.py:58-71)と V3(`io.Schema` + `comfy_entrypoint`)の二方言。コア68ノード(nodes.py:2019-2087)+ comfy_extras 118ファイルを**手書き120行リスト**でロード(nodes.py:2340-2477 — 現在ディスクと完全一致は確認済み)。custom node がコア名をシャドウするのは禁止済み。

**評価**: 登録機構は堅実(ファイル毎の失敗分離、トレースバック記録)。バリデーションは中央集権かつ強力。課題:
- 120行のボイラープレートリストは、既に glob 方式の `init_builtin_api_nodes`(nodes.py:2482)が社内実証 — 新ファイル追加忘れが**無音の no-op**になる故障クラス
- `LoadImage` がサイズ不一致フレームを**無音破棄**し(`nodes.py:1734-1735`)、空リストで `torch.cat` し得る(`:1747`)(裏取り済み)
- bare `except:` 5件、`common_upscale` 呼び出し32ファイル、resize ヘルパー独自再実装3件
- 廃止ノードは "(DEPRECATED)" 表示名で意図維持。trailing-space クラス名 `ConditioningAverage `(nodes.py:94)のレガシーハック

### 2.5 API ノード・SDK層

**構成**: 36プロバイダノード(V3で統一)+ `util/client.py`(990行)のリクエスト基盤。リトライ(408/5xx + 429別枠16回、Retry-After 150秒上限)、中断モニタ、presigned 2段アップロード。全プロバイダ呼び出しは `api.comfy.org/proxy/<provider>/...` 経由で**ローカルにサードパーティ鍵は存在しない**設計(良好)。

**評価**:
- **最重要**: `log_request_response` が全リクエストのヘッダ(`Authorization: Bearer` 含む)を無条件・無マスクで `temp/api_logs/*.log` に書き出す(`client.py:701-708` → `request_logger.py:103-104`)(裏取り済み)。ディスク上の平文資格情報経路
- `apis/__init__.py` が209KBなのは datamodel-codegen 生成物(580クラス、`Type1`/`Status2` 等の衝突名、生成元の `filtered-openapi.yaml` がリポジトリ外で再現不能)
- poll 失敗が裸 `Exception`(`client.py:402-405`)で呼び出し側に区別不可能
- `_generate_operation_id`/`_monitor` クロージャの3重実装、アップロード PUT ループが `_request_base` の手書き並行品
- ハードコードの `float(price) * 211` クレジット換算(`client.py:454`)、`openapi.yaml` はローカルサーバ API の文書でプロバイダ API ではない、client/helpers の単体テストゼロ

### 2.6 開発インフラ・フォーク独自部分

**フォーク独自13コミットの内容**: Makefile(528行、macOS launchd / Linux systemd 方針、arm64 venv ガード、torch 2.4 以上への自動更新)、`scripts/generate_one.py`(stdlib-only のワンショット生成)、WAI-ANIMA ワークフロー自動化(`setup-anima`/`smoke-anima`、Civitai トークンは env/`~/.civitai_token` のみで健全、バイト数完全照合)、`safe_linear`。

**評価(実測)**:
- ユニットスイート: **918 passed / 1 failed / 10 skipped / 約30秒**。失敗は `nodes_math_test.py:190` がエラーメッセージ変更に未追従(裏取り: 実行して再現 "expected 'math domain error' / got 'expected a nonnegative input, got -1.0'")
- CI の `test-unit.yml:15` / `test-execution.yml:15` が `continue-on-error: true` — **赤が握り消される**
- `test-launch.yml:16` は Comfy-Org/ComfyUI(本家)を checkout — フォークのコードを検査していない
- **`comfy/ldm/` のテストは皆零**(tests/ tests-unit/ のどこからも import されない)
- Linux `make start` が参照する systemd unit ファイルがリポジトリに存在しない(`Makefile:410`)
- `generate_one.py:102` に `/Users/jinno/ComfyUI/output/...` のハードコード(裏取り済み)
- ComfyUI-Manager が pip パッケージと custom_nodes コピーの**二重導入**
- Pipfile/mise.toml は uv 管理 の .venv と並行する第二の依存源として放置

---

## 3. 統合改善提案(優先度付き)

### High(全体優先度順)

| # | 提案 | 対象 | 種別 |
|---|---|---|---|
| H1 | API リクエストログの `Authorization`/`X-API-KEY`/`Cookie` ヘッダをマスク | `request_logger.py` | upstream 継承(要パッチ or 上流PR) |
| H2 | `prompt_worker` ループを try/except でガード(ログ + `task_done` エラー処理 + 継続) | `main.py:337-407` | upstream 継承 |
| H3 | `/interrupt` を既存の `interrupt_if_running` に置換(コードは実装済み・実証済み) | `server.py:1136-1148` | upstream 継承 |
| H4 | 赤テスト修正(`nodes_math_test.py:190` の期待メッセージ更新)+ fork の CI から `continue-on-error: true` を除去 | `tests-unit/`, `.github/workflows/` | **フォーク対応** |
| H5 | `safe_linear` のフラグをデバイス別 dict 化 + `discard_cuda_async_error` に失敗テンソルのデバイスを渡す | `ops.py:1150/1214`, `model_management.py:1505` | **フォーク対応** |
| H6 | DB マイグレーションをファイルロック取得後に実行 | `app/database/db.py:151-184` | upstream 継承 |
| H7 | `LoadImage`: スキップフレームの警告化 + 全フレーム消失時の明示的エラー | `nodes.py:1734-1747` | upstream 継承 |
| H8 | ldm の F821 潜在クラッシュ3件修正(実装 or 死んだ分岐削除)+ CI に F821 チェック | `sub_quadratic_attention.py:175` ほか | upstream 継承 |

### Medium

- **M1** マルチGPU cond 経路の統合: `_calc_cond_batch`(2.2節)をデバイス戦略注入型の単一関数に(`samplers.py:220/357`)
- **M2** extras 120行手書きリストを sorted glob 化(`init_builtin_api_nodes` と同じ方式、今日ゼロ挙動変更)
- **M3** `CastWeightBiasOp` の可変クラス属性をインスタンス初期化に(`ops.py:406-409`)
- **M4** `progress_state` ブロードキャストの増分化/レート制限(`progress.py:160-185`)
- **M5** `make test` を unit だけの高速デフォルトに、統合テストは `test-all` へ
- **M6** `safe_linear` の最小単体テスト(CPU でフラグ+matmul経路をモニキーパッチ検証)を追加 — フォーク最大リスク改変の唯一の保険
- **M7** `generate_one.py` のパス相対化(`Path(__file__)` ベース)+ systemd unit の同梱または廃止
- **M8** API 型付きエラー階層(`ApiTaskFailed` 等)+ 生成スキーマ層の再現可能化(.provider 毎分割)
- **M9** リクエストランナー統合(アップロード PUT を `_request_base` へ、`_monitor` の単一化)
- **M10** `ModelPatcherDynamic` の hook ギャップ解消(実装 or 明示的エラー化、サイレント委譲の除去)
- **M11** ldm 共通プリミティブ抽出(timestep_embedding ×9、RoPE ×8、FeedForward ×12)— 次に触るモデルから日和見的に
- **M12** `/ws` clientId 乗っ取りへの所有証明(ワンタイムトークン)
- **M13** ComfyUI-Manager 二重導入の解消

### Low

- extras 残り9ファイルの V3 移行 → ローダー/バリデータ二重経路の解消
- `nodes.py` からローダー/レジストリ部分の分離、`node_info`/object_info のキャッシュ化
- 死にコード除去(flux 死蔵 lambda、`map_node_over_list` stub、`IsChangedCache.outputs_cache`)
- bare `except:` 全廃(ruff E722)、`hook_breaker_ac10a0.py` の改名・文書化
- Pipfile/mise.toml の削除または Makefile への統合、blueprint JSON のスキーマ検証
- `supported_models` マッチの specificity 強制(最も具体的な設定を優先)
- 重複 `main, main` ブランチフィルタの清掃、`origin/HEAD` の main 追従

### 戦略的注記(フォークとしての方針)

Upstream 継承の指摘(H1-H3, H6-H8)は「フォークで即パッチ(同期コストと引き換え)」か「上流 PR(いつ取り込まれるか不明)」かの選択を要る。**フォーク対応の4件(H4, H5, M5, M6, M7)は先に実施する価値が明確** — すべて自分のコード・自分のCIであり、upstream 再同期で壊れないから。upstream 継承分は、再同期時のコンフリクトを避けるため原則上流 PR を推奨(特に `server.py`/`main.py` は改変密度が高い領域)。

---

## 4. 検証記録(裏取り結果)

| 指摘 | 検証方法 | 結果 |
|---|---|---|
| 認証ヘッダの平文ログ | `request_logger.py:95-125` と `client.py:699-710` を再読 | ✅ 確認(ヘッダを無マスクでファイル書き出し) |
| prompt_worker に例外ガードなし | `main.py:312-420` の構造確認(try/except の不在) | ✅ 確認 |
| /interrupt のTOCTOU + 原子版未使用 | `server.py:1136-1148` と `execution.py:1311-1330` を再読 | ✅ 確認(docstring が当該バグを自述) |
| safe_linear のプロセス全局フラグ | `ops.py:1140-1220` を再読 | ✅ 確認(`CUDA_LINEAR_FORCE_MATMUL` 全局・永続) |
| sub_quadratic の F821 | `sub_quadratic_attention.py:165-182` を再読 | ✅ 確認(del 後の参照、noqa 付き) |
| LoadImage の無音フレーム破棄 | `nodes.py:1725-1750` を再読 | ✅ 確認(`continue` + 空 torch.cat) |
| ハードコードパス | grep | ✅ 確認(`generate_one.py:102`) |
| 赤テスト1件 | `pytest tests-unit/comfy_extras_test/nodes_math_test.py` を実行 | ✅ 再現(1 failed, 36 passed) |

未検証(報告のまま採用、要ランタイム確認): `CastWeightBiasOp` 共有リスト汚染(静的解析上は妥当)、`discard_cuda_async_error` の非カレントデバイス問題、重複 prompt_id での heapq TypeError。
