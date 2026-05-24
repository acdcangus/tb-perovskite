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

## 10. Wilson ループ・Wannier 電荷中心 (`topology.py`, 仕様 F2 部分)

`berry.py` の link 変数を再利用し、占有多様体の**非アーベル Wilson ループ**（閉ループ上の重なり行列の積）と、
その固有位相＝**Wannier 電荷中心 (WCC)**、WCC/分極の巻き付き数＝Chern 数を計算する
（**Yu, Qi, Bernevig, Fang, Dai, PRB 84, 075119 (2011)**, DOI 10.1103/PhysRevB.84.075119;
**Soluyanov, Vanderbilt, PRB 83, 235401 (2011)**, DOI 10.1103/PhysRevB.83.235401）。
各 link は SVD 極分解で unitary 化（有限 N でも厳密 unitary, det 位相＝分極は不変）。

### V&V（`tests/test_topology.py`, 12 ケース）
- QWZ 模型で **Wilson ループ Chern == Fukui plaquette Chern**（2 独立手法の相互一致, 整数）。
- QWZ 相図（|C|=1 for |u|<2, u=0 符号反転, |u|>2 で 0）。
- Wilson ループの unitary 性・分極位相の U(1) gauge 不変性・WCC ∈ (−½,½]。

### スコープ外（ハルシネーション防止のため意図的に未実装）
- **Fu-Kane parity Z₂**: Kashikar 軌道基底での**空間反転演算子の表現**が in-repo 情報から確定できない（推測は捏造リスク）→ 反転表現を一次文献で確定するまで保留。
- **Soluyanov-Vanderbilt 時間反転 Z₂（partner switching）**: 手法は実装可能だが、**検証用の既知 3D-Z₂ 参照模型**が必要 → 保留。
- → 立方 CsBX₃ の topological 分類（CsPbI₃ の inverted gap 等, Jin 2012）は上記確定後の follow-up。本コミットは**検証済みの Wilson ループ基盤**まで。

## 11. Boltzmann 熱電輸送 (`thermo.py`, 仕様 F9)

定緩和時間近似 (CRTA) の半古典 Boltzmann 輸送を、既存バンド + 群速度（velocity.py）から計算する
（**Madsen, Singh, Comp. Phys. Commun. 175, 67 (2006)**, DOI 10.1016/j.cpc.2006.03.007, BoltzTraP 形式）。
輸送分布関数 $\Sigma_{xx}(\varepsilon)=\frac1{N_k}\sum_{n,k}v_x^2\,\delta(\varepsilon-E_{nk})$、
モーメント $L^{(a)}=\int d\varepsilon\,(-\partial f/\partial\varepsilon)(\varepsilon-\mu)^a\Sigma$ から

$$\sigma_{xx}/\tau=e^2 L^{(0)},\quad S_{xx}=-\frac{1}{eT}\frac{L^{(1)}}{L^{(0)}},\quad
\kappa^e_{xx}/\tau=\frac1T\Big[L^{(2)}-\frac{(L^{(1)})^2}{L^{(0)}}\Big].$$

単位: エネルギー eV, 温度 K, $k_B$ eV/K。Seebeck は $k_B/e$ 単位（86.17 μV/K）、Lorenz 数は $(k_B/e)^2$ 単位で返す。
**絶対値は緩和時間 $\tau$（材料・散乱依存）が必要でスコープ外** → 相対値（/τ）のみ（既存 SHC/shift current の絶対値限界と同じ立場, honest）。

### V&V（`tests/test_thermo.py`, 6 ケース）
- **Wiedemann-Franz 則**: 縮退極限で Lorenz 数 → $\pi^2/3\,(k_B/e)^2$（解析 $\Sigma=\varepsilon^{3/2}$ で rtol 0.5%; バンド詳細に依らない厳密 anchor）。
- **Sommerfeld Seebeck**: $S\sim-(\pi^2/3)(k_BT)\,d\ln\Sigma/d\varepsilon|_\mu$、3D 放物バンドで符号・大きさ一致。
- 正孔バンドで $S>0$（符号）、$\sigma,\kappa^e>0$、$\Sigma$ ビルダの $\varepsilon^{3/2}$ 形状、立方 CsPbI₃ で実行整合。

## 12. Rashba / 中心反転破れスピン分裂 (`rashba.py`, 仕様 F4)

