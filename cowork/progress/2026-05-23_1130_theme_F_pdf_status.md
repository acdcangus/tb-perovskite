# Theme F PDF status (F1) — 2026-05-23 11:30

directive update (1055) §1.1 + correction (1110) を踏まえ、`references/pdfs/` を確認・取得。
**取得時にタイトルを必ず検証**（ハルシネーション防止）したところ、Cowork が「推定/可能性」と
注記した 2 つの arXiv ID が**別分野の無関係論文**だったため削除しました。

## 取得・検証結果
| 出典 | arXiv ID | 状態 | 検証タイトル |
|---|---|---|---|
| Passos et al. 2018（**primary**, velocity-gauge TB nonlinear optics, PRB 97, 235446） | **1712.04924** | ✅ 取得・検証OK | "Nonlinear optical responses of crystalline systems: Results from a velocity gauge analysis" (Passos, Ventura, Lopes, dos Santos) |
| Sheikhabadi et al. 2022（sub, disorder 2nd-order） | **2207.00331** | ✅ 取得・検証OK | "Theory of nonlinear optical response" (Sheikhabadi, Bagheri, Sadeghi) ← correction 1110 と一致 |
| BPVE 背景（既収集） | 2105.11310 | ✅ 既存 | (Rajpurohit et al., bulk photovoltaic) |
| **Young & Rappe 2012**（必須, PRL 109, 116601） | ~~1207.5462~~ | ❌ **ID 誤り** | 1207.5462 は "Limit points of the iterative scaling procedure" (Erik Aas, 統計) ＝**無関係**。削除済み |
| **Fregoso 2017**（あれば便利, PRB 96, 075421） | ~~1612.09194~~ | ❌ **ID 誤り** | 1612.09194 は "On the local Birkhoff conjecture for convex billiards" (Kaloshin) ＝**無関係**。削除済み |
| **Tan & Rappe 2016**（必須, npj Comput. Mater. 2, 16026） | 不明 | ❌ 未取得 | arXiv ID 不明。Cowork 取得待ち |

## Cowork へのお願い（正しい ID/PDF 取得）
1. **Young & Rappe 2012 (PRL 109, 116601)** の正しい arXiv ID（1207.5462 は誤り）。
   - shift current の第一原理公式の原典。F2 では directive 引用式 + Sipe-Shkrebtii 形式で代替し、
     PDF 取得後にピーク値・符号を照合する。
2. **Tan & Rappe 2016 (npj Comput. Mater. 2, 16026)** — 検証アンカー（MAPbI₃ shift current
     ピーク位置・振幅）の出典。OA のはず。
3. **Fregoso 2017 (PRB 96, 075421)** の正しい arXiv ID（1612.09194 は誤り）。shift vector 形式。
   - 真の ID は arXiv:1612.09155 などの可能性（未確認）。Cowork で 1 次情報確認をお願いします。

## F2 への影響
- **primary methodological ref (Passos 2018, 1712.04924) は取得済み**なので **F2 着手に支障なし**
  （directive correction 1110 §4.4 の新 fallback を満たす）。
- 検証アンカー（Tan & Rappe MAPbI₃ ピーク）は **プレースホルダ**で記述し、PDF 取得後に確定。
- F2 で Young&Rappe / Fregoso を引用する箇所は「PDF 未取得・式は Sipe-Shkrebtii / Passos 2018
  から再構成」と明示。

## 次
- arxiv_1712.04924 (Passos 2018) と arxiv_2105.11310 (BPVE) を読み、F2
  `docs/shift-current-formulation.md` draft を書く。F3（実装）は F2 の Cowork 承認待ち。
