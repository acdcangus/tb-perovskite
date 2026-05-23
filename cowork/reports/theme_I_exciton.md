# Theme I: Wannier-Mott exciton binding in cubic CsBX₃ (TB effective mass + external ε_∞ hybrid)

**ステータス:** Y1-a（有効質量マップ）Production 完了。Y1-c-3（E_b）は **§3.2 が Cowork の ε_∞ 検索待ち**で暫定
（CsPbI₃ proxy のみ確定）。本報告書は directive `0715` Y1-d の構成に従い、ε_∞ 充填後に E_b 表を確定する。
**bundles:** `results/production/theme_I_effective_mass/2026-05-23_1e9c65c/`（masses, 確定）。

---

## 1. Background
ハライドペロブスカイトの**励起子結合エネルギー E_b**（実験で数〜数百 meV）は LED・太陽電池の発光/分離効率を左右する。
本研究は既存 TB から**バンド端有効質量**を出し、**Wannier-Mott 水素様模型**で E_b を推定する:
`E_b = (μ/m₀)/ε_r² × Ry（13.6057 eV）`、`1/μ = 1/m_e + 1/|m_h|`（Yang 2017, Tanaka 2003）。

## 2. Method（hybrid: 誤差ソースの分離）
- **μ（TB 由来・信頼可）**: R 点（直接ギャップ端 π/a(1,1,1)）のバンド曲率 `m*/m₀=(ℏ²/m₀)/(d²E/dk²)`、
  ℏ²/m₀=7.619964 eV·Å²。Kashikar-13, n_occ=20、3 軸（[100]/[010]/[001]）。
- **ε_∞（外部・文献）**: TB-optical の ε_∞ は Blount-1962 由来の f-sum 過小（~0.21）を継承するため不採用。代わりに
  **文献（実験/DFT-RPA）の ε_∞ を外部入力**（`data/parameters/eps_inf_external.json`、出典付き）。
  → **μ=TB / ε_∞=外部** と誤差ソースを明確分離（PI directive 0715/0735）。
- 実装: `src/perovskite_tb/exciton.py`, `scripts/scan_theme_I_effective_mass.py`（Y1-a）,
  `scripts/scan_theme_I_binding_energy.py`（Y1-c-3）。

## 3. Results

### 3.1 有効質量マップ（確定・Production）
出典: `results/production/theme_I_effective_mass/2026-05-23_1e9c65c/MANIFEST.json key_numbers`。
全材料で **異方性比=1.0000（立方等方性）**、dk<0.01% 収束。

| 材料 | m_e | m_h | μ |
|---|---|---|---|
| CsGeCl₃ | 0.2283 | −0.1680 | 0.0968 |
| CsGeBr₃ | 0.1479 | −0.1007 | 0.0599 |
| CsGeI₃ | 0.1115 | −0.1001 | 0.0527 |
| CsSnCl₃ | 0.1766 | −0.1097 | 0.0677 |
| CsSnBr₃ | 0.0749 | −0.0496 | 0.0298 |
| CsSnI₃ | 0.0346 | −0.0254 | 0.0146 |
| CsPbCl₃ | 0.2371 | −0.2253 | 0.1155 |
| CsPbBr₃ | 0.1510 | −0.1439 | 0.0737 |
| CsPbI₃ | 0.1062 | −0.1338 | 0.0592 |

- **CsPbI₃ m_e=0.106/m_h=0.134** は文献（~0.1–0.15 m₀）と整合。質量は **Cl→Br→I で軽量化**、**Sn 系が最軽**（CsSnI₃ μ=0.015）。

### 3.2 E_b（暫定 — Cowork の ε_∞ 充填待ち）
`data/parameters/eps_inf_external.json` の ε_∞ が確定した材料のみ E_b を Production 化する（`scan_theme_I_binding_energy.py`）。
現状、in-repo 文献からは **CsPbI₃ の proxy（MAPbI₃ effective ε≈6.1, Cho 2019 / arXiv:2210.01324）のみ**:

| 材料 | μ | ε_∞ (source) | E_b (meV) |
|---|---|---|---|
| CsPbI₃ | 0.0592 | 6.1（MAPbI₃ proxy） | **22** |
| 他 8 材料 | （上表） | **pending Cowork Chrome search** | TBD |

- **★ 検証**: proxy ε=6.1 で CsPbI₃ E_b=**22 meV**（実験 ~15–20 meV と整合）。TB-optical ε_∞=3.46 では 67 meV（過大）。
  → **外部 ε_∞（option c）が絶対 E_b を実験域に戻す**ことを実証。残り 8 材料の cited ε_∞ が入れば 9 材料 E_b マップ確定。

## 4. Discussion
- **信頼性の分離**: μ は TB 由来で信頼可（異方性=1、dk 収束）。ε_∞ は外部依存（出典トレーサビリティを MANIFEST に明記）。E_b は両者の積。
- **比較**: CsPbI₃ proxy E_b=22 meV は実験報告（~15–20 meV）と整合。Wannier-Mott は **上限**（ε_∞ のみの遮蔽；
  実際はフォノン寄与で ε_∞<ε_eff<ε_static、E_b はやや小さくなる — Tanaka 2003 / Yang 2017）。
- **限界**: フォノン遮蔽未考慮（上限評価）。Frenkel-Wannier 遷移域材料での妥当性は別途要検討。TB intra-atomic 欠落（Blount）は μ には軽微（曲率は信頼可）、影響は主に ε_∞（→ 外部化で回避）。

## 5. Conclusions
- 9 材料の **TB 有効質量マップ**（信頼可・publishable, 異方性=1）を確定。Sn 系が最軽量。
- E_b は **μ(TB)+ε_∞(外部) hybrid** で算出する方針。CsPbI₃ proxy で実験整合（22 meV）を確認。
  残り 8 材料は Cowork の cited ε_∞ 充填後に Production 化（Y1-c-3 script 準備済み）。

## 6. References
- Yang et al. 2017, PRB 96, 035301 — halide perovskite Wannier-Mott
- Tanaka et al. 2003, Solid State Commun. 127, 619 — 励起子結合の実験
- Cho et al. 2019, arXiv:1908.09436 — GW-BSE（ε≈6.1, 質量）
- Kashikar, Gupta, Nanda 2021, arXiv:2101.08562 — TB モデル本体
- ε_∞ 各材料の出典: `data/parameters/eps_inf_external.json`（Cowork 充填後に列挙）

---
（注: 本ファイルは directive 0715 Y1-d の正規報告書。先行の `theme_I_exciton_binding.md`（自走暫定版）は本ファイルに統合・置換。）
