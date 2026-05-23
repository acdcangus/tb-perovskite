# 光学特性（複素誘電関数）の理論定式化メモ（Phase 1.5 / B1, draft v1）

**作成:** 2026-05-23（B1: 文献読み込み）
**ステータス:** ドラフト第一版（Cowork レビュー待ち）
**目的:** 既存 TB エンジン + velocity operator（A2 で実装・検証済み）から、立方晶 CsBX₃ の
複素誘電関数 ε(ω)・吸収係数 α(ω)・屈折率 n(ω) を線形応答（独立粒子近似）で計算する定式化。

---

## 0. 方針

g因子（Theme A）と **同じ velocity operator `dH/dk`（`velocity.py`）を再利用**する。
光学応答は電子-正孔遷移の運動量行列要素（=速度行列要素）で決まるため、A2 のインフラがそのまま使える。
励起子効果（電子-正孔相互作用）は **本フェーズでは含めない**（独立粒子近似）。将来 Wannier-Mott or
簡易 BSE で拡張（Cho 2019 を参考）。

---

## 1. 複素誘電関数（独立粒子近似）

出典: **Apergi 2023 (arXiv:2309.14002) Eq.(3),(4)**。虚部 ε_i を一次摂動の独立粒子表式で計算し、
実部 ε_r は Kramers-Kronig 変換で得る。

### 虚部（Apergi Eq.3 / velocity gauge 標準形）
$$
\varepsilon_i^{aa}(\omega) = \frac{\pi e^2}{\varepsilon_0\, \hbar^2\, \omega^2\, \Omega\, N_k}
  \sum_{\mathbf k}\sum_{v,c} \left|\langle c\mathbf k|\,\partial_{k_a} H_0(\mathbf k)\,|v\mathbf k\rangle\right|^2
  \,\delta\!\big(E_c(\mathbf k) - E_v(\mathbf k) - \hbar\omega\big)
$$
- `a` = デカルト成分（x,y,z）、`v` 占有（価電子）バンド、`c` 非占有（伝導）バンド。
- `Ω` = 単位胞体積、`N_k` = k 点数。スピンは spin-major 基底で和に含まれる（縮退分は自動）。
- δ 関数は **Lorentzian** で平滑化（幅 η = 0.05 eV、Tan & Rappe / Apergi と同程度）。

### 速度（運動量）行列要素（Apergi Eq.4, 電気双極子 ED 項）
$$
\langle c\mathbf k|\,\hat e\cdot \mathbf v\,|v\mathbf k\rangle
  = -\frac{i}{\hbar}\sum_{\alpha\beta} c^*_{c\beta}(\mathbf k)\,
    \big[\hat e\cdot \nabla_{\mathbf k} H_{0,\alpha\beta}(\mathbf k)\big]\, c_{v\alpha}(\mathbf k)
$$
すなわち `v_a = (1/ℏ)∂H/∂k_a`（A2 の `velocity.py`）。位相 −i は |·|² で消える。
（Apergi Eq.4 第二項は電気四重極/磁気双極子 EQMD で **CD 計算用**。誘電関数・吸収には不要なので
Phase 1.5 では第一項=ED のみ。CD は Phase 3 / Theme D で扱う。）

### 単位・前因子（B2 実装時に確定）
`e²/(4πε₀) = 14.39964 eV·Å`、`ℏ²/m₀ = 7.6199 eV·Å²`。`⟨c|∂_a H|v⟩` は eV·Å。
前因子の絶対値は **f-sum rule で校正・検証**する（§3.1）。ε_i は無次元。

## 2. 実部・吸収・屈折率

