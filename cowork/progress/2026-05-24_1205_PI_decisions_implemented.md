# PI 判断 3 件 実装完了 — directive v4 (1145) — 2026-05-24 12:05

`cowork/progress/2026-05-24_1145_directive_PI_decisions.md` の Part 1/2/3 を 3 commit で完了。

| Part | 内容 | commit | `.steering/` | `docs/` 更新 |
|---|---|---|---|---|
| 1 | Theme I 論文化: C' 主・D' 校正に再構成 + 論文骨子 | `f3324e1` | 不要 | 不要 |
| 2 | 自律 5 分巡回 deprecate | `ea075bc` | `.steering/20260524-deprecate-polling/`（req/design/tasklist） | `docs/repository-structure.md`（scripts deprecated + LICENSE root） |
| 3 | MIT LICENSE 整備 | `ee35ed7` | `.steering/20260524-add-mit-license/`（req/design/tasklist） | `docs/development-guidelines.md`（ライセンス/SPDX 節） |

## Part 1（C' 主・D' 校正）
- `cowork/reports/theme_I_exciton.md` 再構成: Abstract + §3.1=★主結果 C' 8材料マップ / §3.2=校正 D' CsPbI₃ 22meV /
  §3.3=入力 有効質量 / §4=bare ε vs ε_eff + Blount 考察。
- `PI_explained_theme_I.md` §3/§4 更新（hybrid novelty）。
- `cowork/reports/theme_I_publication_outline.md` 新規（7 節骨子 + 投稿候補 npj CM/PRM/JPC C）。
- Production bundle 不変。

## Part 2（polling 停止）
- `cowork_5min_poll.ps1` / README 冒頭に DEPRECATED、README 末尾に Unregister/再開手順。
- `COWORK_CLAUDECODE_PATTERN.md` / `PRODUCTION_RULES.md` に停止注記（履歴保持）。
- Task Scheduler 解除は PI 手動（`Unregister-ScheduledTask -TaskName "Cowork-ClaudeCode-5min-poll" -Confirm:$false`）。

## Part 3（MIT LICENSE）
- `LICENSE`（MIT, © 2026 **tk**）。README バッジ + License 節。SPDX を `__init__.py` + 主要 scan 4 本に付与。
- **★ holder 名フラグ**: v4 T3-a は "Teruhisa Kotani" だが supplement 0730（PI 明示）は `tk`。明示決定 `tk` を維持
  （誤って個人名に変えない安全側）。PI がフルネーム希望なら 1 言で差し替えます。

## 受け入れ
- [x] 3 commit 順次 push、各 message に directive 由来を明記。
- [x] Part 2/3 に `.steering/`（req/design/tasklist）+ `docs/` 更新を同梱。
- [x] Production bundle 6→現 7 本すべて git_dirty:false 維持・不変。
- [x] **231 テスト通過維持**。
- [x] LICENSE 直下、`grep -c "MIT License" LICENSE`=1、Copyright 2026。

→ **directive v4 (1145) 全完了**。次指示待ち。
