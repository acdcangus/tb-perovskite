# Theme I: Wannier-Mott exciton binding in cubic CsBX₃ (TB effective mass + external ε_∞ hybrid)

**ステータス:** Y1-a（有効質量マップ）Production 確定。Y1-c（E_b）は web research 実施の結果、**bare ε_∞ では絶対 E_b を
信頼計算できない**ことが判明（§3.2、要 ε_eff）。確定成果＝有効質量マップ + E_b 相対トレンド + CsPbI₃ 校正点。
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

### 3.2 E_b（web research 実施 — ★ bare ε_∞ vs ε_eff の方法論的限界が判明）
PI 指示で外部 ε_∞ を web research（WebSearch/WebFetch, ~12 件, 出典 `data/parameters/eps_inf_external.json`）。

| 材料 | μ | ε (source) | E_b (meV) | 評価 |
|---|---|---|---|---|
| CsPbI₃ | 0.0592 | 6.1（Cho 2019 arXiv:1908.09436 effective; crystal static 6.22） | **22** | **実験 ~15–20 と整合（物理的）** |
| CsPbCl₃ | 0.1155 | 2.4（PMC12757862 LST ε_∞; PMC9071989 ε≈2.51, DFT TB09 **bare** ε_∞） | 273 | 実験 ~64 の **~4× 過大** |
| 他 7 材料 | — | **open web で信頼値得られず**（paywall/相不一致/method 散乱） | — | — |

- **★ 方法論的発見**: 文献が報告するのは **bare 電子 ε_∞**だが、Wannier-Mott が要するのは **effective ε_eff**（ε_∞ と ε_static の中間、フォノン寄与込み）。
  bare ε_∞ を使うと E_b 過大（CsPbCl₃ 2.4→273 meV ≫ 実験 64）。実験 E_b から逆算すると CsPbCl₃ の ε_eff≈5.0（bare 2.4 ではない）。
  CsPbI₃ で 22 meV と合うのは、6.1 が **effective ε**（Cho の励起子遮蔽）だから。
- **結論**: 鉛フリー族の **絶対 E_b は bare ε_∞ からは信頼計算できない**。物理的 ε_eff は CsPbI₃ 型のみ入手可。
  open web に 9 材料の consistent な cubic ε（特に ε_eff）は無い → **Materials Project DFPT（単一手法の ε_∞）か実験 ε_eff が必要**。
- → **Theme I の確定成果は §3.1 有効質量マップ（信頼可）+ E_b 相対トレンド + CsPbI₃ 校正点（22 meV）**。絶対 E_b 9 材料マップは ε_eff データ不足のため未確定（要 PI 判断: MP 利用 or 相対のみで確定）。

## 4. Discussion
- **信頼性の分離**: μ は TB 由来で信頼可（異方性=1、dk 収束）。ε_∞ は外部依存（出典トレーサビリティを MANIFEST に明記）。E_b は両者の積。
- **比較**: CsPbI₃ proxy E_b=22 meV は実験報告（~15–20 meV）と整合。Wannier-Mott は **上限**（ε_∞ のみの遮蔽；
  実際はフォノン寄与で ε_∞<ε_eff<ε_static、E_b はやや小さくなる — Tanaka 2003 / Yang 2017）。
- **限界**: フォノン遮蔽未考慮（上限評価）。Frenkel-Wannier 遷移域材料での妥当性は別途要検討。TB intra-atomic 欠落（Blount）は μ には軽微（曲率は信頼可）、影響は主に ε_∞（→ 外部化で回避）。

## 5. Conclusions（option D' closeout）
- ★ **9 材料の TB 有効質量マップ**（信頼可・publishable, 異方性=1, dk<0.01% 収束）を確定 —
  bundle `theme_I_effective_mass/2026-05-23_1e9c65c`。Sn 系が最軽量（CsSnI₃ μ=0.015）。
- **E_b 相対トレンド**（Cl→Br→I 減, Sn-I 最小）— bundle `theme_I_exciton/2026-05-23_f66690c`（TB-optical ε_∞, 相対のみ）。
- **CsPbI₃ 絶対 E_b 校正点 = 22 meV**（effective ε=6.1, Cho 2019）、実験 ~15–20 meV と整合。
- **絶対 9 材料 E_b マップは未確定**（§3.2）: 文献の bare ε_∞ では E_b 過大、物理的 ε_eff は鉛フリー族で入手不可。
  → 将来 Materials Project DFPT（単一手法）or 実験 ε_eff が得られれば `scan_theme_I_binding_energy.py` で即算出可能。
- **LED 設計示唆**: 大 μ・小 gap（Cl 系, Pb/Ge）ほど E_b 大（励起子発光が明るい傾向）; Sn-I は E_b 最小（自由キャリア寄り）。

## 6. References
- Yang et al. 2017, PRB 96, 035301 — halide perovskite Wannier-Mott
- Tanaka et al. 2003, Solid State Commun. 127, 619 — 励起子結合の実験
- Cho et al. 2019, arXiv:1908.09436 — GW-BSE（ε≈6.1, 質量）
- Kashikar, Gupta, Nanda 2021, arXiv:2101.08562 — TB モデル本体
- ε_∞ 各材料の出典: `data/parameters/eps_inf_external.json`（Cowork 充填後に列挙）

---
（注: 本ファイルは directive 0715 Y1-d の正規報告書。先行の `theme_I_exciton_binding.md`（自走暫定版）は本ファイルに統合・置換。）
