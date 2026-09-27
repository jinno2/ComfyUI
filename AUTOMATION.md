# AUTOMATION.md — ComfyUI fork

## Driver

TAS autopilot が `~` 配下の本リポを発見し、自律開発を駆動する。Comfy-Org/ComfyUI には自動追従せず、上流の取り込みは所有者の明示指示時のみ行う。

## Schedule

`tas-autopilot.timer` は5分ごと。Woodpecker は PR と `main` への push で `.woodpecker.yml` を実行する。

## Entrypoint

開発タスクは TAS 制御平面から dispatch する。Woodpecker の自前エージェントで Ruff と `tests-unit` を実行する。

## Stall Policy

再試行と停滞検知は TAS が担当する。CI が失敗したらコードを直し、GitHub 提供ランナーへ切り替えない。

## Coordination

開発 dispatch は TAS、テストゲートは Woodpecker が担当する。このフォークでは GitHub Actions を無効化済み。残る上流由来の workflow は実行されない。

## Kill Switch

本リポの新規タスク停止は TAS 制御平面で設定する。`systemctl --user stop tas-autopilot.timer` はこのホストの全リポの dispatch を止める。

## Status

稼働中：TAS timer 有効、Woodpecker リポ有効、GitHub Actions 無効（2026-09-27）。

## Notes

worktree と branch の後処理は TAS が担当する。driver 変更時は本書を更新する。

_最終更新: 2026-09-27_
