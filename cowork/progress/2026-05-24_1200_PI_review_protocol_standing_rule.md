# Directive: 全レポート二者並行レビュー（3 ラウンド連続 0 指摘）+ 文献照合必須 — 2026-05-24 12:00 JST

**発行元:** Cowork (supervisor) — PI 直接指示反映
**発行先:** Claude Code
**優先度:** ★ **最高（standing rule、即時適用、すべての既存・将来レポートに恒久適用）**
**親:** PI 指示原文（2026-05-24 11:55 JST 受領）:

> 「すべてのレポート類は、claude code およびあなたそれぞれで批判的にレビューして、3 回指摘がなくなるまで何度もレビューしなおしてね。特に、ハルシネーションは絶対ダメ。記憶じゃなくて、文献など事実に基づいて確認は必須。」

---

## 1. ルールの中核（standing rule）

### 1.1 二者並行レビュー

すべてのレポート（`cowork/reports/*.md`、`results/*/MANIFEST.json` の `key_numbers`、`docs/` の科学的内容を含む箇所）は **Claude Code と Cowork supervisor の両者がそれぞれ独立に批判的レビュー** を実施する。

### 1.2 3 ラウンド連続 0 指摘で「合格」

- ラウンド N: Claude Code 自己レビュー → 指摘リスト保存 → 修正 commit → Cowork が独立レビュー → 指摘リスト保存
- ラウンド N+1 でも同じプロセスを繰り返す
- **連続 3 ラウンドで両者とも指摘 0** になった時点ではじめて「合格 (clean)」とマーク
- 1 つでも指摘が出たらカウンタリセット、再度 3 ラウンド連続が必要

### 1.3 ハルシネーション禁止

**最重要。** すべての記述は:

- **数値**: Production MANIFEST または引用論文の式/表/図から **抜粋元の path・行・式番号を明示**
- **式・公式**: 引用論文の式番号（例: Roth-Lax 1959 Eq. (3)）を明示
- **概念的記述**: 引用論文の section / page まで遡れる形で明示
- **記憶ベースの記述は絶対不可**。「〜と思われる」「〜と一般に言われる」のような根拠不明記述は全て指摘対象

「**Claude の事前知識（学習データ）から書いた**」記述は本プロジェクトでは無条件アウト。**手元の PDF（`references/pdfs/`）または `results/production/*/MANIFEST.json`** に遡れない記述は削除または出典追加。

### 1.4 文献照合の実施方法

```bash
# 例: arxiv_2104.01738 (Vicent-Luna 2021) の Eq. (3) を引用したい場合
pdftotext -layout references/pdfs/arxiv_2104.01738.pdf - | grep -A3 "Eq\. (3)\|Eq.3"
# または該当式番号近傍を直接見る
pdftotext -layout references/pdfs/arxiv_2104.01738.pdf - | head -300 | tail -100
```

`references/pdfs/` に 61 本の PDF がある。`pdftotext -layout` でテキスト化可能。複雑な式は OCR が崩れることがあるので **その場合は引用を控えるか、論文 PDF の特定セクションを参照したと記載**して、ハルシネーションの余地を残さない。

---

## 2. レビュー対象一覧（2026-05-24 12:00 時点）

| # | ファイル | 行数 | 最終更新 | レビュー優先度 |
|---|---|---|---|---|
| R1 | `cowork/reports/PI_explained_overview.md` | 272 | 00:35 UTC | ★★★（全テーマ俯瞰、横断引用多） |
| R2 | `cowork/reports/PI_explained_theme_A.md` | 137 | 02:14 UTC | ★★★ |
| R3 | `cowork/reports/PI_explained_theme_F.md` | 116 | 02:22 UTC | ★★★ |
| R4 | `cowork/reports/PI_explained_phase_1.5_optical.md` | 99 | 02:33 UTC | ★★★ |
| R5 | `cowork/reports/PI_explained_theme_I.md` | 115 | 02:34 UTC | ★★★ |
| R6 | `cowork/reports/theme_A_g_factor.md` | 155 | 23-05 11:08 UTC | ★★ |
| R7 | `cowork/reports/theme_A5_optical.md` | 71 | 23-05 11:09 UTC | ★★ |
| R8 | `cowork/reports/theme_F_shift_current.md` | 131 | 23-05 17:32 UTC | ★★ |
| R9 | `cowork/reports/theme_I_exciton.md` | 63 | 23-05 23:14 UTC | ★★ |
| R10 | `cowork/reports/theme_I_publication_outline.md` | 51 | 02:56 UTC | ★★（v4 Part 1 で新規） |
| M1-M6 | `results/production/*/MANIFEST.json` の `key_numbers` セクション | — | 各 production 時 | ★（数値の起点なので最高位、本ルールでは「合格」してから引用すること） |

→ 計 11 レポート + 6 MANIFEST。

---

## 3. レビュー観点（チェックリスト）

各レポートで以下を 1 行ごとに verify:

### 3.1 数値類

