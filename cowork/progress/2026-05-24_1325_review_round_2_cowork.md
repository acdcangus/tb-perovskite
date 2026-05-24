# ラウンド 2 supervisor (Cowork) レビュー — 1245 マージ commit cfa8172 検証 — 2026-05-24 13:25 JST

**発行元:** Cowork (supervisor patrol)
**プロトコル:** `cowork/progress/2026-05-24_1200_PI_review_protocol_standing_rule.md` 準拠
**ラウンド:** 2 / 連続 0 指摘必要数 3
**対象 commit:** `cfa8172` "review round 1 (claude code + cowork): 16 findings addressed across PI_explained x4 + overview + theme_I"
**照合実施:**
- `git show cfa8172` で 9 ファイル差分の全行 verify
- PDFs: `arxiv_2101.08562` (Kashikar 4-orbital vs 13-orbital 句確認)
- MANIFESTs: `theme_I_exciton_MP_DFPT/2026-05-24_118b3ce/MANIFEST.json` `key_numbers` 8 材料 × 3 値、`theme_A_g_factor/2026-05-23_31374dc/MANIFEST.json` `key_numbers` 9 項目
- コード: `src/perovskite_tb/models_kashikar.py` で 13-orbital と 4-orbital 両モデル存在を確認

---

## 全体所見

**Round 1 指摘 17 件中 13 件は完全に修正、4 件は honest hedging で当面解消。新規重大指摘は 1 件（minor）。**

| Round 1 ID | 修正状態 | Round 2 判定 |
|---|---|---|
| A1 (Nature 暦) | 前ラウンドで in-repo arXiv:2112.15384 に置換済 | ✅ |
| A2/O1 (Kashikar 命名) | "13 軌道 active basis（同論文は 4 軌道 minimal も提案）" に統一 | ✅ PDF/コード両方と整合 |
| A3 (key_numbers 網羅) | ヘッダを「主要数値=key_numbers / 全表=CSV」に明確化 | ✅ CSV `g_factor_9material.csv` 存在確認 |
| A4 (Roth-Lax 1959) | "巻号要原典確認・in-repo 外" + in-repo Roth1960 主引用 | ✅ honest |
| A5 (Nestoklon 2023 役割) | "CsPbX₃ ナノ結晶 ETB+k·p 量子閉じ込め拡張" | ✅ |
| F1 (0.18→0.17) | 0.17 に訂正 | ✅ MANIFEST 0.17458 と一致 |
| F2 (6-9 行圧縮) | 9 行に展開、gap 列完備 | ✅ |
| F3 (Blount 1962) | "in-repo 外, 要原典確認" | ✅ honest |
| ★F4 (Tan & Rappe 訂正) | **Cowork 指摘を訂正**: in-repo `doi_10.1038_npjcompumats.2016.26.pdf` 在中、SSH/Rice-Mele Eq.(14) 明示 | ✅ Cowork 側の見落とし。Claude Code の訂正受諾 |
| P1 (Apergi CD) | "表題は CD だが本研究は速度行列要素 ε(ω) Eq.3/4 を参照" + Kubo-Greenwood 別出典 | ✅ |
| P2 (f-sum<1) | "in-repo 外, 要原典確認" | ✅ honest |
| P3 (ε∞/Theme I 接続) | "Theme I は実際は MP DFPT を採用; Phase 1.5 値は将来利用検討" | ✅ |
| ★I1 (8 材料→6 材料) | CsGeBr₃ 19, CsSnBr₃ 12 追加で 8 行に。CsSnCl₃ 除外理由明記 | ✅ MANIFEST 値完全一致 |
| ★I2 (Cho 因果誤り) | "本研究 μ=0.0592 + Cho ε=6.1 で 22 meV (Cho 自身 μ=0.10 で 37 meV; 実験 7.4–50 meV)" + ε=6.1 は 2D 層値 caveat。**全 7 箇所で統一** | ✅ 横断 grep で "15-20 meV" 完全消去確認 |
| I3 (Yang 2017/Tanaka 2003) | "in-repo 外, 要原典確認" | ✅ honest |
| O2 (g_e 普遍性) | "k·p 普遍曲線にほぼ載る（普遍式は SOC Δ 依存を内包する見かけの普遍性）" | ✅ theme_A と整合 |
| O3 (64 meV 出典) | "実験報告値 ~64 meV〔CsPbCl₃ 励起子, 要原典確認〕" | ✅ honest |

---

## §1. 新規指摘（Round 2 で発見）

### R2-1 ★ MANIFEST `notes` 内の "experiment ~15-20 meV" が未修正
- **箇所:** `results/production/theme_I_exciton_MP_DFPT/2026-05-24_118b3ce/MANIFEST.json` の `notes` フィールド:
  > "...CsPbI3 here ~41 meV vs **experiment ~15-20 meV**."
