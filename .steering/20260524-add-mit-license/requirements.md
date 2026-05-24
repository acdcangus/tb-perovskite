# requirements — MIT LICENSE 適用

**PI 指示 (2026-05-24 11:40):** LICENSE = MIT
**出典 directive:** cowork/progress/2026-05-24_1145_directive_PI_decisions.md Part 3

## 要求内容
- リポジトリルートに MIT `LICENSE` ファイル。
- README に License バッジ + 節。
- 主要 entry-point（src/perovskite_tb/__init__.py + 主要 scan スクリプト 5–10 本）に SPDX ヘッダ。
- docs/development-guidelines.md に「ライセンスと SPDX 表記」節。

## 受け入れ条件
- `LICENSE` 直下に存在, `grep -c "MIT License" LICENSE >= 1`。
- Copyright 行に年(2026)。**holder 表記**: PI 明示判断（supplement 0730）に従い `tk`（v4 T3-a の "Teruhisa Kotani" は
  0730 の明示決定と矛盾するため `tk` を維持。PI 再指示があれば差し替え）。← 受領確認 1150 でフラグ済み。
- README に License セクション + MIT バッジ。
- `src/perovskite_tb/__init__.py` に SPDX。
- docs/development-guidelines.md にライセンス節。
- Production 6 本不変, 231 テスト通過。

## 制約事項
- 全ファイルへの SPDX 一括付与は別 directive（本 directive は主要 entry-point のみ）。
