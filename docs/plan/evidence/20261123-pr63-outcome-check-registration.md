# PR #63 auto_merge_blocked 調査証跡: required outcome check identity is not registered

- 対象作業: inbox-care `auto_merge_blocked`（PR #63 failed CI at the inspected head）
- 執行 run: ai-hub run `20261122-175820-206928`、worktree `ComfyUI-aihub-20261122-175820-206928`、branch `ai/ComfyUI/instruction-20261122-175820-206928`、base commit `720290fe239977924e5632bd2abf3b1be8c86023`
- 観測日時: 2026-11-23（JST）。gh 認証: `jinno-desktop-new-gh-auth[bot]`（GH_TOKEN）
- 前回試行: 2026-11-21T17:48Z run `20261121-174842-303999` は読み取りのみで証跡文件が無く評価失敗。本証跡は evaluator 指示（出典 excerpt と gh 出力の artifact 化）に沿って再実行したもので、調査結論は同一。

## 1. 結論（root cause）

PR #63 の CI 自体は**成功している**。エラー `required outcome check identity is not
registered for this repository` は、着地ゲートを握る tas_autopilot 側
`post_dispatch.py` が「未登録リポジトリの PR CI」を failed 扱いにする**仕様上の登録漏れ**。
`jinno2/ComfyUI`（本リポの origin slug）が `_REQUIRED_CHECK_CONTEXTS` /
`_REQUIRED_CHECK_RUNS` のいずれにも登録されていないため、CI が green でも
auto-merge が `auto_merge_blocked` となる。一過性の環境問題ではなく、
tas_autopilot リポジトリ側の設定欠落（本リポの外）。

## 2. 証拠（実行コマンドと出力）

### 2.1 PR #63 の CI は green（head 一致）

```
$ gh pr view 63 --repo jinno2/ComfyUI --json number,state,headRefOid,baseRefName,title,statusCheckRollup
{"baseRefName":"main","headRefOid":"f713921686f8971711f667643a248d7bdd9cb8d1","number":63,"state":"OPEN",
 "statusCheckRollup":[{"__typename":"StatusContext","context":"ci/woodpecker/pr/woodpecker",
 "startedAt":"2026-11-21T17:22:43Z","state":"SUCCESS",
 "targetUrl":"https://jinno-desktop.tail796c5f.ts.net/repos/22/pipeline/196/1"}],
 "title":"Land orphaned task branch tas/auto/4b4cfc7bb619"}
```

head は inbox 通報の `f713921686f8971711f667643a248d7bdd9cb8d1` に一致。rollup は
`ci/woodpecker/pr/woodpecker` = SUCCESS の1行のみ（非 pass 行なし）。

### 2.2 ステータスの作成者 = tas-bot

```
$ gh api repos/jinno2/ComfyUI/commits/f713921686f8971711f667643a248d7bdd9cb8d1/status \
    --jq '{combined: .state, statuses: [.statuses[] | {context, state, creator: .creator.login}]}'
{"combined":"success","statuses":[{"context":"ci/woodpecker/pr/woodpecker","creator":null,"state":"success"}]}

$ gh api graphql -f query='query{repository(owner:"jinno2",name:"ComfyUI"){object(oid:"f7139216..."){... on Commit{status{contexts{context state creator{login ... on Bot{login}}}}}}}}'
[{"context":"ci/woodpecker/pr/woodpecker","creator":{"login":"tas-bot"},"state":"SUCCESS"}]
```

REST `combined: success`。GraphQL では creator = `tas-bot`（Woodpecker が tas-bot
アイデンティティで status を投稿）。

### 2.3 PR #63 は CI 宣言ファイルを変更している（判定トリガー）

```
$ git diff --stat 720290fe239977924e5632bd2abf3b1be8c86023 f713921686f8971711f667643a248d7bdd9cb8d1 -- .woodpecker .woodpecker.yml .woodpecker.yaml .github/workflows
 .woodpecker.yml | 26 +++++---------------------
 1 file changed, 5 insertions(+), 21 deletions(-)