中心反転が破れた系のスピンテクスチャ $\langle S\rangle(\mathbf{k})$ と線形 $k$ スピン分裂係数 $\alpha_R$ を計算する
（**Bychkov, Rashba, JETP Lett. 39, 78 (1984)**: $H_R=\alpha_R(\boldsymbol\sigma\times\mathbf{k})\cdot\hat z$,
バンド端 doublet は $\Delta E=2\alpha_R|k|$ で分裂しスピンは $k$ に直交; **Niesner et al., PRL 117, 126401 (2016)**,
DOI 10.1103/PhysRevLett.117.126401, ペロブスカイト Rashba）。`berry.spin_operators` と
`shift_current.make_polar_kashikar13_builders`（spinful P4mm）を再利用。

立方 Pm-3m CsBX₃ は中心反転 P + 時間反転 T → 全 k で Kramers 縮退 → $\alpha_R=0$。[001] 極性変位 (P4mm) で P が破れ、
$|k|>0$ で分裂（TRIM $k=0$ は Kramers 定理で保護され分裂ゼロ）。

### V&V（`tests/test_rashba.py`, 8 ケース）
- **解析 2 バンド Rashba** で入力 $\alpha_R$ を厳密回復、スピンは $k$ に直交（spin-momentum locking）。
- **立方 CsBX₃ → 分裂 0**（Kramers, 複数 doublet で <1e-6）。
- **極性 CsBX₃ → 分裂あり**（>1e-4）、$\Gamma$ でゼロ、$|k|$ とともに増大（k 線形）。

### honest 限界
$\alpha_R$ の絶対値は整合するベンチ（文献は**表面** Rashba、本実装は**バルク極性**変形）が無く + Blount 限界 → 対称性（0 vs ≠0）・spin-momentum locking・相対トレンドのみ信頼、絶対値は indicative。

## 13. Edelstein 効果（電流誘起スピン分極） (`edelstein.py`, 仕様 F11)

定緩和時間近似 (CRTA) の線形応答で、電流（電場）が誘起するスピン分極 $\delta S_a=\chi_{ab}E_b$ を計算する
（**Edelstein, Solid State Commun. 73, 233 (1990)**, DOI 10.1016/0038-1098(90)90963-C）。
$\chi_{ab}/(e\tau)=-\frac1{N_k}\sum_{n,k}(-\partial f/\partial E)\langle S_a\rangle\,v_b$（Fermi 面平均）。
`thermo` の Fermi 窓・`berry` のスピン演算子・`rashba` のスピンテクスチャを再利用。

中心反転系では $\langle S\rangle(-k)=\langle S\rangle(k)$（偶）・$v(-k)=-v(k)$（奇）→ 積分が奇 → $\chi=0$。
Rashba 系では電流に**直交**するスピン応答（$\chi_{yx}\neq0,\chi_{xx}=0$, Rashba-Edelstein）。

### V&V（`tests/test_edelstein.py`, 4 ケース）
- **中心反転（非縮退）模型 d(k)=(cos kx,cos ky,M)** → $\chi=0$（機械精度）。
- **Rashba 模型** → $\chi_{yx}\neq0$, $|\chi_{xx}|\ll|\chi_{yx}|$（直交）、$\chi_{yx}(-\alpha)=-\chi_{yx}(\alpha)$（符号反転）。
- 極性 CsPbI₃（P4mm, 非縮退）で実行整合。

### 適用範囲・限界（honest）
per-band 公式は**非縮退バンド**前提。立方 Pm-3m は全 k で Kramers 縮退（応答は対称性で 0 だが per-band では gauge 依存）→
ペロブスカイトは**反転破れ極性 (P4mm)** 相で評価。絶対値は $\tau$ 依存でスコープ外（/eτ で返す）→ 対称性・直交構造・相対のみ信頼。

## 14. 円偏光光起電力効果 (CPGE) / injection current (`cpge.py`, 仕様 F7)

円偏光下の 2 次注入電流テンソル $\beta_{ij}$（$dJ_i/dt=\beta_{ij}(\mathbf{E}\times\mathbf{E}^*)_j$）を計算する
（**Sipe, Shkrebtii, PRB 61, 5337 (2000)**, DOI 10.1103/PhysRevB.61.5337; **de Juan, Grushin, Morimoto, Moore,
Nat. Commun. 8, 15995 (2017)**, DOI 10.1038/ncomms15995, arXiv:1611.05887。式は ar5iv 原典で確認）:

