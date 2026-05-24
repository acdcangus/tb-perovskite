# Directive v4 (1145 PI decisions) 受領確認 — 2026-05-24 11:50

`cowork/progress/2026-05-24_1145_directive_PI_decisions.md` 受領。3 commit（Part 1/2/3）で順次実施します。
CLAUDE.md 準拠（Part 2/3 に `.steering/` + `docs/` 更新同梱）。

## ★ 1 件フラグ: LICENSE Copyright 名の不整合
- v4 T3-a（1145）: `Copyright (c) 2026 Teruhisa Kotani`（フルネーム）
- だが **supplement 0730（PI 明示判断 iv）: `tk`（イニシャル）、「full name 表記にはしない」**。既に `LICENSE` は `tk` で適用済み。
- v4 §229 も「名前表記は PI 確認の余地あり」と明記。
- **判断: より specific で明示的な PI 決定（0730 の `tk`）を維持**します（フルネームへの上書きはしない）。
  PI が現時点でフルネーム希望なら 1 言ください、即差し替えます。誤って個人名を入れ替えない安全側を採用。

## 着手順
1. Part 1: Theme I 報告書 C' 主・D' 併記 + publication outline（.steering/docs 不要）
2. Part 2: polling 停止 deprecate（`.steering/20260524-deprecate-polling/` + `docs/repository-structure.md`）
3. Part 3: MIT LICENSE 整備（README/SPDX/dev-guidelines、`.steering/20260524-add-mit-license/` + `docs/`）
既存 Production 6 本不変・231 テスト維持を厳守。
