# Theme I 完了（option D' closeout）— 2026-05-24 09:25

PI「続けて」+ 0915 web research の結果に基づき、Theme I を **option (D')** で確定（最も honest・捏造ゼロ）。
(C') Materials Project は API key 不可、(B') 実験 ε_eff は鉛フリーで希少のため、自走で完了できる (D') を採用。

## 確定成果（directive 0715 Y1-a〜Y1-d 対応）

| 成果 | 状態 | 場所 |
|---|---|---|
| Y2 MIT LICENSE (© tk) | ✅ | `LICENSE`, SPDX headers |
| Y1-a 有効質量マップ（9 材料, 信頼可） | ✅ Production | `results/production/theme_I_effective_mass/2026-05-23_1e9c65c/`（dirty:false, 異方性=1, dk<0.01%） |
| E_b 相対トレンド（9 材料, TB-optical ε_∞, 相対のみ） | ✅ Production | `results/production/theme_I_exciton/2026-05-23_f66690c/` |
| Y1-c ε_∞ web research（出典付き） | ✅ | `data/parameters/eps_inf_external.json`（CsPbI₃ 6.1 / CsPbCl₃ 2.4 / 他 not-found） |
| Y1-d 報告書 | ✅ | `cowork/reports/theme_I_exciton.md` |

## 主結果
- **有効質量マップ**（一次成果, publishable）: CsPbI₃ m_e=0.106/m_h=0.134（文献整合）、Cl→Br→I で軽量化、CsSnI₃ 最軽（μ=0.015）、立方等方性。
- **CsPbI₃ E_b=22 meV**（effective ε=6.1）実験整合 — 絶対値の校正点。
- **★ 方法論的発見**: Wannier-Mott は bare ε_∞ でなく effective ε_eff を要し、bare ε_∞ は E_b を過大評価（CsPbCl₃ 2.4→273 meV vs 実験 64）。鉛フリー族の絶対 E_b は ε_eff データ不足で未確定。

## 未確定（将来, 要 PI 判断）
- 絶対 9 材料 E_b マップ: Materials Project DFPT ε_∞（API key 要）or 実験 ε_eff が得られれば `scan_theme_I_binding_energy.py` で即算出。

## PRODUCTION_RULES 準拠
- 全 bundle git_dirty:false、MANIFEST 8 フィールド完備、報告書数値は MANIFEST 引用。

→ Theme I は (D') で完了とします。次テーマ/指示があれば `next_directive.md` で。5 分巡回で cowork/ 継続確認。
