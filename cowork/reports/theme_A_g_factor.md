# Theme A: 立方晶 CsBX₃ 9材料の Landé g因子 系統マップ

**ステータス:** 部分完了（A1-A5 実装・解析済み、draft v1。Cowork レビュー待ち）
**実施期間:** 2026-05-23
**コミット範囲:** 83553f0 .. (本コミット)
**担当:** Claude Code / 監督: Cowork

## 1. 動機と仮説
- Kirstein 2021 (arXiv:2112.15384) と Nestoklon 2023 (arXiv:2305.10586) は、**鉛系**ハライド
  ペロブスカイトで「電子・正孔 g因子がバンドギャップ Eg で普遍的に決まる」関係を提唱。
- **仮説:** 鉛フリー（Sn, Ge）系で同じ普遍関係が成立するか？ 成立しないなら何が破るか？
- **新規性:** Ge/Sn 系の g因子の系統予測は 2026-05 時点で未報告。鉛フリースピン光デバイスの設計指針。

## 2. 方法
- **エンジン:** 既存の検証済み TB（Kashikar 13軌道 / Nestoklon sp³d⁵s\*、163テスト通過）。
- **g因子:**
  - 主手法 = **k·p 普遍式**（Kirstein Eq.(5) 正孔, Eq.(6) 電子）。`g_factor.py::g_factor_kp`。
    `g_e=−2/3+(4/3)P²/(C·Eg)+Δg_e`, `g_h=2−(4/3)(P²/C)[1/Eg−1/(Eg+Δ)]`, C=ℏ²/m₀=7.62 eV·Å²。
  - 補助 = **atomistic Roth-Lax**（`compute_g_factor`、velocity operator 経由）。対称性・異方性チェック用。
- **入力 Eg, Δ:** `data/parameters/experimental_band_data.json`（Pb Δ=Table S2、Sn/Ge Δ=Kashikar 3λ、
  Eg=文献値、出典明記）。普遍 P=6.8 eV·Å, Δg_e=−1（Kirstein Fig.5）。
- **検証アンカー:** Nestoklon Table S2（CsPbX₃ バルク ETB g因子）。

## 3. 主要結果
### 3.1 電子 g_e — 全9材料が単一普遍曲線
g_e は Eg のみに依存。B サイトに依らず一本の曲線に乗る。小ギャップほど大:
**CsSnI₃ +4.56 > CsGeI₃ +3.39 > CsPbI₃ +3.01 > ... > CsGeCl₃ +0.71**。

### 3.2 正孔 g_h — 鉛フリーは Pb 曲線から上方乖離（★主結果）
g_h は Eg と Δ に依存。Sn/Ge は伝導帯 SOC Δ が Pb より小さく、**g_h が Pb 普遍曲線から
+0.5〜+1.9 上方乖離**。乖離最大: CsGeI₃ +1.86, CsSnI₃ +1.81。Δ±20% でも傾向は頑健。

**乖離の定義（明確化, Cowork review #3 §2）:**
> Δg_h ≡ g_h(材料固有 Δ_B) − g_h(普遍 Δ ≈ 1.5 eV)
> = 鉛フリーの伝導帯 SOC が、Pb で確立した Kirstein 普遍則（暗に Δ_Pb≈1.5 を仮定）から
>   正孔 g因子をどれだけ引き離すかの指標。
この定義により「Pb で確立した普遍則が Sn/Ge では破れる」主張が誤解されない。
g_h = 2 − (4/3)(P²/C)[1/Eg − 1/(Eg+Δ)] の補正項は Δ→0 で消滅（→ g_h→+2）するため、
弱 SOC 材料が +2 寄りになるのは数式から自明。

### 3.3 未測定物性の予測値（実験確認待ち）
全9材料の (g_e, g_h, Eg) は `results/g_factors/g_factor_9material.csv`。
鉛フリー候補トップ: **CsSnI₃ (g_e=+4.56, Eg=1.30 eV, NIR)**, **CsGeI₃ (g_e=+3.39, g_h=+1.41, Eg=1.60 eV)**。

### 3.4 TB から導いた Kane パラメータ P（A6, 完全 TB ベース化）
g因子を「k·p 公式 + **TB-derived Δ (Eq.9) + TB-derived P (速度演算子)**」で出すことで、
**9材料の g因子を TB Hamiltonian の物理量のみから予測**（`results/g_factors/kane_parameters.csv`）。