- [ ] 数値の単位が明示されているか
- [ ] 引用元の MANIFEST path（または論文式番号）が明示されているか
- [ ] MANIFEST の対応 key と完全一致しているか（丸め誤差含めて）
- [ ] 「実験値」と書いてある数値は、実験論文の table/text に遡れるか

### 3.2 式・公式

- [ ] 式番号が引用論文と一致しているか
- [ ] 符号規約が論文と一致しているか（特に SOC, Slater-Koster, Kubo-Greenwood）
- [ ] 単位系が論文と一致しているか（SI / atomic units / cgs）

### 3.3 引用・出典

- [ ] arXiv ID / DOI が正しいか（**PDF タイトルと照合**、CLAUDE.md「PDF 取得時の必須チェック」と同じ）
- [ ] 引用箇所が論文の主張に沿っているか（誤解釈・拡大解釈ゼロ）
- [ ] 出典のないクレームがゼロか

### 3.4 物理的整合性

- [ ] 極限挙動（SOC→0、k→0、低エネルギー極限など）が物理的に妥当か
- [ ] 対称性議論（時間反転、空間反転、結晶対称性）が論文と一致するか
- [ ] honest な limitation 記述があるか（bare ε vs ε_eff、f-sum 比など）

### 3.5 用語・表記

- [ ] 用語の初出定義があるか
- [ ] 略語が初出時に展開されているか
- [ ] 日本語訳が原語と乖離していないか

---

## 4. ワークフロー（1 ラウンドあたり）

### 4.1 Claude Code 担当

1. レポートを **1 ファイルずつ** 開き、L1 から逐行レビュー
2. 上記 3.1〜3.5 のチェック項目を機械的に適用
3. 指摘事項を `cowork/progress/2026-05-24_HHMM_review_round_N_claude_code.md` に保存
   - 形式: `[ファイル名]:行番号 — 問題種別 — 詳細 — 解決方針（出典追加 / 削除 / 訂正）`
4. 修正 commit を実施
5. commit message に `review round N (claude code), N findings addressed` と明記

### 4.2 Cowork supervisor 担当

1. Claude Code commit 後、同じレポートを独立にレビュー
2. 同じチェック項目を適用
3. 指摘事項を `cowork/progress/2026-05-24_HHMM_review_round_N_cowork.md` に保存
4. Claude Code がさらに修正 → 次ラウンドへ

### 4.3 連続 3 ラウンド 0 指摘で合格

- 合格時: `cowork/progress/2026-05-24_HHMM_report_NAME_clean_3rounds.md` で記録
- リセット条件: いずれかのラウンドで両者の合計指摘が 1 件でもあればカウンタ 0 に戻す

---

## 5. 受け入れ条件（standing rule の deployment 段階）

- [ ] 本 directive を Claude Code が `cowork/progress/2026-05-24_HHMM_review_protocol_received.md` で受領確認
- [ ] **`cowork/next_directive.md` の §2 に standing rule として記載**（supervisor が並行で実施）
- [ ] ラウンド 1 の **Claude Code 自己レビュー** が R1-R10 すべてに対して完了
- [ ] ラウンド 1 の **Cowork レビュー** が R1-R10 すべてに対して完了
- [ ] 以後、3 ラウンド連続 0 指摘になるまで継続

### 着手順（推奨）

PI 解説 4 本（R2-R5）が最優先（PI が直接読む文書）。次に overview (R1)、最後に技術レポート（R6-R10）。

---

## 6. 緊急性と並行性

- 本ルールは**最高優先度**だが、緊急性は低い（既存 Production は健全、231 テスト通過維持）。
- v4 directive Part 2 (polling 停止)、Part 3 (LICENSE 整備) は **本レビューと並行実施可**（コード変更系で独立）。
- **新しい計算・Production bundle 作成は本レビューが安定するまで控えめに**（Production の数値も照合対象だが、Production 自体は MANIFEST が真実の源として既に固定されている）。

---

## 7. 違反検出

- supervisor patrol で「出典なき新規数値」「記憶ベース推論」「論文式番号の誤り」を検出したら `cowork/progress/YYYY-MM-DD_HHMM_review_violation.md` で警告
- 違反内容によっては該当 commit の revert を Claude Code に依頼

---

## 8. 完了の定義

「全 11 レポート × MANIFEST 6 本 = 17 ターゲット」がすべて **3 ラウンド連続 0 指摘**になった時点で「PI レビュー protocol Phase 1 完了」とマーク。以後は新規レポート追加時のみ本 protocol を起動。

PI に最終報告（`cowork/progress/YYYY-MM-DD_HHMM_PI_review_protocol_phase1_complete.md`）を提出して PI 判断を仰ぐ。

---

## 9. 補足: 既に PDF 化された 61 本の活用

`references/pdfs/` 61 本 + `references/references.md` 分類タグが既に整備済。引用したい論文の arXiv ID から PDF を即座に開けるので、**「記憶ベース」と「出典付き」の二択で迷ったら必ず PDF を開いて確認**してください。
