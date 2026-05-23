# Y1-c-1 ε_∞ 抽出結果 — ★ 8/9 材料が in-repo 文献に無し → PI 判断要請 — 2026-05-24 07:35

directive `0715_directive_theme_I_hybrid_and_license.md` Y1-c-1 を実施。
**directive §199 の「多数の材料で見つからない場合は一旦止めて PI 確認」に該当**するため、ここで停止して報告します。

## 抽出方法
`references/texts/*.txt`（61 ファイル）を grep:
high-frequency / optical dielectric, `ε∞ / ϵ∞ / epsilon_inf`, refractive index, dielectric constant + 材料名近接。

## 結果（出典付き、捏造なし）→ `data/parameters/eps_inf_external.json`

| 材料 | ε_∞ | 状態 |
|---|---|---|
| CsPbI₃ | **6.1**（proxy） | Cho 2019 (arXiv:1908.09436, ε=6.1) / arXiv:2210.01324 (ϵ_p=6.1, **bulk MAPbI₃ high-freq dielectric**)。**MAPbI₃ 由来の effective 値**で CsPbI₃ 実測 ε_∞ ではない。proxy。 |
| CsPbBr₃, CsPbCl₃ | — | **not_found**（in-repo に無し） |
| CsSnI₃/Br₃/Cl₃ | — | **not_found**（Sn ハライドの ε_∞ は in-repo にゼロ） |
| CsGeI₃/Br₃/Cl₃ | — | **not_found**（Ge ハライドの ε_∞ は in-repo にゼロ） |

- 唯一の値も **MAPbI₃ の effective ε_p（6.1）**で、(i) Cs 材料でない、(ii) 厳密な ε_∞ でなく ε_∞〜ε_static 中間の effective 遮蔽。
- arxiv_2605.22453 に ε∞ 表があるが **LaMoN₃（窒化物ペロブスカイト）**で無関係。
- **9 材料中 8 が in-repo 文献に ε_∞ 無し**（特に Sn/Ge 系は皆無）。

## ★ PI 判断要請（Y1-c-3 は本判断まで保留）

ハルシネーション禁止のため **Sn/Ge 等の ε_∞ を勝手に入れません**。以下から選択をお願いします:

- **(A) 外部 WebSearch を許可**: DFT-RPA データベース（Materials Project 等）/ 実験文献から 9 材料の ε_∞ を
  出典付きで収集し `eps_inf_external.json` を補完（各値 arXiv/DOI/DB-ID + 取得日を明記、捏造なし）。
- **(B) PI が ε_∞ 値を提供**（手元の DFT/実験値があれば最確実）。
- **(C) 見つかった材料のみで部分 Production**（実質 CsPbI₃ proxy のみ → E_b 1 点では bundle 価値低、非推奨）。
- **(D) Y1-c（絶対 E_b）を見送り**、Theme I は Y1-a（有効質量マップ, 完了済み）+ E_b 相対トレンドで確定。

**推奨: (A)**（directive §192 の DFT-RPA フォールバックと整合、9 材料そろえられる）。許可いただければ WebSearch で
出典付き ε_∞ を収集して Y1-c-3 を進めます。**(A) 不可なら (D)** が次善（有効質量マップは既に publishable）。

## 完了済み（参考）
- Y2（MIT LICENSE + SPDX）✅ commit `b9571a1`
- Y1-a（有効質量マップ Production）✅ bundle `theme_I_effective_mass/2026-05-23_1e9c65c`（dirty:false, anisotropy=1.0, dk<0.01% 収束）commit `72cd18a`
