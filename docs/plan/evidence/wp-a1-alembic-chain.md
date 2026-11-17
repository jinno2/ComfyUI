# WP-A1 受入証跡: alembic マイグレーション連鎖（0001..0008）

- 対象作業: `docs/plan/milestones.md` WP-A1「alembic マイグレーション連鎖の受入確認」
- 執行 run（本証跡作成）: ai-hub run `20261107-235007-331852`（recovery。元 run `20261107-233514-229391` / TAS `run-853297c93e02` は観測実行済みも harness 側証拠窓が無く全 criteria unverified → 本 run で隔離実行を実施し直し証跡をトラックされたファイルとして永続化）
- 観測日時: 2026-11-07T23:53–23:55 UTC / base commit `eadbeeebbf69e3af79c14ef3b66fdd51ef383798`（本証跡ファイル以外に repo 変更なし）
- 環境: mise python 3.13, alembic 1.18.4, SQLAlchemy 2.0.50（`alembic --version` 実測）

## 隔離構成（本番・既存 DB の設定を継承しない）

作業ディレクトリ `/tmp/wp-a1-repair-20261108/` に隔離用 ini を生成して実行
（リポジトリの `alembic.ini` は不使用。`alembic.ini` の
`sqlalchemy.url = sqlite:///user/comfyui.db` を継承していない）:

```ini
[alembic]
script_location = /home/jinno/ComfyUI-aihub-20261107-235007-331852/alembic_db
prepend_sys_path = /home/jinno/ComfyUI-aihub-20261107-235007-331852
sqlalchemy.url = sqlite:////tmp/wp-a1-repair-20261108/wp_a1_acceptance.db
```

- `alembic.ini` sha256: `5f83450cdb8866345625bebb75c459516213930d43ed878cd03088bb135999da`
- `alembic_db/versions/0008_missing_content_age.py` sha256: `7dae51f51e421949b1f2a9cd5933057382c9aa0b1fcea7001548fcc6fb6554cd`

## 実行トランスクリプト（コマンド・exit code・出力）

| # | コマンド（`ISO=/tmp/wp-a1-repair-20261108/alembic_iso.ini`） | exit | 出力 |
|---|---|---|---|
| 1 | `ls /tmp/wp-a1-repair-20261108/wp_a1_acceptance.db`（実行前） | 2 | `No such file or directory` — 空からの開始を確認 |
| 2 | `ls user/comfyui.db`（実行前・後とも） | 2 | `No such file or directory` — 既存 DB は worktree 上に存在せず無読み書き |
| 3 | `alembic -c $ISO heads` | 0 | `0008_missing_content_age (head)`（単一 head） |
| 4 | `alembic -c $ISO upgrade head` | 0 | （出力なし。env.py が logging fileConfig を呼ばないため INFO ログは出ない。適用は下記 stepwise トレースと DB 終状態で証明） |
| 5 | `alembic -c $ISO current` | 0 | `0008_missing_content_age (head)` — heads と一致 |
| 6 | `alembic -c $ISO history` | 0 | `<base> -> 0001_assets` … `0007 -> 0008_missing_content_age (head)` の線形 8 revision |

## per-revision 適用トレース（stepwise upgrade）

upgrade 後に `downgrade base`（exit 0）で戻し、`upgrade +1` を 8 回実行して各段階の
`alembic current` を記録:

```
step 1: exit=0 current='0001_assets'
step 2: exit=0 current='0002_merge_to_asset_references'
step 3: exit=0 current='0003_add_metadata_job_id'
step 4: exit=0 current='0004_drop_tag_type'
step 5: exit=0 current='0005_allow_case_sensitive_tags'
step 6: exit=0 current='0006_add_loader_path'
step 7: exit=0 current='0007_record_content_split'
step 8: exit=0 current='0008_missing_content_age (head)'
```

## DB 終状態（sqlite3 で実測）

- テーブル: `alembic_version, asset_contents, asset_meta, asset_system_state, asset_tags, assets, tags`
  （`app/assets/database/models.py` の 6 テーブル + `alembic_version`）
- `alembic_version` 行: `0008_missing_content_age`
- `asset_contents.missing_at` カラム存在（0008 で追加された列）

## 結論

- AC1: 隔離一時 DB（ファイル実行前不在 = 空）に対し `upgrade head` が exit 0、
  0001..0008 の全 revision が stepwise トレースどおり適用された。
- AC2: `heads` は単一 `0008_missing_content_age (head)`、`current` が同一 revision を示し一致。
- AC3: リポジトリ設定（`user/comfyui.db`）は不使用・同ファイルは実行前後とも不在。
  一時成果物は `/tmp/wp-a1-repair-20261108/` 配下のみ。本 run の repo 変更は本証跡ファイルと
  `docs/llm-wiki/` のログ/索引追記のみ。

## 再現手順

```bash
TMP=$(mktemp -d)
cat > "$TMP/alembic_iso.ini" <<EOF
[alembic]
script_location = <repo>/alembic_db
prepend_sys_path = <repo>
sqlalchemy.url = sqlite:///$TMP/wp_a1.db
EOF
alembic -c "$TMP/alembic_iso.ini" heads
alembic -c "$TMP/alembic_iso.ini" upgrade head
alembic -c "$TMP/alembic_iso.ini" current
```

期待結果: 3 コマンドとも exit 0、`heads`/`current` とも `0008_missing_content_age (head)`。