$$\beta_{ij}(\omega)=\frac{\pi e^3}{\hbar V}\epsilon_{jkl}\sum_{\mathbf{k},n,m}f_{nm}\,\Delta^i_{nm}\,r^k_{nm}r^l_{mn}\,
\delta(\hbar\omega-E_{mn}),\qquad r^a_{nm}=-i\,v^a_{nm}/E_{nm}.$$

2 バンドでは $\beta_{ij}=\frac{i\pi e^3}{\hbar^2 V}\sum_k(\partial_{k_i}E_{12})\,\Omega^j_1\,\delta(\hbar\omega-E_{21})$
（速度差 × 下バンド Berry 曲率ベクトル）に簡約され、`berry.berry_curvature_kubo` を再利用。
de Juan の**位相幾何学的量子化**: Weyl 点（Chern 数 $C$）で $\mathrm{Tr}[\beta]=i\pi(e^3/h^2)C$（共鳴窓で $\omega$ 非依存のプラトー）。

### V&V（`tests/test_cpge.py`, 4 ケース）
- **式の簡約（de Juan）**: $-\mathrm{Im}(\epsilon_{jkl}r^k_{12}r^l_{21})=\Omega^j_1$（一般式 ⇔ 2 バンド Berry 曲率形が一致）。
- **中心反転（偶 d, 非縮退）→ $\beta=0$**。
- **Weyl 量子化**: $\mathrm{Tr}[\beta]$ が $\omega$ 非依存プラトー、chirality で符号反転、$|\mathrm{Tr}|\approx\pi e^3/h^2=1/(4\pi)$（$e{=}\hbar{=}1$）を ~20% で数値再現。

### honest 限界
符号は de Juan と Xiao（berry.py）の Berry 曲率規約差を 2 バンド検証で整合させた。立方ペロブスカイトの $\beta=0$ は
（Kramers 縮退の per-band gauge 問題回避のため）非縮退中心反転模型で検証、材料適用は極性相で。絶対値は Blount 限界 + 規約依存。

## 15. Fröhlich ポーラロン結合 (`polaron.py`, 仕様 F6)

無次元 Fröhlich 結合定数 $\alpha$ と弱結合ポーラロン質量を、誘電率・LO フォノン・有効質量から計算する
（**Fröhlich, Adv. Phys. 3, 325 (1954)**; **Feynman 1955/1962**; **Frost, PRB 96, 195202 (2017)**,
DOI 10.1103/PhysRevB.96.195202, arXiv:1704.05404; 式は ar5iv 原典で確認）:

$$\alpha=\frac{1}{4\pi\epsilon_0}\,\frac12\Big(\frac1{\epsilon_\infty}-\frac1{\epsilon_{\rm S}}\Big)\,
\frac{e^2}{\hbar\Omega}\sqrt{\frac{2m_b\Omega}{\hbar}},\qquad m_p/m_b\simeq 1+\alpha/6\ (\text{弱結合}).$$

物性値は OA 一次文献から収集（`data/parameters/frohlich_polaron_params.json`, 各値に出典明記）。

### V&V（`tests/test_polaron.py`, 7 ケース）— **2 つの独立ベンチマークで前因子を固定**
- **MAPbI₃**（Frost 2017）: ε∞=4.5, ε_S=24.1, ν_LO=2.25 THz, m*=0.12/0.15 → **α=2.39 (e), 2.68 (h)** を <1% で再現。
- **CsPbBr₃**（Sendner et al., Nat. Commun. 12, 4945 (2021), PMC8494801）: ε∞=4.8, ε_S=20.5, ω_LO=19.2 meV, m*=0.22 → **α≈2** を再現（第 2 の独立検証）。
- 単位変換（THz⇔meV）、スケーリング（√m*、(1/ε∞−1/ε_S)）、弱結合質量極限。

### スコープ・限界（honest）
$\alpha$ と**先頭次**弱結合質量 $1+\alpha/6$ のみ実装・検証（intermediate 結合 α~2 では完全 Feynman variational が必要 → 移動度は未実装, cf. PolaronMobility.jl）。
9 材料 α マップは各材料の **cited な $\epsilon_{\rm S}$・$\omega_{\rm LO}$** が必要 → CsPbBr₃ は収集済（上記）、他材料は一次出典が揃い次第追加（`_pending` 参照）。捏造防止のため未収集材料は計算しない。

