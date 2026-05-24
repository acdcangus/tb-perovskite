# 数値解法仕様書 (numerical-methods)

理論モデル（[theoretical-model.md](theoretical-model.md)）を数値的に解く手法を定義する。

---

## 1. Slater-Koster 二中心積分

任意方向 `(l,m,n)`（原子1→原子2の方向余弦）に対する行列要素
`⟨α(1)|H|β(2)⟩` を Slater-Koster (1954) Table I の角度公式で計算する
（`src/perovskite_tb/slater_koster.py`）。

- 軌道種別: s型（s, s\*）, p型（pₓ,p_y,p_z）, d型（d_{xy},d_{yz},d_{zx},d_{x²-y²},d_{3z²-r²}）。
- 二中心積分 σ, π, δ は**順序対ごと**に呼び出し側が与える（極性結合に対応）。
- 高角運動量を先に置く場合はパリティ関係
  `E_{βα}(l,m,n) = (-1)^{l_α+l_β} E_{αβ}(l,m,n)`
  で標準順（低角運動量先）に帰着。
- 妥当性確認: 軸方向 `(1,0,0)` の手計算値、および基本関係
  `E_αβ(d) = E_βα(−d)` を全軌道対で検証（`tests/test_slater_koster.py`、106 テスト）。

ペロブスカイトの最近接結合は立方軸方向のみだが、エンジンは一般方向に対応するため
将来の歪み・低対称相にも再利用できる。

## 2. スピン軌道相互作用 (SOC)

オンサイト SOC `H_SO = λ L·S`（`S = σ/2`）を p 軌道に課す
（`src/perovskite_tb/_soc.py`）。`L` は実 p 軌道に作用する軌道角運動量。

- スピン順序は **spin-major**（全軌道スピン↑、続いて↓）。
- **規約（重要）**: 両出典とも λ は「Δ/3」型係数で **p 分裂 = 3λ**。Kashikar Eq.(10) の
  6×6 行列要素は大きさ {±i, ±1} = 2·(L·S) なので `H_SO = λ·(2 L·S)`。
  実装は `soc_p_from_lambda3(λ) = soc_p_matrix(2λ)`。
  固有値 {+λ (×4, j=3/2), −2λ (×2, j=1/2)}、分裂 3λ。
- 検証: 生の `L·S` 固有値 {+λ/2 (×4), −λ (×2)}、Δ/3 規約で分裂 3λ
  （`tests/test_soc.py`, `tests/test_kashikar.py::test_cb_soc_splitting_at_R`）。

## 3. Bloch ハミルトニアンの組み立てと電子占有数

- 原子ゲージ（[theoretical-model.md](theoretical-model.md) §2）で `H(k)` を構築。
  スピンは `H = I₂ ⊗ H₀ + H_{SOC}`（spin-major）。
- 占有スピンバンド数 `n_filled`（バンドギャップ位置の決定に使用）:
  - Kashikar 13軌道（26状態）: **20**（VEC=20）。R点で E1(2)+E2(16)+E4(2)=20、CBM=E3。
  - Kashikar 4軌道（8状態）: **2**（s 由来反結合帯）。
  - Nestoklon sp³(32) / sp³d⁵s\*(80): **26**（I⁻ 5s²5p⁶ ×3 = 24, Pb²⁺ 6s² = 2）。CBM=Pb-p。

## 4. 対角化

- Hermite 行列の固有値は `numpy.linalg.eigvalsh`（LAPACK divide-and-conquer,
  後退安定）で計算。組み立て後に `H ← (H + H†)/2` で数値的 Hermite 性を担保。
- 固有値は昇順ソート。バンド構造は k 経路上の各点で対角化して得る。
- **浮動小数点の等価比較は禁止**。ギャップ・固有値の比較は許容誤差（`np.allclose`,
  `pytest.approx`）で行う（CLAUDE.md 規約）。

## 5. k 経路（高対称点）

単純立方 BZ の高対称点（簡約座標, 単位 `2π/a`）:
`Γ=(0,0,0)`, `X=(½,0,0)`, `M=(½,½,0)`, `R=(½,½,½)`
（`src/perovskite_tb/kpath.py`）。デカルト波数 = 簡約座標 × `2π/a`。
標準経路は `M–R–Γ–X–M–Γ`（Nestoklon Fig.1,2,4 と同じ、`configs/cubic_MRGXM.json`）。
経路は線分ごとに等間隔サンプリングし、累積距離をプロット横軸に用いる。

## 6. バンドギャップの算出

- **直接ギャップ（指定 k 点）**: `E[n_filled] - E[n_filled-1]`。R 点ギャップの検証に使用。
- **基本ギャップ（経路上）**: 占有帯最大 (VBM) と非占有帯最小 (CBM) の差。VBM と CBM が
  同一 k 点なら直接。立方ハライドペロブスカイトでは R 点で直接ギャップとなることを確認。

## 7. 安定性・誤差・計算量

- 本手法は**境界値問題ではなく**有限次元 Hermite 行列の固有値問題であり、CFL のような
  時間積分の安定性条件は無い。誤差要因は (i) 浮動小数点丸め（倍精度、~10⁻¹⁵ 相対）、
  (ii) k 経路の離散化（ギャップ位置の分解能、§5 のサンプル数で制御）。
- 計算量: 1 k 点あたり行列対角化 `O(N³)`（N=8〜80）。k 点数 `N_k` に線形。
  単一材料のバンド構造（数百 k 点）は秒オーダー。メモリ `O(N²)`。
