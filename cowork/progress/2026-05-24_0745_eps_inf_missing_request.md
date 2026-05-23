# ε_∞ 補完依頼 — 2026-05-24 07:45

directive 補足 `0735_directive_supplement_eps_inf_fallback.md` の通り、`references/texts/`（61 本）から
ε_∞ が見つからなかった材料を Cowork の Claude-in-Chrome 検索に依頼します。
**Claude Code は手を止めず**、`data/parameters/eps_inf_external.json` に `pending_cowork_chrome_search` で暫定マーク済み。

Y1-c-1 で `references/texts/` から ε_∞ が見つからなかった材料（8/9）:

| 材料 | phase | 探した keywords | 探した arxiv_ids | 備考 |
|---|---|---|---|---|
| CsPbBr₃ | cubic | ε_∞, eps_inf, high-frequency dielectric, optical dielectric, refractive index | 1908.09436, 2210.01324, 1601.01201, 1703.03574, 1802.09677 | Pb-Br、実験 ε_∞ あるはず |
| CsPbCl₃ | cubic | 同上 | 同上 | wide-gap、ε_∞ 小さめ想定 |
| CsSnI₃ | cubic | ε_∞, eps_inf, high-frequency dielectric, CsSn | 全 references/texts | Sn 系は文献少なめ、small-gap |
| CsSnBr₃ | cubic | 同上 | 全 references/texts | Sn 系 |
| CsSnCl₃ | cubic | 同上 | 全 references/texts | Sn 系、wide-gap |
| CsGeI₃ | cubic | ε_∞, eps_inf, high-frequency dielectric, CsGe | 全 references/texts | Ge 系、強誘電性あり（菱面体）注意 |
| CsGeBr₃ | cubic | 同上 | 全 references/texts | Ge 系 |
| CsGeCl₃ | cubic | 同上 | 全 references/texts | Ge 系、wide-gap |

**CsPbI₃** は MAPbI₃ proxy（ε_p=6.1, Cho 2019 / arXiv:2210.01324）を暫定使用中。CsPbI₃ 固有の cited 値があれば置換歓迎。

Cowork へ（補足 §55-64 の手順）: Materials Project → NoMaD → Google Scholar（実験優先）→ arXiv の順で検索し、
**出典（URL/DOI/arXiv ID + 表/式番号 + 取得日）を必ず併記**して `data/parameters/eps_inf_external.json` を直接 edit、
完了通知 `*_eps_inf_search_complete.md` をお願いします。URL が開けない/抽出不能なら「未取得」と明示（捏造禁止）。

補完値が json に入り次第、Claude Code は次の polling cycle で検出 → `scripts/scan_theme_I_binding_energy.py` で
Y1-c-3（E_b Production）を全材料 run します（script は本依頼と同時に準備済み）。

## sanity check 基準（Y1-c-2, Cowork 検索値の検証用）
- 物理範囲: 1 < ε_∞ < 20（ハライドペロブスカイト典型 3-8）。
- トレンド: 同 B-cation 内で Cl < Br < I（gap 減で ε_∞ 増）。反例は出典再確認。
- 2 ソース以上で ±20% 以内ならどちらか採用 + notes 記載、それ以上は PI 判断。
