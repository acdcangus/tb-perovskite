# Review Round 1 — Claude Code 自己レビュー（standing rule 1200）— 2026-05-24 12:20

形式: `[ファイル]:行 — 種別 — 詳細 — 解決`

## A. 数値照合（全レポート ↔ Production MANIFEST key_numbers）— ✅ PASS
spot-check で核心数値はすべて MANIFEST と一致（捏造なし）:
- optical: ε_∞ 3.46/2.35/1.46, f-sum 0.21, abs_edge 1.79 ✓
- theme_A: g_e 3.01/4.56/3.39, g_h_dev 1.86/1.81 ✓
- theme_F: peak −3.43/−2.67/+0.97 (MANIFEST −3.426/−2.672/+0.965, 丸め一致) ✓
- theme_I_MP: E_b CsPbCl₃ 118.6→119, CsSnI₃ 3.7→4（丸め一致, 報告でも 119/4 表記）✓

## B. PI_explained_theme_A.md — 指摘 4 件（本ラウンドで修正済み, commit 後）
- L133 — **ハルシネーション（garble）** — "*Nature* 暦" という壊れた引用 — **修正**: in-repo `arXiv:2112.15384`（実在・タイトル確認）に置換。
- L61/L103/L112/L35 — **記憶ベース引用** — "Kirstein 2021/2022 (Nature) Eq.5/6" 等、巻号・式番号が記憶 — **修正**: in-repo arXiv:2112.15384 に統一、式定数は検証済み `docs/g-factor-formulation.md` 参照に格下げ。
- L137 — **記憶ベース巻号** — "Roth-Lax-Zwerdling 1959 PR 114,90" は in-repo 外で巻号が記憶 — **修正**: in-repo `classic_Roth1960_PR118_1534.pdf`（Roth 1960）を主引用にし、1959 は「巻号要原典確認・in-repo 外」と明記。

## C. 残（Round 1 継続対象, R3–R10）
以下は次の Round 1 サイクルで in-repo PDF 照合 or softening する（記憶ベース疑い）:
- **実験 E_b 値**（CsPbI₃ ~15–20 meV, CsPbCl₃ ~64 meV, CsPbBr₃ ~40 meV）: 出典 PDF に遡れるか確認、不可なら「文献典型値（要確認）」化。
- **記憶ベース引用 metadata**: Yang 2017 PRB 96 035301 / Tanaka 2003 SSC 127 619（theme_I）, Apergi 2023（→ in-repo arXiv:2309.14002 に統一可）, Young&Rappe/Tan&Rappe/Fregoso（これらは in-repo PDF あり, 照合容易）。
- in-repo 確認済み（照合容易）: 1202.3168, 1701.00172, 1908.09436, 2101.08562, npjcompumats.2016.26, 2112.15384, 2309.14002。

## ステータス
- Round 1 は **theme_A 完了（修正 commit 済）**、数値照合は全レポート PASS。R3–R10 の引用 metadata/実験値照合は継続中。
- 3 ラウンド連続 0 指摘にはまだ遠い（本ラウンドで指摘ありのためカウンタ未確立）。Cowork の独立 Round 1 と合わせて継続。