```

base→head で `.woodpecker.yml` が変化しているため、下記 `_unregistered_repo_has_pr_ci`
の `declarations_changed.returncode == 1` → `return True`（PR CI を期待）が直接成立する。

### 2.4 発生源: tas_autopilot post_dispatch.py（repo 外・読み取りのみ）

出典ファイル: `tas_autopilot` リポジトリ `tas_autopilot/control_plane/post_dispatch.py`
- sha256: `e5c66eec834b1cf6c12e0a9d11df0d9fa0e5f959f1d6d3d1c8bdaced0c23c5af`
- 同ファイルの最終変更 commit: `26f2974a1` "fix(post-dispatch): refuse merging a PR whose exact head already failed CI (#1794)"

登録テーブル（L1431–L1473 抜粋、`jinno2/*` は存在しない）:

```python
_REQUIRED_CHECK_CONTEXTS = {                       # L1431
    "jinno0/contracts": frozenset({"ci/woodpecker/pr/woodpecker"}),
    "jinno0/tas_autopilot": frozenset({"ci/woodpecker/pr/woodpecker"}),
    "jinno0/ai-hub_agent_proxy": frozenset(
        {"ci/woodpecker/pr/woodpecker"}
    ),
    "nobu007/miyabiprivate": frozenset({"ci/woodpecker/pr/woodpecker"}),
    "co-priv4/agent-pm": frozenset(
        {
            "ci/woodpecker/pr/ci",
            "ci/woodpecker/pr/quality-gates",
        }
    ),
}
_REQUIRED_CHECK_RUNS = {                           # L1444
    "jinno0/ai-hub_agent_proxy": frozenset({("CI", "lint-test-build (20.x)")}),
}
...
_REQUIRED_CHECK_CONTEXT_PRODUCERS = {              # L1452
    "jinno0/contracts": {"ci/woodpecker/pr/woodpecker": "tas-bot"},
    "jinno0/tas_autopilot": {"ci/woodpecker/pr/woodpecker": "tas-bot"},
    "jinno0/ai-hub_agent_proxy": {"ci/woodpecker/pr/woodpecker": "nobu007"},
    "nobu007/miyabiprivate": {"ci/woodpecker/pr/woodpecker": "nobu007"},
    "co-priv4/agent-pm": {
        "ci/woodpecker/pr/ci": "tas-bot",
        "ci/woodpecker/pr/quality-gates": "tas-bot",
    },
}
```

エラー送出パス（L1994–L2020 抜粋）:

```python
    slug = slug or ""
    required_contexts = _REQUIRED_CHECK_CONTEXTS.get(slug, frozenset())
    required_check_runs = _REQUIRED_CHECK_RUNS.get(slug, frozenset())
    unregistered_expects_ci: bool | None = None
    if (
        slug
        and slug not in _REQUIRED_CHECK_CONTEXTS
        and slug not in _REQUIRED_CHECK_RUNS
    ):
        expects_ci = _unregistered_repo_has_pr_ci(...)
        if expects_ci is None:
            return "pending", "cannot resolve CI declarations for this PR"
        unregistered_expects_ci = expects_ci
        if expects_ci:
            return (
                "failed",
                "required outcome check identity is not registered for this repository",  # L2018
            )
```

`_unregistered_repo_has_pr_ci`（L1703–L1759、要点）: base SHA と PR head の
`git diff --quiet` を CI 宣言パス（`.woodpecker` / `.woodpecker.yml` /
`.woodpecker.yaml` / `.github/workflows`）に対して実行し、差分があれば `True` を返す
（§2.3 が該当）。差分無ければ `_repo_expects_pr_checks` で CI 期待を判定。

### 2.5 本リポの origin slug

```
$ git remote get-url origin
https://github.com/jinno2/ComfyUI.git
```

`jinno2/ComfyUI` は§2.4 の両テーブルに存在しない（`jinno0/*` 系の登録のみ）。

## 3. repo 内で修正した欠陥: .concept/charter.yml の YAML 不通

前回 run の検証レシポートが exit_code 1（malformed `.concept/charter.yml`）で
一切の criterion 検証が不可能になっていた。原因は MS-003 の `intent:` 行のみ
インデント欠落（4スペースが 0）。

```
修正前: yaml.safe_load -> yaml.parser.ParserError
  while parsing a block mapping in ".concept/charter.yml", line 1, column 1
  expected <block end>, but found '<block mapping start>' in line 73, column 5
修正（.concept/charter.yml の1行、charter.yml|2 +-）:
  - intent: ".concept/ の辞書を実コード・テストと同期し、…"  （行頭インデントなし）
  +     intent: ".concept/ の辞書を実コード・テストと同期し、…"（4スペース）
修正後: python -c "import yaml; d=yaml.safe_load(open('.concept/charter.yml')); print('parse ok; milestones:', [m['id'] for m in d['milestones']])"
  parse ok; milestones: ['MS-001', 'MS-002', 'MS-003', 'MS-004', 'MS-005']  (exit=0)
```

実行環境: `/home/jinno/ai-hub/.venv/bin/python`（Python 3.12, PyYAML）。
本修正以外に charter の内容変更なし（`git diff --stat` = 1 file, 1 insertion, 1 deletion）。

## 4. 境界と follow-up

- **repo 内修正（実施済み）**: charter.yml インデント修復（§3）+ 本証跡の tracking 化。
- **repo 外（tas_autopilot、本 run の編集禁止 scope）**: `_REQUIRED_CHECK_CONTEXTS` へ
  `"jinno2/ComfyUI": frozenset({"ci/woodpecker/pr/woodpecker"})`、
  `_REQUIRED_CHECK_CONTEXT_PRODUCERS` へ
  `"jinno2/ComfyUI": {"ci/woodpecker/pr/woodpecker": "tas-bot"}` の登録が必要。
  登録後、PR #63（green・head 一致・producer 一致）は `auto_merge_blocked` にならない
  はず。`docs/llm-wiki/relations.md` の tas_autopilot 節に unchecked follow-up を記録した。

## 5. 最終 JSON サマリー

```json
{
  "root_cause": "tas_autopilot post_dispatch.py (sha256 e5c66eec..., L1994-L2020) treats any PR CI on an origin slug missing from _REQUIRED_CHECK_CONTEXTS/_REQUIRED_CHECK_RUNS as failed ('required outcome check identity is not registered'). jinno2/ComfyUI is unregistered there, and PR #63 modifies .woodpecker.yml base->head so _unregistered_repo_has_pr_ci returns True. The PR's actual CI is green: ci/woodpecker/pr/woodpecker=SUCCESS at head f713921686f8971711f667643a248d7bdd9cb8d1, producer tas-bot.",
  "fix_or_boundary": "In-repo fixed: .concept/charter.yml MS-003 intent line indentation restored (YAML now parses; this was breaking verification receipts). Out-of-repo boundary: the required registration (jinno2/ComfyUI -> ci/woodpecker/pr/woodpecker, producer tas-bot) lives in tas_autopilot, outside this run's write scope; recorded as unchecked follow-up in docs/llm-wiki/relations.md.",
  "branch": "ai/ComfyUI/instruction-20261122-175820-206928"
}
```
