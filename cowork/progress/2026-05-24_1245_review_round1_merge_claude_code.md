# Review Round 1 — Claude Code × Cowork 指摘マージ・対応完了 — 2026-05-24 12:45

Cowork 独立レビュー（`1230_review_round_1_cowork.md`, 17 件）+ 自己レビュー（`1220`）をマージし、PDF/MANIFEST 照合の上で対応。

## 対応済み（PDF/MANIFEST で検証して修正）
| ID | 内容 | 対応 |
|---|---|---|
| A1 | "Nature 暦" 壊れ引用 | in-repo arXiv:2112.15384 に置換（前ラウンドで対応済） |
| A2/O1 | 「Kashikar-13」命名 | Kashikar PDF abstract 確認（"thirteen orbitals active" + "four orbital minimal"）→「13 軌道 active basis（同論文は 4 軌道 minimal も提案）」に明確化 |
| A3 | MANIFEST 引用範囲 | ヘッダを「主要数値=key_numbers / 全表=bundle CSV」に訂正 |
| A5 | Nestoklon 2023 役割 | arXiv:2305.10586（CsPbX₃ ナノ結晶 ETB+k·p 量子閉じ込め拡張）と正確化 |
| F1 | CsSnI₃ gap 0.18 | MANIFEST 0.17458 → **0.17** に訂正 |
| F2 | 表 6–9 行圧縮 | 9 材料すべて材料/σ/gap の統一行に展開 |
| ★I1 | E_b 表が 6/8 材料 | CsGeBr₃(19)・CsSnBr₃(12) を追加し 8 材料に |
| ★I2 | Cho 2019 引用の因果誤り | Cho PDF 確認（μ=0.10 で **37 meV**, 実験 **7.4–50 meV**, ε=6.1 は **2D 無機層**値）→「本研究 μ=0.0592 + Cho ε=6.1 で 22 meV（Cho 自身 37 meV; 実験 7.4–50 meV; bulk 転用は近似）」に全面訂正。**全レポートの「実験 ~15–20 meV」を「7.4–50 meV (Cho 2019)」に統一** |
| P1 | Apergi 2023 文脈 | Apergi PDF 確認（題目=円二色性 CD）→「CD 論文だが速度行列要素ベース ε(ω) の具体形 Eq.3/4 を参照、一般 Kubo-Greenwood は Kubo1957/Greenwood1958」に限定 |
| P3 | ε∞ と Theme I 接続 | 「Theme I は実際は MP DFPT ε∞ を採用、Phase 1.5 値は将来利用」に訂正 |
| O2 | overview g_e 普遍性 | theme_A と整合させ「k·p 普遍曲線にほぼ載るが Δ 依存を内包する見かけの普遍性」に |
| O3 | 実験 64 meV 出典 | 「文献報告値, 要原典確認」と明記 |

## ★ Cowork 指摘の訂正（1 件）
- **F4: 「Tan & Rappe 2016 は PDF library 未収」は誤り。** `references/pdfs/doi_10.1038_npjcompumats.2016.26.pdf` に**在中**（F4-2 で照合済）。
  該当の対称則は同論文 Eq.(14) SSH/Rice-Mele 模型に基づく旨を明記。

## Round 2 へ持ち越し（in-repo 外文献, 要 PDF 収集 = Cowork/PI 側）
A4/F3/P2/I3: Roth-Lax 1959・Blount 1962・Yang 2017・Tanaka 2003 は `references/pdfs/` 未収。
当面「in-repo 外, 要原典確認」と明記して honest 化。Round 2 前に PDF 収集（Cowork §6 リスト）or 二次文献化で確定。

## 数値照合
全レポートの核心数値は MANIFEST と一致（捏造ゼロ）を再確認。コード変更なし → **231 テスト不変**。

## カウンタ
本ラウンドで両者とも指摘あり → 連続 0 カウンタは未確立（リセット状態）。修正 commit 後、Cowork の Round 2 独立レビューへ。
