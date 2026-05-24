# Theme I: 立方晶 CsBX₃ の励起子結合エネルギー（TB 有効質量 + Materials Project DFPT ε∞ hybrid）

**ステータス（論文化方針, PI 判断 2026-05-24）:** **主結果 = option C'**（Materials Project DFPT bare ε∞ による
**8 材料**絶対 E_b マップ）、**校正点として option D' を併記**（Cho 2019 実効 ε_eff による CsPbI₃ 単独 E_b=22 meV、
実験 7.4–50 meV (Cho 2019) の範囲内）。C' の絶対値は bare ε∞ 由来で**上限**、相対トレンドが頑健、と honest に位置づける。
数値は Production MANIFEST 引用: `theme_I_exciton_MP_DFPT/2026-05-24_118b3ce`（C'）, `theme_I_exciton/2026-05-23_f66690c`（D'）,
`theme_I_effective_mass/2026-05-23_1e9c65c`（μ）。

## Abstract（主結果）
9 材料の TB 有効質量から換算質量 μ を出し、**Materials Project の DFPT 高周波誘電率 ε∞（単一手法）**を用いて
Wannier-Mott 励起子結合エネルギー E_b の 8 材料マップ（C'）を構築。E_b は Cl 系で最大（CsPbCl₃ 119 meV）、
Sn-I で最小（CsSnI₃ 4 meV）。単一手法ゆえ**相対トレンドは defensible**。絶対値は bare ε∞（<実効 ε_eff）由来で上限：
CsPbI₃ は C' で 41 meV だが、実効 ε_eff≈6.1（D' 校正）では 22 meV で実験整合。bare ε vs ε_eff の差は本研究の方法論的考察（§4）。

---

## 1. Background
ハライドペロブスカイトの励起子結合エネルギー E_b（実験で数〜数百 meV）は LED 発光効率・太陽電池のキャリア分離を左右する。
TB 有効質量 + Wannier-Mott 水素様模型 `E_b=(μ/m₀)/ε_r²·Ry`（Ry=13.6057 eV, 1/μ=1/m_e+1/|m_h|）で推定する。

## 2. Method（hybrid: 誤差ソースの分離）
- **μ（TB 由来・信頼可）**: R 点（直接ギャップ端）バンド曲率 `m*/m₀=(ℏ²/m₀)/(d²E/dk²)`、ℏ²/m₀=7.619964 eV·Å²、
  Kashikar-13, n_occ=20, 3 軸平均。立方等方。bundle `theme_I_effective_mass/2026-05-23_1e9c65c`。
- **ε∞（C' 主, Materials Project DFPT）**: `src/perovskite_tb/materials_project.py`（PI 提供 API キー, gitignored, 非ロギング）。
  **単一手法**で 9 材料中 8 材料取得（CsSnCl₃ は MP に dielectric なし）。
- **ε_eff（D' 校正, 文献実効値）**: CsPbI₃ のみ Cho 2019 (arXiv:1908.09436) の effective ε≈6.1。
- → **μ=TB / ε=外部** と誤差源を明確分離。実装: `scripts/scan_theme_I_binding_energy.py --profile MP_DFPT`。

## 3. Results

### 3.1 ★ 主結果（option C'）: Materials Project DFPT ε∞ による 8 材料 絶対 E_b マップ
bundle `results/production/theme_I_exciton_MP_DFPT/2026-05-24_118b3ce/`（MANIFEST 引用、出典＝各 mp-id）。

| 材料 | μ | ε∞ (MP DFPT, phase) | E_b (meV) |
|---|---|---|---|
| CsPbCl₃ | 0.116 | 3.64 (mp-675022, R32) | **119** |
| CsGeCl₃ | 0.097 | 3.64 (mp-22988, R3m) | 99 |
| CsPbBr₃ | 0.074 | 4.21 (mp-567629, Pnma) | 57 |
| CsPbI₃ | 0.059 | 4.43 (mp-540839, Pnma) | 41 |
| CsGeI₃ | 0.053 | 5.69 (mp-642690, Cm) | 22 |
| CsGeBr₃ | 0.060 | 6.55 (mp-570223, **Pm-3m**) | 19 |
| CsSnBr₃ | 0.030 | 5.91 (mp-27214, **Pm-3m**) | 12 |
| CsSnI₃ | 0.015 | 7.35 (mp-614013, **Pm-3m**) | **4** |
| CsSnCl₃ | — | MP に dielectric なし | — |