- 解析式（Eq.9）との一致が機械精度であることが、組み立て・対角化経路の正しさを保証する。

## 8. 採用理由と代替

- SK-TB は最近接の少数パラメータで DFT/実験バンドを再現でき、ナノ構造へ拡張しやすい
  （k·p や DFT に対し計算が安価）。Kashikar/Nestoklon が立方ペロブスカイトで実証済み。
- 代替（Wannier 補間, DFTB, k·p）は references に存在するが、初回実装では
  「論文の解析式・数値で厳密検証できる」SK-TB を選定した（ハルシネーション排除のため）。

## 9. Berry 曲率・異常 Hall・スピン Hall (`berry.py`)

仕様 `extention/03_tb-perovskite_spec.md` F1（future_themes Theme H）。既存の velocity operator
`dH/dk`（§velocity, `velocity.py`）の上に Berry 曲率コアを構築する。

### 9.1 Berry 曲率（Kubo 公式）
バンド `n` の Berry 曲率は Kubo 公式で計算する（**Xiao, Chang, Niu, Rev. Mod. Phys. 82, 1959 (2010)
の Eq. (1.13)**, DOI 10.1103/RevModPhys.82.1959）:

$$
\Omega^{n}_{xy}(\mathbf{k}) = i\sum_{m\neq n}
\frac{\langle n|\partial_{k_x}H|m\rangle\langle m|\partial_{k_y}H|n\rangle-(x\leftrightarrow y)}{(E_n-E_m)^2}
= -2\sum_{m\neq n}\frac{\mathrm{Im}\left[V^x_{nm}V^y_{mn}\right]}{(E_n-E_m)^2},
$$

ここで $V^a = U^\dagger (\partial H/\partial k_a) U$（バンド基底の速度行列）。準縮退対（$|E_n-E_m|<$ `degen_tol`）は
和から除外する。占有多重項を完全に含む和は射影子 $P_M$ のみに依存し gauge 不変。

### 9.2 異常 Hall 伝導率 (AHC)
$\sigma_{xy}^{\rm AH}\propto \sum_{\mathbf{k}}\sum_{n\in\text{occ}}\Omega^n_{xy}(\mathbf{k})$。
立方 CsBX₃ は空間反転 $P$ と時間反転 $T$ をともに持つため、占有多重項の和は **各 $\mathbf{k}$ で 0**
（$P$: $\Omega(-\mathbf{k})=\Omega(\mathbf{k})$、$T$: $\Omega(-\mathbf{k})=-\Omega(\mathbf{k})$）→ **AHC = 0**。
本実装はこれを機械精度（~10⁻¹⁵）で再現する（占有は実ギャップ内の Fermi 準位で選び、縮退多重項を割らない）。

### 9.3 スピン Hall 伝導率 (SHC)
スピン流演算子 $j^{s_z}_x=\tfrac12\{s_z,v_x\}$（**Sinova et al., Rev. Mod. Phys. 87, 1213 (2015)**,
DOI 10.1103/RevModPhys.87.1213）で速度頂点を置換し、スピン Berry 曲率を計算する。$P\!\cdot\!T$ では
0 に強制されない（SHC≠0 が許される）。**絶対値は in-repo にベンチマーク材料（Pt 等）が無く未検証**であり、
TB 位置演算子の Blount 限界（intra-atomic 欠落）も効くため、相対傾向・対称性のみを信頼する
（g 因子・shift current の絶対値限界と同じ立場）。

### 9.4 離散 Chern 数（Fukui-Hatsugai-Suzuki 法）
gauge 不変な整数 Chern を、離散 BZ の link 変数で計算する（**Fukui, Hatsugai, Suzuki, J. Phys. Soc.
Jpn. 74, 1674 (2005)**, DOI 10.1143/JPSJ.74.1674; 非アーベル=行列式形）。プラケット場
$F_{12}=\mathrm{Im}\ln[U_1 U_2(k{+}1)U_1(k{+}2)^{-1}U_2^{-1}]$、$C=-\tfrac{1}{2\pi}\sum F_{12}$
（符号は Berry 接続 $A=i\langle u|\partial u\rangle$ 規約で Kubo と整合させた; §V&V で相互検証）。

### 9.5 V&V（`tests/test_berry.py`, 22 ケース）
- **質量 Dirac** $H=k_x\sigma_x+k_y\sigma_y+m\sigma_z$: 下バンド $\Omega_-=+m/[2(k^2+m^2)^{3/2}]$（解析解、当方で Kubo 規約から導出）に一致。
- **Qi-Wu-Zhang Chern 絶縁体**（PRB 74, 085308 (2006)）: Fukui 法が整数 Chern、$|C|=1$ for $|u|<2$、$u=0$ で符号反転、$|u|>2$ で $0$。
- **Kubo ↔ Fukui** 相互一致（QWZ gapped）。
- **立方 CsBX₃**（CsPbI₃/CsSnI₃/CsGeCl₃, SOC on）で **AHC=0** を機械精度で確認（$P\!\cdot\!T$）。
- スピン演算子の su(2) 代数 $[S_x,S_y]=iS_z$、$S_z^2=\tfrac14 I$；スピン流 $j$ のエルミート性。

### 9.6 計算量
1 k 点あたり 26×26 対角化 `O(N³)` + Berry 和 `O(N²)`。9 材料 × BZ メッシュは個人 PC で数分〜1h（GPU 不要）。

