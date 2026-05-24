# Y1-c ε_∞ web research 完了（PI 指示「自分でやって」）— ★ 方法論的限界が判明 — 2026-05-24 09:15

**PI 指示**「webresearch 自分でやって」を受領 → Claude Code が WebSearch/WebFetch で ε_∞ を自力調査（~12 件）。
**Cowork の Chrome 検索（plan B）は不要**になりました（重複回避のため、0940 plan B は中止してください）。

## 1. 調査結果（出典は `data/parameters/eps_inf_external.json`、捏造なし）

| 材料 | ε (source) | 状態 |
|---|---|---|
| CsPbI₃ | **6.1**（Cho 2019 arXiv:1908.09436 effective; crystal static 6.22, S1876107018306059） | found（effective, 物理的） |
| CsPbCl₃ | **2.4**（PMC12757862 LST ε_∞=2.40; PMC9071989 ε≈2.51, DFT TB09） | found（**bare** ε_∞） |
| 他 7 材料 | — | open web で**信頼値得られず**（paywall / 相不一致(rhombohedral) / 手法散乱） |

## 2. ★ 重要な方法論的発見（捏造防止の核心）

- 文献が報告するのは **bare 電子 ε_∞**。だが Wannier-Mott が要するのは **effective ε_eff**（ε_∞〜ε_static 中間、フォノン込み）。
- **bare ε_∞ を使うと E_b 過大**: CsPbCl₃ ε_∞=2.4 → E_b=**273 meV**（実験 ~64 meV の ~4×）。実験 E_b から逆算 ε_eff≈5.0。
- CsPbI₃ で 22 meV（実験整合）になるのは **6.1 が effective ε**（Cho の励起子遮蔽）だから。
- → **鉛フリー族の絶対 E_b は bare ε_∞ からは信頼計算不可**。物理的 ε_eff は CsPbI₃ 型のみ入手可。

## 3. なぜ 9 材料そろわないか（honest）

- open web に **9 材料の consistent な cubic ε（特に ε_eff）が無い**: Sn/Ge ハライドは (a) paywall（Springer 等）、
  (b) cubic でなく rhombohedral 相（CsGeI₃ PMC9833107）、(c) static（格子支配）のみで ε_∞ 数値なし（CsGeI₃ OSTI/RSC）、
  (d) 図のみで zero-frequency 値が本文に無い（CsSnI₃-xBrx）。
- bare ε_∞ を寄せ集めても **手法バラバラ + そもそも ε_eff でない**ため、絶対 E_b マップは defensible にならない。

## 4. 推奨（PI 判断）

- **(D') 確定**: Theme I = **有効質量マップ（信頼可）+ E_b 相対トレンド + CsPbI₃ 校正点 22 meV**（実験整合）。絶対 9 材料 E_b は見送り。**推奨**（最も honest、捏造ゼロ）。
- **(C') Materials Project**: 単一手法 DFPT の ε_∞ を 9 材料分（mp-ID 経由）取得すれば consistent な set になるが、(i) ε_eff でなく ε_∞ なので E_b は依然過大、(ii) MP API key が要（私の環境から query 不可）。PI が MP key/値を提供できるなら実施可。
- **(B') 実験 ε_eff**: 励起子論文の ε_eff を材料ごとに収集（CsPbI₃ 以外は文献希少）。

→ **(D') を推奨**。E_b の Production bundle は作らず（bare ε_∞ の非物理値を bundle しない）、報告書 `theme_I_exciton.md` §3.2 に
本finding を記載済み。`scan_theme_I_binding_energy.py` は ε_eff が手に入れば即 run 可能な状態で保持。

## 5. 状態
- 有効質量マップ bundle `theme_I_effective_mass/2026-05-23_1e9c65c`（確定）/ 報告書 `theme_I_exciton.md`（§3.2 更新済み）。
- `eps_inf_external.json`（出典・finding 記録済み）。PI 判断（D'/C'/B'）待ち。