- **実部（Kramers-Kronig, Apergi 本文）:**
  $$\varepsilon_r(\omega) = 1 + \frac{2}{\pi}\,\mathcal P\!\int_0^\infty
    \frac{\omega' \varepsilon_i(\omega')}{\omega'^2 - \omega^2}\,d\omega'$$
- **屈折率 / 消衰係数:** `n + iκ = sqrt(ε_r + i ε_i)`。
- **吸収係数（Apergi Eq.2）:** `α(ω) = ω ε_i / (n c)` = `2ωκ/c`。

## 3. 検証アンカー（B3 テスト用）

### 3.1 f-sum rule（前因子の校正・必須）
$$\int_0^\infty \omega\,\varepsilon_i(\omega)\,d\omega = \frac{\pi}{2}\,\omega_p^2,
  \qquad \omega_p^2 = \frac{n_e e^2}{\varepsilon_0 m_0}$$
`n_e` = 価電子数密度（占有バンド数 / Ω）。許容 ~1–5%（k グリッド・ω カットオフ依存）。
→ 前因子の絶対正規化はこの sum rule で固定する。

### 3.2 Kramers-Kronig 整合
ε_i から KK 変換した ε_r が、独立に計算した（あるいは KK 逆変換した）ものと整合。自己無撞着チェック。

### 3.3 立方対称
立方相で `ε_xx = ε_yy = ε_zz`（許容 1e-6、対称性チェック）。

### 3.4 論文値との比較
- **Apergi 2023 Fig.1(c):** (R/S−MBA)₂PbI₄ の ε_i 立ち上がり ℏω ≈ 1.6 eV（本文記載）。
  ただし対象は 2D ハイブリッドで本実装（3D 無機立方）と構造が異なるため、定性比較に留める。
- **Cho 2019 (arXiv:1908.09436):** 層状ペロブスカイトの TB(-GW-BSE) ε(ω)。独立粒子部の
  立ち上がり位置を比較（GW/BSE 補正前の bare 部分）。
- **本エンジンのバンドギャップとの整合:** ε_i の吸収端 ≈ 直接ギャップ Eg（R点）になること。
  CsPbI₃ なら Eg ≈ 0.63 eV（mBJ+SOC, Kashikar）/ 1.65 eV（Nestoklon expt）。
  → **吸収端 = ギャップ**は最も確実な内部整合チェック（ハルシネーション防止）。

> 注: 絶対ピーク強度の論文一致は、励起子効果なし・前因子・k グリッドに依存するため、
> **吸収端位置（=ギャップ）と f-sum rule・KK 整合を主検証**とし、絶対強度は二次とする。

## 4. 既存コードとの接続（B2 設計）

```python
def compute_dielectric(hamiltonian_fn, dHdk_fn, k_grid, omega_grid,
                       n_occ, omega=..., smearing_eta=0.05, volume=...):
    # 各 k で eigh(H), dH/dk_a を構築（velocity.py 再利用）
    # eps_i_aa(omega) を Lorentzian 和で計算、KK で eps_r、alpha, n を導出
    return {"omega":..., "eps_real":..., "eps_imag":..., "alpha":..., "n_refractive":...}
```
- velocity operator は `velocity.py`（Kashikar `dH_dk_kashikar13`, Nestoklon `make_dH_dk_nestoklon`）を共有。
- k グリッドは Monkhorst-Pack（収束は論文値再現/f-sum で担保）。
- 占有バンド数 `n_occ` は g因子と同じ（Kashikar13: 20, Nestoklon: 26）。

## 5. 未解決・要判断（progress / Cowork へ）
1. **前因子の絶対正規化**: f-sum rule で校正する方針で良いか（絶対強度の論文一致は二次とする）。
2. **Sipe-Shkrebtii 2000 (PRB 61, 5337)** がリポ未収録 → Cowork が arXiv 版を探索中。
   非線形（Theme F shift current）では必須だが、線形 ε(ω) は Apergi Eq.3/4 で完結。
3. 検証対象: Apergi は 2D ハイブリッド、Cho は層状。**3D 無機立方の独立粒子 ε(ω) の
   直接の論文アンカー**が弱い → 「吸収端=ギャップ」+ f-sum + KK を主検証とする方針で良いか。

## 6. B2/B3 実装結果（2026-05-23 追記）

`src/perovskite_tb/optical.py` 実装、`tests/test_optical.py`（4テスト）通過。CsPbI₃
（Nestoklon expt, `results/optical/CsPbI3_dielectric.png`）で:
- **吸収端 = ギャップ**: ε_2, α はギャップ 1.65 eV 以下でほぼ 0、直上で急峻に立ち上がる。✅
  （`1/E_cv²` を和の内側に置くのが要点。外側 `1/ω²` だと低エネルギーに偽の裾が出る。）
- **立方等方** ε_xx=ε_yy=ε_zz（~1e-9）。✅
- **Kramers-Kronig** ε_r 有限、ε_r(低ω)=ε_∞~1.9。

**f-sum rule の TB 不完全性（重要・正直な記録）:** ∫ω ε_i dω は期待値の **~20% 程度**しか
得られない（ω→40 eV まで取っても ratio~0.21）。これは **velocity operator `∂H/∂k` が
inter-atomic（ホッピング）成分のみで、intra-atomic 電流を欠く**ため（Blount 1962）。
**g因子の atomistic Roth-Lax 過小評価と同じ不完全性**であり、一貫している。
→ **絶対強度・ε_∞ は過小**。検証は **吸収端=ギャップ・立方等方・KK・スペクトル形状（相対）**を主とし、
f-sum と絶対強度は二次（TB 固有の限界として明記）。改竄せず ratio を記録。

## 参考文献（出典）
- S. Apergi, G. Brocks, S. Tao, *Calculating the Circular Dichroism of Chiral Halide
  Perovskites: A Tight-Binding Approach*, arXiv:2309.14002 (2023). — Eq.(2),(3),(4)。
- Y. Cho, T. C. Berkelbach, *...layered hybrid organic–inorganic halide perovskites: A
  tight-binding GW-BSE study*, arXiv:1908.09436 (2019). — TB-GW-BSE 参考。
- J. E. Sipe, A. I. Shkrebtii, *Phys. Rev. B* **61**, 5337 (2000). — 線形・非線形応答の
  k 空間表式（リポ未収録、Cowork 取得中）。
- E. I. Blount, *Solid State Physics* **13**, 305 (1962); E. I. Blount, *Phys. Rev.*
  **126**, 1636 (1962). — 局在基底の position operator の正準分解。TB velocity operator
  `∂H/∂k` が intra-atomic 電流を欠くため f-sum rule を完全には満たさない（§6）原因。
  g因子の atomistic Roth-Lax 過小評価（`g-factor-formulation.md`）と同根の TB 不完全性。