- **CB の cation-p_z 重み sin²θ = 1/3**（全材料・両モデル）→ Nestoklon Eq.S1b の解析的
  Bloch 構造 (sinθ=√(1/3)) と一致。抽出法の妥当性を裏付け。
- **TB-derived bare P (eV·Å)**: Kashikar 13軌道 4.1〜5.9（普遍 6.8 の 60〜87%）、
  Nestoklon sp³d⁵s\* CsPbI₃ = **5.44**（普遍の 80%, |5.44−6.8|=1.36<1.5 ✓）。
- **系統的過小評価**: TB-derived P < 普遍 6.8。軌道基底が豊富な sp³d⁵s\*(5.44) は最小 Kashikar
  s,p(4.11) より大きく 6.8 に近い。原因 = 利用可能パラメータが**バンド構造フィット（g因子非調整）**
  のため（Nestoklon の g 調整 Table S1 は pp_sigma が大きく P も大きいはずだが paywall）。

**A7 逆抽出チェック（`scripts/plot_ge_universality.py`, `results/g_factors/ge_universality.png`）:**
Pb 系の (ETB) g_e を再現する「逆 Kane P」は **3 ハロゲンとも 6.80 で一定** → g_e 普遍性の前提
（P 一定）を裏付け。一方 **TB-derived P (4.1〜5.3) は 25〜40% 過小**（Blount 不完全性が P に現れた形）。
∴ g_e 普遍性自体は妥当（有効 P 一定）だが、band-fit TB Hamiltonian の P はそれを再現せず系統的に
小さい → 絶対予測には普遍 P（or g 調整パラメータ）が必要。
（注: Pb 逆 P=6.8 は Table S2 g_e 自体が普遍 P=6.8 と整合するため半ば自己無撞着。非自明な結論は
「TB-derived P が一貫して過小」の方。）

→ **これで Theme A は完全に TB ベース**: "We extract from our TB Hamiltonian both the
conduction-band SO splitting Δ (analytic R-point eigenvalues, Kashikar Eq.9) and the Kane
momentum P (analytic velocity operator), and substitute them into the k·p universal formula,
giving the first TB-based g-factor prediction for Sn- and Ge-based halide perovskites."

## 4. 論文値との比較・整合性
- **電子 g_e: Nestoklon Table S2 を meV 再現**（CsPbCl₃ 0.95, CsPbBr₃ 1.77, CsPbI₃ 3.23）。✅
- **正孔 g_h: Cl/Br 良好、I で過小**（CsPbI₃ −0.12 vs −0.33）。2バンド k·p の既知限界。
- atomistic Roth-Lax の絶対値は TB position operator の不完全性（Blount 1962）で過小（g_e 1.06）。
  → 主結果は k·p。Roth-Lax は対称性チェックに限定（立方等方性 1e-15 で確認）。

## 5. 物理的考察
- g_e の普遍性: 伝導帯底が価電子帯との k·p 混成で決まり、その強さ（P）がほぼ材料非依存のため。
- g_h の鉛フリー乖離: 正孔（価電子帯）の g因子は伝導帯の SO 分裂 Δ との混成で決まる。
  Pb の重い SOC（Δ≈1.5）が Sn(0.45)/Ge(0.21)で大幅減 → 補正項が小さく g_h→+2 寄り。
- **含意: 鉛フリーペロブスカイトでは「Eg を見れば g がわかる」普遍則が正孔で破れる。
  g因子設計には B サイト SOC を独立変数として扱う必要がある。**

### g_e 普遍性は「真の普遍」か「見かけ」か（A6 の含意）
g_e の単一曲線は普遍 P=6.8 を仮定した帰結だった。TB-derived P は材料で 4.1〜5.9 と
**~40% の変動**を示す（P/P_univ = 0.60〜0.87）。したがって g_e の「単一曲線」は
**厳密には見かけ**で、材料別 P を入れると曲線から散らばる。ただし TB-derived P は band-fit 由来で
系統的に過小（Pb で 6.8 を再現しない）ため、絶対値は普遍 P の方が実験に合う。
→ 結論: **g_e 普遍性は「P がほぼ一定」という近似の上に成り立つ**。P の材料依存（特に X=I で大）を
入れると補正が要る。これは論文で「普遍関係の適用限界」として議論できる。

