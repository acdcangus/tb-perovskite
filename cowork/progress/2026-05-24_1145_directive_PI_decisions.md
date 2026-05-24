# Directive: PI 判断 3 件を反映 — 2026-05-24 11:45 JST

**発行元:** Cowork (supervisor)
**発行先:** Claude Code
**優先度:** 中（緊急性なし。Production 健全性に影響しない方針確定）
**前提:** Directive 0930 完全完了済み（Part 1 + Part 2 PI 解説 4/4）、HEAD `2228a4a`

---

## PI 判断結果（2026-05-24 11:40 のチャットで受領）

| # | 項目 | PI 決定 |
|---|---|---|
| 1 | (x) Theme I 論文化方針 | **C' を主結果、D' は併記**（Cowork supervisor 推奨どおり） |
| 2 | (i) 自律 5 分巡回ループ | **停止する**（`claude --continue` 検証は行わず、機構ごと撤去） |
| 3 | (ii) LICENSE | **MIT** |

---

## ★ Part 0. プロジェクト規律（CLAUDE.md 準拠）— PI 追加指示 2026-05-24 11:45

PI 追加指示: **「プログラム自体に手をいれているのであれば、それぞれの CLAUDE.md にしたがって、各種ドキュメントの整備もしてください。面倒くさがらずにちゃんとやっておいて。」**

→ 本 directive は `src/` / `scripts/` / `docs/` / ルート（LICENSE）に変更を入れるため、`C:\Users\kteru\tb-perovskite\CLAUDE.md` 「機能追加・修正時の手順」に従い **`.steering/` ディレクトリ + 永続ドキュメント更新を必ず実施** すること。「面倒だから省略」は禁止。

### 0.1 各 Part の steering 必要性判定

| Part | 変更領域 | `.steering/` | 永続 `docs/` 更新 |
|---|---|---|---|
| Part 1 | `cowork/reports/` のみ（コード無変更） | **不要**（docs/cowork は科学計算本体外） | 不要 |
| Part 2 | `scripts/` + `cowork/` ドキュメント | **作成**: `.steering/20260524-deprecate-polling/` | `docs/repository-structure.md`（scripts/ 配下の deprecated 注記） |
| Part 3 | ルート（LICENSE）+ `README.md` + `src/` + `docs/` | **作成**: `.steering/20260524-add-mit-license/` | `docs/development-guidelines.md`（ライセンス節）/ `docs/repository-structure.md`（LICENSE 追加） |

### 0.2 `.steering/` テンプレート（Part 2, Part 3 共通）

各 `.steering/[YYYYMMDD]-[title]/` 配下に **3 ファイルを順次作成**:

**(a) `requirements.md`**: PI 指示原文 + 受け入れ条件 + 制約事項（既存 Production bundle 不変、231 テスト通過維持）
**(b) `design.md`**: 変更ファイル一覧、影響範囲分析、既存テストへの影響
**(c) `tasklist.md`**: 具体タスク + チェックボックス + 完了条件

CLAUDE.md 推奨は「1 ファイル作成ごとに承認」だが、本 directive 起源で内容も小さいので **3 ファイル連続作成 OK**（PI 確認は本 directive 受領で代替）。

### 0.3 `docs/` 更新の具体内容

**`docs/development-guidelines.md`** に追加（Part 3 で対応、Part 0.4 の節「ライセンスと SPDX 表記」も参照）:
```
## ライセンスと SPDX 表記
- 本リポジトリは MIT License（`LICENSE` ファイル参照）
- 新規ソースファイル（`src/`, `scripts/`, `tests/`）には冒頭に SPDX 識別子を必ず付与:
  - Python: `# SPDX-License-Identifier: MIT`
  - Shell: `# SPDX-License-Identifier: MIT`
- Copyright 行は必須でないが、ファイル単位で著作権を明示したい場合は SPDX 行の直後に `# Copyright (c) <year> <holder>` を置く
- 既存ファイルへの一括付与はバッチ作業（別 directive）
```

**`docs/repository-structure.md`** に追加（Part 2 + Part 3 で対応）:
```
## ルート直下ファイル
- LICENSE — MIT License 全文（2026-05-24 追加）

