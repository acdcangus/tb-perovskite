# PI 判断 3 件受領 + directive 発行 — 2026-05-24 11:45 JST

**経緯:** Cowork 11:40 patrol で PI 判断待ち 3 件を通知 → PI が 11:42 のチャットで即答 → 本ノートで受領記録 + directive 発行を文書化。

## PI 判断（原文）

> 1 は C' が主、D は併記でいい。あなたの提案通り。
> 2．自立 polling はやめよう
> 3．MIT

→ 追加指示:
> あと、プログラム自体に手をいれているのであれば、それぞれの claude.md にしたがって、各種ドキュメントの整備もしてください。面倒くさがらずにちゃんとやっておいて。

## 翻訳された方針

| # | 項目 | 決定 |
|---|---|---|
| 1 | (x) Theme I 論文化方針 | C' 主・D' 校正点として併記（supervisor 推奨どおり） |
| 2 | (i) 自律 polling | 停止、`claude --continue` 検証はスキップ |
| 3 | (ii) LICENSE | MIT |
| 4 | (追加) ドキュメント規律 | `tb-perovskite/CLAUDE.md` 準拠で `.steering/` + `docs/` 整備必須 |

## 発行 directive

**`cowork/progress/2026-05-24_1145_directive_PI_decisions.md`** — 5 Part 構成 (Part 0 = CLAUDE.md 規律 / Part 1-3 = PI 判断 3 件 / 全体受け入れ)

### 主要な要求事項
- 3 commit に分割（Part 1 / Part 2 / Part 3）
- Part 2 / Part 3 は対応する `.steering/[YYYYMMDD]-[title]/` を新規作成（requirements / design / tasklist の 3 ファイル）
- Part 2 / Part 3 は対応する永続 `docs/` 更新を同梱
- 完了時 `cowork/progress/2026-05-24_HHMM_PI_decisions_implemented.md` で 3 件の commit ハッシュ + `.steering/` パス + `docs/` 更新箇所を記録
- Production bundle 6 本 + 既存 231 テストに無影響

### 緊急性
**低**。物理結果・Production には影響しない方針確定。ペース任意だが、受領時に軽量 ack のみお願い。

## `cowork/next_directive.md` 更新

v3（2026-05-23 14:40, 467 行, 旧自走モード）→ v4（2026-05-24 11:45, ~110 行, PI 判断 3 件反映版）に差し替え。
旧 §-1 「自律 5 分巡回ループ」を「停止中」に書き換え、v3 タスクキューは「§1 完了タスク履歴」に集約。

## supervisor 監視タスク

次 patrol（1155 JST）以降:
1. `2026-05-24_HHMM_directive_received.md` の出現を確認（受領遅延検出）
2. 3 commit の順次 push を監視（commit message に「PI directive `..._1145_directive_PI_decisions.md` 由来」が含まれるか）
3. `.steering/20260524-deprecate-polling/` と `.steering/20260524-add-mit-license/` に 3 ファイルずつ揃っているか機械検証
4. `docs/development-guidelines.md` と `docs/repository-structure.md` の diff を確認
5. Production bundle 6 本の git_dirty:false 維持を確認（再現性保持）
6. 既存 231 テスト通過維持を確認

## 残課題（v4 で解消）

- (x) Theme I 論文化方針 → ✅ 決定済み（C' 主・D' 併記）
- (i) `claude --continue` 検証 → ✅ スキップ確定（polling 停止）
- (ii) LICENSE → ✅ 決定済み（MIT）

→ **PI 判断待ち 0 件**。Claude Code は本 directive 消化後、また待機モード。
