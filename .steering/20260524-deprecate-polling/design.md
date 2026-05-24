# design — polling 停止

## 変更ファイル一覧
- `scripts/cowork_5min_poll.ps1` — 冒頭に DEPRECATED ヘッダ（本体ロジックは保持）。
- `scripts/cowork_5min_poll_README.md` — 冒頭 DEPRECATED 注記、末尾に解除/再開手順。
- `cowork/COWORK_CLAUDECODE_PATTERN.md` — 「5 分自律巡回ループ」節に停止前置き。
- `docs/repository-structure.md` — scripts/ deprecated 注記（永続ドキュメント更新, CLAUDE.md 準拠）。
- `src/perovskite_tb/shift_current.py` ほかの layer-2 hook（`_check_cowork_progress`）は**残置**（無害・呼ばれても軽量、
  scan 実行時の liveness ログのみ）。撤去は不要（PI 指示は OS スケジューラ層の停止が主眼）。

## 影響範囲分析
- 計算ロジック・Production 数値: **無影響**（polling は監視機構のみ）。
- テスト: 無影響（polling はテスト対象外）。
- 運用: 監視は Cowork 15 分巡回 + (Cowork 側で) 新規 commit ゼロ 4 サイクル → PI 通知ロジックが代替（本 steering 外）。

## 既存テストへの影響
なし（コメント/ドキュメント変更のみ）。