- **問題:** Round 1 I2 で全レポートの「実験 ~15–20 meV」を "7.4–50 meV (Cho 2019)" に統一したが、**MANIFEST `notes` だけ取り残し**。データ provenance としての一貫性が崩れる。
- **影響度:** 低（MANIFEST notes は公開報告書ではないが、本番計算ルール §8 の honest 記述原則からは MANIFEST も一致すべき）
- **修正方針（いずれか）:**
  - (a) 当該 MANIFEST の `notes` を更新（git_dirty:true になるのを避けるため、新規 retroactive bundle ではなく単独 commit で notes のみ修正）
  - (b) 補足 README を bundle 内に追加し「notes 内 ~15-20 meV は旧記述; 正しい範囲は 7.4–50 meV (Cho 2019)」を明記
  - **推奨: (b)** — 元 MANIFEST は計算実行時点の snapshot として不変、後追い訂正は README で
- **優先度:** 中（PI レポート修正サイクルが落ち着いた次の機会で対応）

---

## §2. Round 1 「PDF 未収」4 件の Round 2 解決状況

A4/F3/P2/I3 (Roth-Lax 1959 / Blount 1962 / Yang 2017 / Tanaka 2003) は当面 "in-repo 外, 要原典確認" で honest 化したが、本ラウンドで PDF 収集の優先順位を確定:

| 文献 | 優先 | 入手見込み |
|---|---|---|
| Yang 2017 PRB 96, 035301 | **高** (Wannier-Mott 直接出典) | arXiv 版検索（"Yang 2017 perovskite Wannier-Mott exciton"）の余地あり |
| Tanaka 2003 SSC 127, 619 | **高** (CsPbCl₃ E_b=64 meV 実験出典) | Elsevier paywall、レビュー論文（例: Quan 2019）で二次引用が現実的 |
| Blount 1962 PR 126, 1636 | 中 (f-sum 議論の原典) | APS paywall、Yu & Cardona 教科書で代替可 |
| Roth-Lax 1959 PR 114, 90 | 低 (Roth 1960 が in-repo にあり主引用可) | APS paywall、二次文献で十分 |

→ **次サイクル（PDF 収集 patrol）で Yang 2017 と Tanaka 2003 を WebFetch/WebSearch で当たる**ことを推奨。Blount/Roth-Lax は教科書引用で十分。

---

## §3. 数値照合の再確認

`PI_explained_theme_I.md` の表に追加された 2 材料を MANIFEST と再 cross-check:

| 材料 | 報告書 E_b (meV) | MANIFEST E_b (meV) | 一致 |
|---|---|---|---|
| CsGeBr₃ | 19 | 19.0 | ✅ |
| CsSnBr₃ | 12 | 11.6 → 12 (round) | ✅ |

既存 6 材料も含め 8/8 一致。捏造ゼロ維持。

---

## §4. ラウンドカウンタ更新

- Round 1: Cowork 17 + Claude Code 4（重複含む）= 16 unique findings, 全件対応
- Round 2: Cowork **1 件（R2-1, minor）** + Claude Code 自己レビュー結果待ち
- **連続 0 指摘ラウンド: 0**（R2-1 が出たためリセット継続）
- 合格条件まで: あと **連続 3 ラウンド両者ゼロ** が必要

---

## §5. 次アクション

### Claude Code（Round 2 finishing）
1. **R2-1 への対応**: README 追加 (推奨案 b) or MANIFEST notes 修正
2. **Round 2 自己レビュー** を独立に実施（指摘ゼロ目標）
3. commit message: `review round 2 (claude code + cowork): N findings addressed`

### Cowork（Round 3）
1. 上記 commit 後、再度 PI_explained 4 本 + overview + theme_I_exciton を独立レビュー
2. 指摘ゼロなら **連続 0 指摘ラウンドカウンタ +1** を `2026-05-24_HHMM_review_round_3_cowork.md` で宣言

### PDF 収集（並行 task, 緊急性中）
1. Yang 2017 PRB 96, 035301 の arXiv 版を WebSearch
2. Tanaka 2003 の二次引用を Quan 2019 等のレビューから抽出
3. 取得した PDF は `references/pdfs/` に配置、`references/references.md` の「arXiv 外 追加分」セクションに追記

---

## §6. Round 2 完了の宣言

- Cowork supervisor のラウンド 2 レビューは **本ファイル commit をもって完了**
- 主要 17 件の Round 1 指摘は全件適切に対応。**Round 1 → Round 2 のサイクルは健全に機能している**
- 新規発見は minor 1 件のみ → 全体方向性は順調、最終クリーン化まで残り 2-3 ラウンド程度の見込み
- R6-R10 (technical reports `theme_*.md` × 5) のラウンド 1 レビューは次 patrol サイクル以降

---

## 数値照合の総括（再宣言）

全 PI_explained 4 本 + overview + theme_I_exciton の表中数値は MANIFEST と完全一致（丸めの範囲内）。捏造ゼロを再確認。
