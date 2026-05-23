# 理論モデル仕様書 (theoretical-model)

本書はバンド構造計算の理論モデルを定義する。すべての式・パラメータは出典を持ち、
実装（`src/perovskite_tb/`）と検証（`tests/`）に対応する。物理量と変数名の対応は
[glossary.md](glossary.md) を参照。

---

## 1. 結晶構造

立方晶ペロブスカイト `ABX₃`（空間群 Pm-3m, 格子定数 `a`）。A サイト（Cs⁺ 等）は
電子構造への寄与が小さいため基底から除外する（Boyer-Richard et al. および
Nestoklon に従う）。残る副格子:

- **B サイト（cation, 記号 c）**: 原点 `(0,0,0)`。単純立方格子（B–B 最近接距離 `a`）。
- **X サイト（anion, 記号 a）**: 各立方軸上の `a/2` に1個ずつ、計3個。
  `X₁=(a/2,0,0)`（x軸）, `X₂=(0,a/2,0)`（y軸）, `X₃=(0,0,a/2)`（z軸）。

B は6個の X に八面体配位され、B–X 結合は立方軸方向（長さ `a/2`）。

```
   z                X3
   |                |
   |        X1------B------(X1 of +x cell)
   |                |
   +----- x        X2          （B を中心とする BX6 八面体）
```

単位胞の原子: 1×B + 3×X = 4 原子。各原子に軌道基底を載せる。

---

## 2. タイトバインディング・ハミルトニアン（一般形）

第二量子化で
$$
H = \sum_{i,\alpha} \epsilon_{i\alpha}\, c^\dagger_{i\alpha} c_{i\alpha}
  + \sum_{\langle ij\rangle,\alpha\beta} t_{i\alpha,j\beta}\, c^\dagger_{i\alpha} c_{j\beta}
  + \lambda\, \mathbf{L}\cdot\mathbf{S},
$$
ここで `i,j` は原子サイト、`α,β` は軌道、`ε` はオンサイトエネルギー、`t` はホッピング、
第3項はスピン軌道相互作用 (SOC)。（Kashikar Eq.(1)。）

ホッピング `t_{iα,jβ}` は Slater-Koster の二中心近似で、結合方向の方向余弦 `(l,m,n)` と
二中心積分（σ, π, δ）で表される（[numerical-methods.md](numerical-methods.md) §1, Slater-Koster 1954）。

Bloch ハミルトニアン（**原子ゲージ**）:
$$
H_{\alpha\beta}(\mathbf{k}) = \sum_{\mathbf{R}} t_{\alpha\beta}(\mathbf{R})\,
  e^{i\mathbf{k}\cdot(\mathbf{R}+\boldsymbol{\tau}_\beta-\boldsymbol{\tau}_\alpha)},
$$
固有値はゲージ不変。B を原点に置くと Kashikar の簡約因子
`S_d = 2i\sin(k_d a/2)`, `C_d = 2\cos(k_d a/2)` を厳密に再現する。

---

## 3. モデル I: Kashikar 13軌道 SK-TB（CsBX₃ 全9種）

出典: **arXiv:2101.08562**, Eqs.(3)–(8)、パラメータ Table II。

### 基底（13軌道）
`{ B-s, B-pₓ, B-p_y, B-p_z, X₁-{pₓ,p_y,p_z}, X₂-{…}, X₃-{…} }`。

### 相互作用
- **B–X 最近接**（距離 `a/2`）: s-pσ, p-pσ, p-pπ。
  軸 `d` 上のハライドについて
  `⟨B-s|H|X_d-p_d⟩ = t^{BX}_{sp}\,S_d`,
  `⟨B-p_i|H|X_d-p_i⟩ = (t^{BX}_{pp\sigma}\text{ if }i{=}d\text{ else }t^{BX}_{pp\pi})\,C_d`。
- **B–B 第二近接**（距離 `a`, 単純立方）: s-s, s-pσ, p-pσ, p-pπ。分散関数（Eq.8）
  $$h_1 = 2t^{BB}_{ss}\sum_d\cos(k_d a),\quad
    h_{2,3,4} = 2t^{BB}_{pp\sigma}\cos(k_{d} a) + 2t^{BB}_{pp\pi}\sum_{e\neq d}\cos(k_e a),$$
  s–p 結合は `2i\,t^{BB}_{sp\sigma}\sin(k_d a)`（full-`a` 位相、R点で消える）。
