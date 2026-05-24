# design — MIT LICENSE

## 変更ファイル一覧
- `LICENSE`（ルート, 既存 — MIT + Copyright (c) 2026 tk。本 directive で内容確認・維持）。
- `README.md` — バッジ + `## License` 節。
- `src/perovskite_tb/__init__.py` — SPDX ヘッダ。
- 主要 scan スクリプト（SPDX 未付与のもの）に SPDX: scan_g_factors.py, scan_optical_9materials.py,
  scan_shift_current_9materials.py 等（5–10 本以内）。
- `docs/development-guidelines.md` — 「ライセンスと SPDX 表記」節。
- `docs/repository-structure.md` — ルート LICENSE 記載（Part 2 commit で追記済み）。

## 影響範囲分析
- 計算ロジック: SPDX は冒頭コメント行のみ → **無影響**。Python はコメント前置きで docstring/挙動不変。
- テスト: 無影響（import collection に影響しないことを確認）。
- Production bundle: 不変。

## holder 名の判断
v4 T3-a は "Teruhisa Kotani" だが supplement 0730（PI 明示 iv）は `tk`。より specific な明示決定を優先し `tk` 維持。
