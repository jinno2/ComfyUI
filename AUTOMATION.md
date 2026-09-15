# AUTOMATION.md — ComfyUI

大ゴール: AIによる全自動開発の実現。人間より圧倒的に効率的に。(fleet共通)

## 発火 (Driver)
- crontab: 0本(2026-09-15 実測・全41行との突合)
- GitHub Actions: 25本(上流由来・当repoでは運用しない)

## 対象外宣言 (fork・upstreamのみ)
本repoは https://github.com/jinno2/ComfyUI のlocal clone(jinnoのfork・上流追従対象)。発火・運用の正本は上流。fleet運用対象外。

## Kill Switch
該当する発火なし

## Status
2026-09-15 初版整備(実測: crontab突合・workflow列挙)。fleet台帳: /home/jinno/business_notes/AUTOMATION.md
