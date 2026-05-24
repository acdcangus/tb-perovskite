# requirements — 自律 5 分巡回ループの停止 (deprecate)

**PI 指示原文 (2026-05-24 11:40):** 「自立 polling はやめよう」
**出典 directive:** cowork/progress/2026-05-24_1145_directive_PI_decisions.md Part 2

## 要求内容
- `scripts/cowork_5min_poll.ps1`（OS スケジューラ層）の自律 5 分巡回を停止。
- スクリプトは削除せず **DEPRECATED 注記**で履歴保持。再開手順を明記。
- 監視は Cowork supervisor の 15 分巡回が代替。

## 受け入れ条件
- `cowork_5min_poll.ps1` 冒頭に DEPRECATED ヘッダ。
- `cowork_5min_poll_README.md` 冒頭に DEPRECATED 注記 + 末尾に Unregister-ScheduledTask 手順 + 再開手順。
- `cowork/COWORK_CLAUDECODE_PATTERN.md` の 5 分巡回節に停止注記（既存は履歴保持）。
- `docs/repository-structure.md` に scripts/ deprecated 項目を追記。

## 制約事項
- 既存 Production bundle 6 本は不変（git_dirty:false 維持）。
- 既存 231 テスト通過維持（コード本体に計算ロジック変更なし）。
- スクリプト本体の PowerShell は Linux サンドボックスから実行不可 → Task Scheduler 解除は PI が手動実行（手順書化のみ）。
