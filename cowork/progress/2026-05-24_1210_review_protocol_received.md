# レビュー protocol 受領確認 — standing rule 1200 — 2026-05-24 12:10

`cowork/progress/2026-05-24_1200_PI_review_protocol_standing_rule.md` 受領。最高優先 standing rule として適用開始。

## 理解した内容
- 全レポート（R1–R10）+ MANIFEST 6 本を、Claude Code と Cowork が**独立に**批判レビュー。
- **連続 3 ラウンド両者 0 指摘**で合格。1 件でも指摘が出たらカウンタ reset。
- **ハルシネーション禁止**: 数値→MANIFEST path / 式→論文式番号 / 概念→論文 section、すべて遡れること。
  **記憶ベース記述は無条件アウト**。`references/pdfs/`（61 本）or `results/production/*/MANIFEST.json` に遡れないものは削除/出典追加。
- 着手順: PI 解説 4 本（R2–R5）→ overview（R1）→ 技術レポート（R6–R10）。

## v4 (1145) との関係
- v4 directive（PI 判断 3 件, Part 1/2/3）は **全完了**（commit `f3324e1`/`ea075bc`/`ee35ed7`、報告 `1205_PI_decisions_implemented.md`）。
- 本 protocol は v4 と独立の新規 standing rule。これより着手。

## Round 1 着手計画（Claude Code 自己レビュー）
1. **数値照合**（最優先・最も hallucination リスク）: 全レポートの数値を対応 MANIFEST key_numbers と突き合わせ。
2. **出典照合**: 記憶ベースで書いた可能性のある記述（実験値・論文誌名/年/式番号）を `references/pdfs/` で verify、
   遡れないものは「文献典型値（要確認）」に格下げ or 削除。
3. 指摘を `2026-05-24_HHMM_review_round_1_claude_code.md` に記録 → 修正 commit。
4. Cowork の独立レビューと合わせて 3 ラウンド連続 0 を目指す。

注: 緊急性は低（Production 健全・231 テスト通過）。新規 Production 作成は本レビュー安定まで控えめに（§6）。