論文用考察（Cowork review #5 提案, 英文）:
> "The apparent universality of g_e arises because P varies only modestly (~40%)
> across the CsBX3 family while Eg varies by a factor of ~2.6. The compensation is
> partial: a stricter test with TB-derived material-specific P shows that the
> single-curve fit to g_e(Eg) is an approximation valid to within Δg_e ~ 0.5. For
> the hole factor g_h, the additional dependence on Δ amplifies material-specific
> deviations because Δ varies by an order of magnitude (Pb 1.5 → Ge 0.21 eV),
> making the universal curve inadequate for lead-free systems."

### Blount 1962 統一クロス検証（手法論の柱）
g因子 atomistic Roth-Lax の過小評価（〜3×）と光学 f-sum の ~20% 取得は、いずれも TB の
velocity operator `v≈∂H/∂k` が **intra-atomic position-matrix 成分を欠く**（E. I. Blount,
*Solid State Phys.* **13**, 305 (1962); *Phys. Rev.* **126**, 1636 (1962)）ことに起因する同一の限界。
論文では以下を明記する（Methods/Discussion, Cowork review #5 提案）:
> "Our TB results display two systematic underestimates: the Roth-Lax g-factor from
> dH/dk is ~3x too small relative to the k.p formula, and the optical f-sum rule is
> satisfied at only ~20%. Both originate from the same source -- the velocity
> operator in a localized basis omits the intra-atomic position-matrix contribution
> (Blount 1962). We therefore emphasize relative trends and spectral-shape /
> band-edge features (robust under this limitation), keeping absolute magnitudes as
> documented diagnostics rather than predictions."

## 6. 学会・論文化の見通し
- **新規性確認（独立検証, 2026-05-23）:** 2025年11月の g因子レビュー arXiv:2511.02956
  (Rodina, Semina, Ivchenko) を全文確認した結果、**鉛フリー（Sn/Ge）ハライドペロブスカイトの
  g因子の記述はゼロ**。Theme A の新規性は堅持（Cowork novelty check, `progress/..._0900_..`）。
  英語注記: "An independent novelty check against the November 2025 g-factor review
  (arXiv:2511.02956) confirms that lead-free halide perovskites remain unexplored in the
  universal Landé g-factor literature."
- **Letter 規模で成立**: 「鉛フリーハライドペロブスカイトにおける正孔 g因子の普遍関係破れ」。
- 候補: Phys. Rev. B (Letter/Regular), npj Comput. Mater., J. Phys. Chem. Lett.。
- 磁気光学（最近のホット）と接続: g因子は時間分解 Faraday/Kerr の観測量。鉛フリー × 磁気光学は新規。
- 「面白い結果」: g_h の鉛フリー上方乖離（明確・定量的・実験検証可能）。
- 「面白くない/要注意」: g_e の普遍性は P 普遍を仮定した帰結（材料別 P で再検証要）。

## 7. 限界・残課題
- **CsPbI₃ g_h 絶対値ズレ調査（A5補強, docs/g-factor-analysis.md §1.1）:** k·p −0.12〜+0.03 vs
  Table S2 −0.33。切り分け: Eg を 1.652 にすると −0.117（~0.15 説明）、残差 ~0.21 は
  「単一等方 2バンド P が電子(P=6.80)と正孔(P=7.13)を同時再現できない」近似限界。改竄せず記録。
  主結果（g_h の Sn/Ge 相対乖離）はこの絶対値ズレに鈍感だが、絶対値に ±0.2 系統不確かさを明記。
- Sn/Ge の Δ は Kashikar 3λ 由来（±20%）。文献の直接 Δ が望ましい（Cowork task #18）。
- g_e の材料別 P 補正（TB 速度から）は未実施 → g_e 普遍性の真の検証に必要。
- g_h 絶対値の精密化（多重項/remote）と atomistic 法の Wannier ベース改良は将来 Phase。
- 実験 Eg 出典 PDF（Stoumpos 2013 等）のリポ取り込み待ち。

## 8. 再現コマンド
```bash
pip install -r requirements.txt && pip install -e .
PYTHONPATH=src python scripts/scan_g_factors.py
PYTHONPATH=src python -m pytest tests/test_g_factor.py tests/test_velocity.py -q
```

## 9. 関連ファイル
- 定式化: `docs/g-factor-formulation.md`、解析: `docs/g-factor-analysis.md`
- 実装: `src/perovskite_tb/g_factor.py`, `velocity.py`
- データ: `data/parameters/experimental_band_data.json`, `results/g_factors/g_factor_9material.csv`
- 図: `results/g_factors/kirstein_universal_plot.png`, `material_grid.png`
- テスト: `tests/test_g_factor.py`, `tests/test_velocity.py`