- **単一手法 DFPT → 相対トレンドが defensible 最高**。E_b は Cl 系最大（μ 大・ε 小）、Sn-I 最小（μ=0.015 超軽 + ε 大）。
- **絶対値は上限**: MP の ε∞ は bare 電子値（フォノン/イオン遮蔽なし, ε∞<ε_eff）→ E_b 過大。§4 で考察。
- **相注記**: MP は cubic Pm-3m の dielectric を一部材料（CsGeBr₃/CsSnBr₃/CsSnI₃）のみ計算済み。他は基底状態相
  （ortho/rhombo/monoclinic）の ε∞ を ~相非依存 proxy として使用（μ は cubic）。CsSnCl₃ は除外。

### 3.2 校正点（option D'）: CsPbI₃ 実効 ε_eff
bundle `theme_I_exciton/2026-05-23_f66690c`。CsPbI₃ に Cho 2019 の実効 ε=6.1 と本研究 μ=0.0592 を使うと **E_b=22 meV**（Cho 自身は μ=0.10 で 37 meV と報告; 実験範囲 7.4–50 meV, Cho 2019）。→ C' の CsPbI₃（bare ε=4.43, 41 meV）に対し、**実効 ε で絶対値が実験域に入る**ことを示す校正点。
（C' 41 meV ÷ D' 22 meV ≈ 1.9 倍が bare→実効の補正係数の目安。）

### 3.3 入力データ: 有効質量マップ（TB, 確定）
`theme_I_effective_mass/2026-05-23_1e9c65c`（異方性比=1.0000 立方等方、dk<0.01% 収束）。
代表値: CsPbI₃ m_e=0.106/m_h=0.134/μ=0.059（文献 ~0.1–0.15 整合）、CsSnI₃ μ=0.015（最軽）、CsPbCl₃ μ=0.116（最重）。
質量は Cl→Br→I で軽量化、Sn 系最軽。全 9 材料は bundle CSV。

## 4. Discussion（方法論的考察）
- **★ bare ε∞ vs 実効 ε_eff**: Wannier-Mott が要するのは励起子が感じる**実効遮蔽 ε_eff**（ε∞ と ε_static の中間、
  フォノン寄与込み）。文献・DFPT が出すのは **bare 電子 ε∞**で、ε∞<ε_eff のため **bare で計算すると E_b 過大**。
  CsPbI₃ で実証: bare ε=4.43→41 meV vs 実効 ε=6.1→22 meV（本研究 μ; 実験 7.4–50 meV, Cho 2019）。
- **web research の結論（経緯）**: open web には 9 材料の consistent な cubic ε（特に ε_eff）が無い（paywall/相不一致/手法散乱）。
  そこで PI 提供キーで **MP DFPT（単一手法）** に切替え、相対トレンドの defensibility を確保（C'）。
- **Blount 統一限界**: ε∞ の過小は g 因子・光学 f-sum と同じ Blount 1962（TB 位置演算子の原子内成分欠落）の糸。
  相対傾向は信頼可、絶対値は要 Wannier 化。

## 5. Conclusions
- **主結果（C'）**: MP DFPT ε∞ による 8 材料 E_b マップ。相対トレンド（Cl 系大・Sn-I 小）defensible、絶対値は上限。
- **校正点（D'）**: CsPbI₃ 実効 ε_eff で E_b=22 meV、実験整合 → C' の bare ε∞ 由来 overestimate（~1.9×）を定量化。
- **有効質量マップ**（信頼可・publishable, 立方等方）は独立した確定成果。
- **LED 示唆**: Cl 系（大 E_b）は励起子発光が明るい候補、Sn-I（小 E_b）は太陽電池向き（自由キャリア寄り）。
- **論文化骨子**: `cowork/reports/theme_I_publication_outline.md`。

## 6. References
- Wannier-Mott 適用例（Yang 2017 PRB 96 035301 = 記憶ベース, 要原典確認）。Tanaka et al. 2003, SSC 127, 619（巻号確認済; 対象は MAPbBr₃/MAPbI₃, CsPbCl₃ ではない）。
- J. Cho et al. 2019, arXiv:1908.09436（実効 ε≈6.1, D' 校正）。
- A. Jain et al. 2013, *APL Mater.* 1, 011002（Materials Project, DFPT 誘電率, C'）。
- R. Kashikar et al. 2021, arXiv:2101.08562（TB モデル）。E. I. Blount 1962, *Phys. Rev.* 126, 1636（TB 限界）。
- Production bundles: `theme_I_exciton_MP_DFPT/2026-05-24_118b3ce`（C'）, `theme_I_exciton/2026-05-23_f66690c`（D'）,
  `theme_I_effective_mass/2026-05-23_1e9c65c`（μ）。ε∞ 出典詳細: `data/parameters/eps_inf_external.json`。