- **X–X**: 無視（X-p ブロックはオンサイト対角 `ε^X_p`、Eq.7）。

### R点固有値（解析式, Eq.9）— 実装検証の要
`R = (π/a,π/a,π/a)` で（SOC なし）
$$
E_{1}=\tfrac{E^X_p+E^B_s}{2}-3t^{BB}_{ss}-\eta,\quad
E_{2}=E^X_p\ (\times 8),\quad
E_{3}=E^B_p-2t^{BB}_{pp\sigma}-4t^{BB}_{pp\pi}\ (\times 3),
$$
$$
E_{4}=\tfrac{E^X_p+E^B_s}{2}-3t^{BB}_{ss}+\eta,\qquad
\eta=\tfrac12\sqrt{(E^X_p-E^B_s+6t^{BB}_{ss})^2+48\,(t^{BX}_{sp})^2}.
$$
VBM は `E₄`（反結合 s–X）、CBM は `E₃`（B-p 三重項）。本実装は数値対角化が
この式と機械精度（~10⁻¹⁵ eV）で一致することを全9材料で確認している
（`tests/test_kashikar.py::test_eq9_R_point`）。

### 4軌道最小モデル
B-{s,p} のみ（X-p を実効 B–B に繰り込む）。SOC なしギャップ閉形式
`E_g = ε_p - ε_s - 2t_{pp\sigma} - 4t_{pp\pi} + 6t_{ss}`（Kashikar §III.C, Table IV）。

---

## 4. モデル II: Nestoklon Jancu sp³d⁵s\* ETB（CsPbI₃）

出典: **arXiv:2012.14705**, Table I。手法は Jancu et al. (PRB 57, 6493) の
sp³d⁵s\* 最近接 SK スキーム。

### 基底（10軌道/原子）
`{s, pₓ, p_y, p_z, d_{xy}, d_{yz}, d_{zx}, d_{x²-y²}, d_{3z²-r²}, s*}`。
cation=Pb, anion=I の2種。単位胞 4 原子 × 10 軌道 × 2 スピン = **80 状態**。
（sp³ 簡約モデルは最初の4軌道、32 状態。）

### 相互作用
最近接 cation–anion のみ（B–B, X–X なし）。二中心積分は極性結合のため
**順序対（cation軌道 → anion軌道）ごとに異なる積分**を用いる（Table I の命名規約、
[glossary.md](glossary.md) §SK積分）。Table I キャプションで零に固定される積分:
`s*s*σ = sₐ*… = pᵤ d_a … = 0`（実装では該当キー欠落時に 0）。

### スピン軌道相互作用
オンサイト `λ\mathbf{L}\cdot\mathbf{S}` を **両副格子の p 軌道**に課す。
パラメータは `Δ_a/3`（I）と `Δ_c/3`（Pb）。Chadi/Jancu 規約で **p 分裂 = 3λ = Δ**
（[numerical-methods.md](numerical-methods.md) §2）。

### 3つのパラメータセット
- `sp3`: DFT バンド構造への最小フィット。
- `sp3d5sstar`: DFT バンド構造への完全フィット（R点ギャップ 1.017 eV を meV 精度で再現）。
- `experiment_corrected`: 実験ギャップ（R 1.65 eV, M 2.75 eV）を再現するよう改訂。

---

## 5. 物理的特徴（両モデルで再現される）

- **直接ギャップが R 点**に現れる（立方ハライドペロブスカイトの特徴）。
- 価電子帯頂上 (VBM) は反結合的な `B-s`–`X-p` 状態、伝導帯底 (CBM) は `B-p`。
- 伝導帯は強い SOC で分裂（Pb で ~1.5 eV）。
- 価電子数 VEC = 20/式単位（Kashikar §II）。占有数は
  [numerical-methods.md](numerical-methods.md) §3 参照。

## 6. 仮定・近似と適用限界

- 立方（高対称）相のみ。八面体回転（低対称相）は未対応。
- A サイトを除外（バンド端近傍の電子構造に主寄与しないという近似）。
- Nestoklon は最近接のみ（一部の平坦価電子帯は厳密には再現できないと原論文が明記）。
- SOC はオンサイト p 軌道のみ（d-SOC は無視、原論文も p のみパラメータ化）。
- 単位系: エネルギー eV、長さ Å。バンドエネルギーは格子定数の数値に依存しない
  （高対称点・経路を `π/a` 単位で評価するため）。