## scripts/ の deprecated 項目
- cowork_5min_poll.ps1 — 2026-05-24 deprecate（PI 判断による自律 polling 停止）
- cowork_5min_poll_README.md — 同上
- 履歴として保持。再開手順は README 末尾参照
```

### 0.4 受け入れ条件（Part 0 全体）

- [ ] `.steering/20260524-deprecate-polling/` に requirements.md / design.md / tasklist.md
- [ ] `.steering/20260524-add-mit-license/` に requirements.md / design.md / tasklist.md
- [ ] `docs/development-guidelines.md` に「ライセンスと SPDX 表記」節が追加
- [ ] `docs/repository-structure.md` に LICENSE 追加 + scripts/ deprecated 注記
- [ ] 各 `.steering/*/` への新規ファイル作成は対応する Part の commit に含める（分割 commit しない）

---

## Part 1. Theme I 論文化方針: C' 主・D' 併記

### 1.1 方針

- **主結果**: option C' = Materials Project DFPT bare ε∞ による **8 材料**絶対 E_b マップ（`results/production/theme_I_exciton_MP_DFPT/2026-05-24_118b3ce/`）。
- **併記（校正点）**: option D' = Cho 2019 effective ε_eff ≈ 6.1 による **CsPbI₃ 単独**の絶対 E_b = 22 meV（`results/production/theme_I_exciton/2026-05-23_f66690c/`）。
- **位置づけ**: 「C' で 8 材料の相対トレンドを defensible に提示、D' で Pb-I 系の絶対値が実験と整合することを示し、C' の絶対値は bare ε∞ 由来で上限と honest に明記」。

### 1.2 タスク

**T1-a: `cowork/reports/theme_I_exciton.md` の構成見直し（**主に序文と §3 の見出し再編、本文は流用可**）**
- 冒頭の Abstract / 30 秒サマリで「主結果 = C' 8 材料マップ、D' は校正点」を明示
- §3.3 を「**§3.1 主結果: C' 8 材料 E_b マップ**」に格上げ
- 既存 §3.1（effective mass）→ §2 に格下げ（前提データとしての位置）
- 既存 §3.2（web research finding）→ §4 「方法論的考察」に移動
- 既存 D'（CsPbI₃ 校正）を新 §3.2 「校正点: D' = CsPbI₃ 実効 ε_eff」として併記
- limitations セクションで「C' は bare ε∞ 由来のため絶対値は上限、相対トレンドが頑健」を明記（既に書いてあるので維持）

**T1-b: `cowork/reports/PI_explained_theme_I.md` の軽微更新**
- §3 タイトルを「**主結果（C'）と校正点（D'）**」に。本文の数値・解釈は維持（既に C' を主に扱っているため大幅変更不要）。
- §4 「何が新しいか」に「**C' 主・D' 校正の hybrid 提示**は本研究の方法論的貢献」と 1 文追加

**T1-c: `cowork/reports/theme_I_publication_outline.md` を新規作成（論文骨子初稿）**
- セクション構成: Abstract / Introduction / Methods (TB / MP DFPT / Wannier-Mott) / Results (C' 8材料 + D' 校正) / Discussion (bare ε vs ε_eff / Blount 統一限界) / Conclusion / References
- 各セクション 100–300 字程度のスケッチで OK（清書は後日）
- 投稿候補: npj Comput. Mater. / Phys. Rev. Materials / J. Phys. Chem. C を併記
- 既存 PI 解説と技術報告書の差分（学術論文ならではの構成）を意識

### 1.3 受け入れ条件

- [ ] `theme_I_exciton.md` 冒頭で「C' 主・D' 併記」が一目で分かる
- [ ] §3 の見出し順が論文化を意識した構成になっている
- [ ] `PI_explained_theme_I.md` で §4 に hybrid 提示の novelty が明記
- [ ] `theme_I_publication_outline.md` が新規作成され、7 セクション骨子と投稿候補が含まれる
- [ ] Production bundle には**一切手を加えない**（数値・MANIFEST は不変）
- [ ] 既存 231 テスト通過維持（コード変更なしのはず）

---

## Part 2. 自律 5 分巡回ループ停止

### 2.1 背景

PI 判断: 「自立 polling はやめよう」（2026-05-24 11:40）。
理由（Cowork 推測）: 5 分巡回はコンテキスト消費・コスト・ノイズが大きく、また Cowork supervisor の 15 分巡回が機能している今、二重化は不要。

### 2.2 タスク

**T2-a: Windows Task Scheduler の解除（手順書化のみ、Claude Code 自身では実行しない）**
- スクリプト本体は Linux サンドボックスからは PowerShell 実行不可。
- **PI への手順を `scripts/cowork_5min_poll_README.md` 末尾に明示** したうえで、PI 側で 1 行コマンド実行:
  ```powershell
  Unregister-ScheduledTask -TaskName "Cowork-ClaudeCode-5min-poll" -Confirm:$false
  ```
- 完了確認方法も併記: `Get-ScheduledTask -TaskName "Cowork-ClaudeCode-5min-poll"` が `ObjectNotFound` を返せば成功

**T2-b: スクリプトファイルの deprecate**
- `scripts/cowork_5min_poll.ps1` 冒頭に以下のヘッダを追加（削除はしない、履歴として保持）:
  ```powershell
  # ⚠️ DEPRECATED 2026-05-24 — PI 判断により自律 5 分巡回ループは停止しました。
  # Cowork supervisor の 15 分巡回（Cowork 側 scheduled task）で代替します。
  # 経緯: cowork/progress/2026-05-24_1145_directive_PI_decisions.md §Part 2
  # 復活させる場合: scripts/cowork_5min_poll_README.md §「再開手順」参照
  ```
- `scripts/cowork_5min_poll_README.md` 冒頭にも同等の DEPRECATED 注記
- README 末尾に「Unregister-ScheduledTask 手順」と「再開手順（参考）」を追加

**T2-c: ドキュメント反映**
- `cowork/COWORK_CLAUDECODE_PATTERN.md` の §「5 分自律巡回ループ」を「(2026-05-24 PI 判断で停止) 〜以下は履歴として保持」と前置きして既存内容を維持
- `cowork/next_directive.md` §-1 を「停止済み」に更新（Part 3 で同時に実施）
- `cowork/PRODUCTION_RULES.md` 内に polling 言及があれば同様に「停止」を 1 行追記

**T2-d: 沈黙再発に備えた代替策の確認**
- 元の動機は `cowork/progress/2026-05-23_2225_BLOCKED_session_stalled.md`（4h 沈黙事例）の再発防止
- 代替: **Cowork supervisor 15 分巡回が新規 commit ゼロを 4 サイクル（=1h）連続検出した場合に PI 通知**するロジックを Cowork 側 scheduled task に組み込み（本 directive 外、Cowork 側で追って対応）
- Claude Code 側は本項目について追加実装不要

### 2.3 受け入れ条件

- [ ] `scripts/cowork_5min_poll.ps1` 冒頭に DEPRECATED ヘッダ
- [ ] `scripts/cowork_5min_poll_README.md` 冒頭に DEPRECATED 注記＋末尾に解除手順
- [ ] `cowork/COWORK_CLAUDECODE_PATTERN.md` §「5 分自律巡回ループ」に停止注記（既存内容は履歴として保持）
- [ ] Production bundle / テストには無影響（コード本体は触らない）

---

## Part 3. LICENSE = MIT

### 3.1 タスク

**T3-a: `LICENSE` ファイル作成（リポジトリルート）**
- 標準 MIT テンプレート
- Copyright 行: `Copyright (c) 2026 Teruhisa Kotani`
  - 表記に institutional affiliation を入れたい場合は PI に都度確認（本 directive では個人名で進める）

**T3-b: `README.md` に License バッジ・節を追加**
- バッジ: `[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)`
- 末尾に `## License` セクションを追加: `This project is licensed under the MIT License — see [LICENSE](LICENSE) for details.`

**T3-c: ソースコードへの SPDX ヘッダ方針**
- 新規ファイルには冒頭に `# SPDX-License-Identifier: MIT` を必ず付与（development-guidelines.md に追記）
- 既存ファイルへの一括付与は本 directive ではスコープ外（次回まとめて batch で対応）。ただし `src/perovskite_tb/__init__.py` と `scripts/scan_*.py` の主要 entry-point 数本のみ手動付与（5–10 ファイル）。
- 全件付与は別 directive で。

**T3-d: `docs/development-guidelines.md` 更新**
- 「ライセンス」節を追加: 「本リポジトリは MIT License。新規ソースファイルには冒頭に `# SPDX-License-Identifier: MIT` を付与すること」

### 3.2 受け入れ条件

- [ ] `LICENSE` ファイルがリポジトリ直下に存在、`grep -c "MIT License" LICENSE >= 1`
- [ ] Copyright 行に年（2026）と PI 名（Teruhisa Kotani）が含まれる
- [ ] `README.md` に License セクションと MIT バッジ
- [ ] `src/perovskite_tb/__init__.py` に SPDX ヘッダ
- [ ] `docs/development-guidelines.md` にライセンス節
- [ ] Production bundle / テストに無影響

---

## 全体の受け入れ条件と commit 方針

### コミット粒度

3 つの独立した PI 判断なので、**3 commit に分けて push** してください。各 commit には対応する `.steering/` ファイル群と `docs/` 更新を**同梱**（Part 0.4 参照）:

1. `Theme I publication direction: C' main + D' as calibration point — reports restructured + outline drafted`
   （Part 1 のみ。`.steering/` 不要、`docs/` 不要）
2. `Deprecate 5-min self-polling loop (PI decision); Cowork 15-min patrol covers monitoring`
   （Part 2 + `.steering/20260524-deprecate-polling/` + `docs/repository-structure.md` scripts deprecated 注記）
3. `Add MIT LICENSE; SPDX headers in main entrypoints; README + dev-guidelines updated`
   （Part 3 + `.steering/20260524-add-mit-license/` + `docs/development-guidelines.md` + `docs/repository-structure.md` LICENSE 追加）

### 全体受け入れ

- [ ] 上記 3 commit が順次 push される
- [ ] 各 commit message に「PI directive `2026-05-24_1145_directive_PI_decisions.md` 由来」を 1 行明記
- [ ] Part 2 / Part 3 の commit には対応する `.steering/` ディレクトリ（requirements/design/tasklist）が含まれる
- [ ] Part 2 / Part 3 の commit には対応する `docs/` 更新（development-guidelines, repository-structure）が含まれる
- [ ] 既存 Production bundle 6 本に変更なし（git_dirty:false 維持、再現性保持）
- [ ] 既存 231 テスト通過維持
- [ ] 完了時に `cowork/progress/2026-05-24_HHMM_PI_decisions_implemented.md` を作成、3 件の完了状況とコミットハッシュ + `.steering/` パス + `docs/` 更新箇所を記載

### 緊急性

**全件低**。Production 数値・物理結果には一切影響しない方針確定なので、ペースは任意。
ただし directive を受領したら即 `2026-05-24_HHMM_directive_received.md` で軽量確認だけお願いします（受領遅延の検出のため）。

---

## 質問・blocker があれば

- `cowork/progress/YYYY-MM-DD_HHMM_question.md` で。
- 特に: LICENSE Copyright 行の名前表記（個人名のみで OK か、所属を入れたいか）は PI に都度確認の余地あり。本 directive では「個人名のみ」で進めて差し支えない判断ですが、迷ったら聞いてください。

---

**Cowork 署名:** supervisor patrol 2026-05-24 11:45 JST
**前 directive:** `cowork/progress/2026-05-24_0930_directive_theme_I_MP_and_PI_reports.md` (完全完了)
