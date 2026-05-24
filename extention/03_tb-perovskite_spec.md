# tb-perovskite — 追加機能仕様書

**対象リポジトリ**: `C:\Users\kteru\tb-perovskite`
**現在の状況**: 立方相 CsBX₃ (B=Ge/Sn/Pb, X=Cl/Br/I) Slater-Koster TB と Jancu sp³d⁵s* TB を実装。velocity operator、g-factor、shift current、光学応答（ε(ω)）を実装済み。future_themes.md で Theme G–L 候補確認済み。
**ベース論文**: Kashikar arXiv:2101.08562 (2021), Nestoklon arXiv:2012.14705 (2021), Slater-Koster PR 94, 1498 (1954), Jancu PRB 57, 6493 (1998)
**作成日**: 2026-05-24
**改訂**: r3

---

## 1. 既存機能サマリ

実装済み：
- 立方相 CsBX₃ の SK TB（13軌道, 4軌道など）
- 立方相 CsPbI₃ Jancu sp³d⁵s* ETB
- スピン軌道相互作用 (オンサイト L·S)
- バンド構造、k 経路、高対称点
- velocity operator（既存 `velocity.py`）
- g-factor 計算（既存 `g_factor.py`, Theme A）
- shift current 計算（既存 `shift_current.py`, Theme F）
- 光学応答 ε(ω)（既存 `optical.py`, Phase 1.5）
- 励起子（Wannier-Mott, `exciton.py`, Theme I 簡易版）

未実装（future_themes に予定はあるが未着手）：
- Berry curvature, AHC, SHC (Theme H)
- CPGE（Theme J 円偏光光学電流）
- 2D Ruddlesden-Popper の層数依存（Theme K）
- Fröhlich polaron 移動度（Theme L）

未予定（本仕様で新規提案）：
- **トポロジカル不変量（Z₂, Chern, ℤ₂ 鏡映, fragile topology）**
- **熱輸送・熱電（Boltzmann + Wannier）**
- ~~動的無秩序 / 有限温度効果（MD–TB 結合）~~ — **HPC 必須のため本仕様から除外（F10 削除）**
- **Rashba/Dresselhaus 解析（中心反転破れ）**
- **非線形光学（SHG, THG, BPVE 拡張）**
- **電荷-スピン変換（Edelstein 効果, IEE）**
- **層・歪み・電場下のバンド工学**
- **多層・界面・ヘテロ構造（HOIP）**
- **励起子 Bethe-Salpeter（Mott-Wannier の上の補正）**

---

## 2. ここ10年（2015–2026）のハライドペロブスカイト数値計算トレンド

ペロブスカイトは2015以降爆発的に研究が進展しており、TB レベルで追える物理が多い：

**(a) Rashba / Dresselhaus と動的中心反転破れ**：CsPbBr₃ 単結晶で表面 Rashba (Niesner 2016)、有機カチオン回転による動的破れ（Etienne 2016, Quarti 2016）。
**(b) 強い Spin-Hall / Berry 物理**：Pb 重い SOC、4 Lochner 2017。
**(c) 鉛フリー（Sn, Ge）と Pb 系の系統比較**：Nestoklon 2018, 2023; Kashikar 2021。
**(d) 励起子・多体・GW-BSE**：Cho 2019 arXiv:1908.09436, Filip 2018.
**(e) 2D RP / Quasi-2D**：n=1,2,3 の量子閉込め（Blancon 2018; Even 2014）。実験的 g-factor（Kopteva 2026）。
**(f) Polaron**：Fröhlich 結合定数 α が大きい（α~2.4 for MAPbI₃, Frost 2017）。移動度の温度依存性 μ ∝ T^{-1/2}。
**(g) Topology**：Pb 系 inverted gap, Z₂ 議論（Jin 2014）；2D RP Floquet topological。
**(h) 非線形光学**：BPVE bulk photovoltaic effect（Ferroelectric MAPbI3 — Wang 2017）, SHG (Stoumpos 2017)。
**(i) 熱輸送・熱電**：低κ ペロブスカイト（Pisoni 2014, Mettan 2015）。
**(j) Spin-LED, Chiral**：キラル HOIP の CD, スピン偏光検出（Long 2020 Nat. Photon., Liang 2025）。

---

## 3. 追加機能群（仕様）

優先度凡例：★★★ 必須 / ★★ 推奨 / ★ オプション

### F1 ★★★ Berry Curvature コアモジュール → AHC / SHC / Orbital Hall

**目的**：既存 velocity operator を使い、Berry curvature Ω(k) を高速計算する **コア基盤** を新設し、その上に anomalous Hall (σ_xy^AH)、spin Hall (σ_xy^SH)、orbital Hall (σ_xy^OH) を build する。立方 CsBX₃ は inversion symmetric なので AHC=0、SHC≠0、OH≠0。**鉛フリーで強い SHC/OH を予測** することが新規性。
**Novelty Statement**: 既存 future_themes Theme H は Berry phase 系を提案。本仕様で **AHC / SHC / OH を統一インフラ** で一気に計算可能にする。鉛フリー halide perovskite SHC マッピングは未報告。
**注**：非線形光学（SHG, χ⁽²⁾, BPVE）は F8 に分離。
**[既存 future_themes Theme H に対応]**

**入力**：既存 H(k)、速度演算子 v_α(k) = ∂H/∂k_α、スピン演算子 s

**出力**：
- Ω_n(k)（バンド分解 Berry curvature）
- σ_xy^AH (ω) (各バンド由来)
- σ_xy^SH (ω) (intrinsic, side-jump はオプション)
- valley Chern number per high-symmetry point

**アルゴリズム**：
1. **Berry curvature**: Kubo–like formula (Xiao–Chang–Niu 2010, Eq. 5.27)
   Ω_n^c(k) = -2 ℏ² Im Σ_{m≠n} ⟨n| v_a |m⟩⟨m| v_b |n⟩ / (E_n − E_m)²
2. **離散版（gauge invariant, multi-band）**: Fukui–Hatsugai–Suzuki (2005) リンク変数法は単バンドの場合。**縮退・準縮退バンドを含む場合は非アーベル拡張（Wilczek-Zee, Yu 2011）が必要**。本仕様では Yu 2011 多バンド Wilson loop へ標準化する。
3. **σ_xy^SH**: ⟨v_a, s_b⟩ Kubo + anti-Hermitian 部、Sinova review (2015)。spin operator は TB on-site spin matrix を使用（軌道角運動量 L は分離して F4, F8 で扱う）。

**参考文献（必須）**：
- D. Xiao, M.-C. Chang, Q. Niu, RMP 82, 1959 (2010). DOI: 10.1103/RevModPhys.82.1959
- T. Fukui, Y. Hatsugai, H. Suzuki, J. Phys. Soc. Jpn. 74, 1674 (2005). DOI: 10.1143/JPSJ.74.1674
- J. Sinova et al., RMP 87, 1213 (2015). DOI: 10.1103/RevModPhys.87.1213
- Y. Yao et al., PRL 92, 037204 (2004). DOI: 10.1103/PhysRevLett.92.037204
- G. Y. Guo et al., PRL 100, 096401 (2008). DOI: 10.1103/PhysRevLett.100.096401

**計算規模**：BZ サンプル 30³×9バンド系で ≤ 数 GB、≤ 1 h（GPU 推奨）

**検証**：
- バルク GaAs (cubic, centrosym) で AHC=0
- Bi₂Se₃ TI surface での既知 SHC 再現（簡易ベンチマーク）
- リンク変数法 → 連続式の収束次数 ∝ Δk

---

### F2 ★★★ トポロジカル不変量計算（Z₂, Wilson loop, Wannier center flow）

**目的**：CsBX₃ の Z₂ ≠ 0 / 0 判定。Pb 系で SOC + inverted gap の topology 議論を定量化（Jin 2014）。

**入力**：既存 H(k) on a dense BZ mesh

**出力**：
- Z₂ 不変量 (空間反転対称あり → Fu-Kane parity criterion)
- Wilson loop / Wannier 中心の流れ
- Surface state 計算（slab）

**アルゴリズム**：
1. Fu-Kane 2007 parity at TRIM (空間反転対称ある場合 — CsPbI₃ 立方相は対称)
2. Wilson loop method (Yu 2011)
3. Slab Green's function for surface band

**参考文献（必須）**：
- L. Fu, C. L. Kane, PRB 76, 045302 (2007). DOI: 10.1103/PhysRevB.76.045302
- R. Yu et al., PRB 84, 075119 (2011). DOI: 10.1103/PhysRevB.84.075119
- A. A. Soluyanov, D. Vanderbilt, PRB 83, 235401 (2011). DOI: 10.1103/PhysRevB.83.235401
- H. Jin, J. Im, A. J. Freeman, PRB 86, 121102(R) (2012). DOI: 10.1103/PhysRevB.86.121102 — Halide perovskite topology

**検証**：CsPbI₃ で SOC off → trivial、SOC on → inverted? を確認

---

### F3 ★★★ 励起子 Bethe-Salpeter 方程式（TB 基底, model RPA screening）

**目的**：簡易 Wannier-Mott は誘電関数 ε_r が一定の極限。Coulomb 行列要素を完全に積分した BSE で結合エネルギー・吸収スペクトルを精密化。
**Novelty Statement**: 既存 `exciton.py` (Theme I) は Wannier-Mott 簡易のみ。TB 基底 BSE は CsBX₃ 9 材料で系統未報告。Cho 2019 (GW-BSE on MAPbI₃) を TB レベルに簡易移植する位置づけ。
**規模制約**：RPA 自己整合 dielectric は本コードのスコープ外。**Cappellini–Reining model dielectric (1993)** をハード前提とする：
ε⁻¹(q) = 1 − (1 − 1/ε_∞)·q²/(q² + q_TF²)
ε_∞ は文献値（材料ごと）、q_TF はキャリア密度から Thomas-Fermi 公式

**入力**：TB 単電子状態、スクリーンド Coulomb (model dielectric, Cappellini 1993)

**出力**：
- 励起子状態 (E_n, φ_n)
- 吸収 α(ω) with excitons
- biexciton (拡張 4-body, オプション)

**アルゴリズム**：
1. Onida–Reining–Rubio 2002 RMP に従う Tamm-Dancoff BSE
2. スクリーンド Coulomb: model dielectric W(q,0) = v(q) / ε_∞ for q > q_TF
3. TB Wannier basis で K^x = δK exchange + W direct を構築

**参考文献（必須）**：
- G. Onida, L. Reining, A. Rubio, RMP 74, 601 (2002). DOI: 10.1103/RevModPhys.74.601
- M. R. Filip, F. Giustino, PRB 90, 245145 (2014). DOI: 10.1103/PhysRevB.90.245145 (Halide perovskite GW-BSE)
- Y. Cho, T. C. Berkelbach, arXiv:1908.09436 → J. Phys. Chem. Lett. 10, 6189 (2019)
- G. Cappellini, R. Del Sole, L. Reining, F. Bechstedt, PRB 47, 9892 (1993)

**計算規模**：BZ 16³×k_BSE 8³×軌道数, ≤ 16 GB, ~ 半日

**検証**：MAPbI₃ E_b 実験値 ~ 16 meV（Yang 2017）

---

### F4 ★★ Rashba / Dresselhaus 解析（中心反転破れ系）

**目的**：表面・歪み・有機カチオン秩序による Rashba split α_R を定量予測。
**Novelty Statement**: 既存実装は Rashba 計算なし。CsBX₃ 9 材料 + 歪み下 α_R(ε) マップは未報告。

**Spin operator の取扱（重要）**：
TB 基底は軌道（s, p, d）とスピン (↑,↓) の Kronecker 積。スピン期待値 ⟨S_y⟩(k) は **on-site Pauli matrix の固有値投影** で計算する。
軌道角運動量 ⟨L_y⟩ も別途出力し、全角運動量 ⟨J_y⟩ = ⟨L_y⟩ + ⟨S_y⟩ で SOC 強い系の Rashba 強度を解釈する。

**入力**：H(k) ＋ 反転破れ摂動（電場、層終端、歪み）

**出力**：
- α_R (eV·Å)
- spin texture (k 空間)

**アルゴリズム**：
1. Bychkov–Rashba 1984 形式の k·p 縮約
2. k=0 周りで spin expectation value ⟨s_y⟩(k_x) のフィット → α_R = 2 ⟨s_y⟩/k_x

**参考文献（必須）**：
- Y. A. Bychkov, E. I. Rashba, JETP Lett. 39, 78 (1984).
- D. Niesner et al., PRL 117, 126401 (2016). DOI: 10.1103/PhysRevLett.117.126401
- M. Kim et al., PNAS 111, 6900 (2014). DOI: 10.1073/pnas.1405780111
- F. Zheng et al., Nano Lett. 15, 7794 (2015). DOI: 10.1021/acs.nanolett.5b01854

**検証**：CsPbBr₃ surface α_R ~ 1 eV·Å 文献値再現

---

### F5 ★★ 2D Ruddlesden-Popper の層数依存（n=1,2,3,4 slab）
**[既存 future_themes Theme K に対応]**

**目的**：Kopteva 2026 実験（arXiv:2605.15807, g-factor of 2D RP）と直接照合。
**Novelty Statement**: 2D RP の層数依存 g-factor 系統理論計算は文献に未報告。鉛フリー (Sn/Ge) 2D RP 予測は完全に独自。
**表面終端**：z 方向有限化（slab）での dangling bond 処理は **H 様 passivation（仮想原子）** を default。または PbI₂ Cs⁺-terminated（A サイト終端）を選択可能とする（Even 2014 に基づく）。

**入力**：CsPbI₃ slab、n 層、A サイトおよびスペーサ層は埋め込み境界条件

**出力**：
- n 依存バンドギャップ E_g(n)
- spin-orbit 分裂
- g-factor g(n)
- 励起子結合 E_b(n)（F3 と統合）

**アルゴリズム**：
1. 既存 sp³d⁵s* TB を z 方向 finite size に拡張（x,y 周期）
2. 既存 g_factor.py を slab に再利用
3. F3 BSE を 2D 系に適用（layer projection）

**参考文献（必須）**：
- J.-C. Blancon et al., Science 355, 1288 (2017). DOI: 10.1126/science.aal4211
- C. Katan, N. Mercier, J. Even, Chem. Rev. 119, 3140 (2019). DOI: 10.1021/acs.chemrev.8b00417
- E. A. Kopteva et al., arXiv:2605.15807 (2026) — `references_pdf/Kopteva2026_arxiv_2605.15807.pdf` に同梱
- J. Even, L. Pedesseau, C. Katan, J. Phys. Chem. C 118, 11566 (2014). DOI: 10.1021/jp503337a

**計算規模**：~ 2000 軌道 slab、~10 GB、~ 数時間

**検証**：n→∞ で 3D バルク値に収束、Blancon 2017 Fig. 2 比較

---

### F6 ★★ Fröhlich Polaron 移動度
**[既存 future_themes Theme L に対応]**

**目的**：温度依存移動度 μ(T) を予測。鉛フリー比較に役立つ。

**入力**：TB バンド構造から有効質量 m*、LO フォノン ω_LO（文献値）、誘電率 ε_∞, ε_s

**出力**：
- Fröhlich 結合 α = (e²/4πε₀ℏ)(1/ε_∞ − 1/ε_s)(m*/2ℏω_LO)^(1/2)
- Polaron 質量 m_P = m*/(1 − α/6) (Feynman 1962, weak coupling)
- 移動度 μ_FH(T)

**アルゴリズム**：
1. m* は band curvature から既存 routine 拡張
2. Hellwarth 1999 averaged Fröhlich, Frost 2017 implementation を踏襲
3. Boltzmann 緩和時間近似

**参考文献（必須）**：
- H. Fröhlich, Adv. Phys. 3, 325 (1954). DOI: 10.1080/00018735400101213
- R. P. Feynman, R. W. Hellwarth, C. K. Iddings, P. M. Platzman, Phys. Rev. 127, 1004 (1962).
- R. W. Hellwarth, I. Biaggio, PRB 60, 299 (1999). DOI: 10.1103/PhysRevB.60.299 (Path-integral averaged mobility)
- J. M. Frost, PRB 96, 195202 (2017). DOI: 10.1103/PhysRevB.96.195202
- F. Giustino, RMP 89, 015003 (2017). DOI: 10.1103/RevModPhys.89.015003

**検証**：MAPbI₃ μ ~ 100 cm²/V·s @ 300K

---

### F7 ★★ Circular Photogalvanic Effect (CPGE)
**[既存 future_themes Theme J に対応]**

**目的**：円偏光下の直流電流 j^c = β·iE×E*。歪み/対称破り誘起。

**アルゴリズム**：既存 shift_current.py 拡張。
**参考文献（必須）**：
- F. de Juan et al., Nat. Commun. 8, 15995 (2017). DOI: 10.1038/ncomms15995
- J. E. Sipe, A. I. Shkrebtii, PRB 61, 5337 (2000). DOI: 10.1103/PhysRevB.61.5337

---

### F8 ★ 第二高調波 (SHG) と非線形光学

**目的**：強誘電 / 反転破れペロブスカイトの SHG, χ⁽²⁾ 計算。
**参考文献（必須）**：
- E. Ghahramani, D. J. Moss, J. E. Sipe, PRB 43, 9700 (1991). DOI: 10.1103/PhysRevB.43.9700
- C. Aversa, J. E. Sipe, PRB 52, 14636 (1995). DOI: 10.1103/PhysRevB.52.14636
- L. Z. Tan et al., npj Comput. Mater. 2, 16026 (2016). DOI: 10.1038/npjcompumats.2016.26

---

### F9 ★ 熱電・熱輸送（Boltzmann + 既存 velocity）

**目的**：S, σ, κ_e を BoltzTraP 形式で計算。
**参考文献（必須）**：
- G. K. H. Madsen, D. J. Singh, Comp. Phys. Commun. 175, 67 (2006). DOI: 10.1016/j.cpc.2006.03.007
- T. J. Scheidemantel et al., PRB 68, 125210 (2003).
- L. D. Whalley et al., APL Mater. 4, 091502 (2016) — Halide perovskite thermoelectric

---

### F10（削除済み：動的無秩序 / MD-TB 結合はスコープ外）

論文品質の動的無秩序解析は、(a) AIMD（HPC 必須）または (b) 大量サンプルの統計平均（数百〜数千スナップショット）を要する。デスクトップ規模では「論文品質」を達成しにくいため除外する（2026-05-24 ユーザ指示）。
- 必要な場合は外部 AIMD コード（VASP, CP2K）と本 TB の連携を別プロジェクトで実装することを推奨。
- 番号は維持（F11, F12 はそのまま）。

---

### F11 ★★ Edelstein / Inverse Edelstein 効果（電荷-スピン変換）

**目的**：Spin Hall + Edelstein 系のスピン-電荷変換効率 λ_IEE = ⟨s⟩/j。
**参考文献（必須）**：
- V. M. Edelstein, Solid State Commun. 73, 233 (1990). DOI: 10.1016/0038-1098(90)90963-C
- J. C. R. Sánchez et al., Nat. Commun. 4, 2944 (2013). DOI: 10.1038/ncomms3944

---

### F12 ★★ 歪み・電場下のバンド工学

**目的**：薄膜成長 ε=1% の歪み下での E_g, Δ_SO シフト予測。電場下 Stark shift。
**Novelty Statement**: 鉛フリー CsBX₃ 9 材料での E_g(ε) Pikus-Bir 変形ポテンシャル系統値はまだ公開実装が限定的。
**符号規約**：Bir-Pikus 1974 系（弾性スピノル基底, **strain ε_ij > 0 を引張**として正の容積変形に対し ΔE_v < 0）に統一。出力では a_v, b, d Pikus-Bir 形変形ポテンシャルとして与える。
**参考文献（必須）**：
- A. Buin et al., Nano Lett. 14, 6281 (2014).
- M. Grumet, P. Liu, M. Kaltak, J. Klimes, G. Kresse, PRB 98, 155143 (2018).
- G. L. Bir, G. E. Pikus, *Symmetry and Strain-Induced Effects in Semiconductors*, Wiley (1974).

---

### F13 ★★★ 2D Ruddlesden–Popper の z 方向無限周期化（QWSL 様 stack）

**目的**：F5 の 2D RP slab を z 方向に無限周期化し、type-II 様超格子としてのミニバンドを計算する。LD/LED 設計や、層間結合の系統評価に必要。
**Novelty Statement**: 2D RP 単一スラブ (F5) は単独の n 層を見るが、**実材料は (BA)₂(MA)$_{n-1}$Pb$_n$I$_{3n+1}$ で z 方向に周期的に積層**している。F13 は単一スラブ-周期スタック間のミニバンド分散・mini-gap を出す。

**入力**：
- F5 で構築した n 層スラブ
- スペーサ層厚（typical: BA dimer 6.4 Å）
- z 方向 k_z サンプリング

**出力**：
- z 方向ミニバンド分散 E(k_z) 
- 層間トランスファ integral t_∥, t_⊥
- ミニバンド DOS、mini-gap ΔE
- 「type-II 様」二重井戸的キャリア局在の可視化（既存 wavefunction 出力）

**アルゴリズム**：
1. F5 のスラブ TB を 1 周期分構築（z 方向、結晶格子内）
2. Bloch–Floquet 境界条件 ψ(z + L) = e^{i k_z L} ψ(z) を z 方向に課す
3. k_z スイープで一般化固有値問題
4. 単一スラブ極限 (L→∞) と 3D バルク極限 (n→∞) の整合性確認

**参考文献（必須）**：
- D. L. Smith, C. Mailhiot, *Theory of semiconductor superlattice electronic structure*, RMP 62, 173 (1990). DOI: 10.1103/RevModPhys.62.173 — 超格子 k·p / TB
- J. Even, L. Pedesseau, C. Katan, *Understanding quantum confinement of charge carriers in layered 2D hybrid perovskites*, J. Phys. Chem. C 118, 11566 (2014). DOI: 10.1021/jp503337a
- J.-C. Blancon et al., Science 355, 1288 (2017). — 2D RP n 依存実験
- D. Smith, C. Mailhiot, JAP 62, 2545 (1987). DOI: 10.1063/1.339429 — type-II SL
- C. Katan, N. Mercier, J. Even, Chem. Rev. 119, 3140 (2019). — レビュー (RP 系)

**計算規模**：F5 スラブ（~2000 軌道）× k_z 21 ≈ 数時間、メモリ ≤ 16 GB

**検証**：
- 単一スラブ極限（スペーサ→∞）でミニバンド幅 → 0
- バルク極限（n→∞）で 3D CsPbI₃ 分散に収束
- Blancon 2017 n=1,2,3,4 band gap E_g(n) を半定量再現

---

### F14 ★★★ 外部電場印加（Slab Stark 効果 + Bulk Berry phase）

**目的**：TB のバンドに外部電場を導入し、Stark shift・BPVE 補強・電場誘起 Rashba を計算する。
**Novelty Statement**: 既存 shift current/CPGE は AC 応答。本機能で DC 電場を周期境界整合に扱える。

**重要な物理的制約（QDSL F11 と同じ理由）**：
バルク 3D 周期下では一様 DC 電場は不整合。本機能は **2 モード** で提供する。

#### モード A: Slab geometry + scalar potential (F5 と組合せ)
- F5 の z 方向有限スラブに z 方向 DC 電場を **scalar potential V(z) = −eE_z·z** として直接導入。
- 平面方向は周期、z 方向は finite で問題なし。
- Stark shift、band bending、charge accumulation を直接計算可能。
- 参考文献：J. Neugebauer, M. Scheffler, PRB 46, 16067 (1992) — dipole correction

#### モード B: Bulk + Berry phase formulation
- バルク周期系には **King-Smith–Vanderbilt 1993** の Berry phase 分極式で線形応答を計算（QDSL F11 と同じ枠組み）。
- 第二量子化形の電場摂動 H_E = e·E·r は extended system では非ヒルベルト的 → polarization の Berry 位相形式で代替。
- 線形電気感受率 χ^(1)、有効電気電荷 Z*、Born effective charge を出す。

**入力**：E_z (V/Å), 既存 TB Hamiltonian, スラブ厚（モード A のみ）

**出力**：
- モード A: バンドプロファイル E_n(z, E_z)、Stark shift ΔE_n(E_z)、空間電荷分布 ρ(z, E_z)
- モード B: バルク P, χ^(1), Z*

**アルゴリズム**：
1. **モード A**: F5 スラブ TB に対角項 V_n = −e E_z z_n を加える（z_n は格子点 z 座標）。両端で dipole correction（仮想電荷層）を適用。
2. **モード B**: BZ メッシュ上で離散 Berry 位相（Resta 1998）を計算。摂動法で k·E 一次補正項を解析的に。

**参考文献（必須）**：
- J. Neugebauer, M. Scheffler, *Adsorbate-substrate and adsorbate-adsorbate interactions of Na and K adlayers on Al(111)*, PRB 46, 16067 (1992). DOI: 10.1103/PhysRevB.46.16067 — dipole correction
- L. Bengtsson, *Dipole correction for surface supercell calculations*, PRB 59, 12301 (1999). DOI: 10.1103/PhysRevB.59.12301
- R. D. King-Smith, D. Vanderbilt, PRB 47, 1651 (1993). — Berry phase polarization
- R. W. Nunes, X. Gonze, PRB 63, 155107 (2001). — finite electric field
- P. Umari, A. Pasquarello, *Ab initio molecular dynamics in a finite homogeneous electric field*, PRL 89, 157602 (2002). DOI: 10.1103/PhysRevLett.89.157602
- I. Souza, J. Iniguez, D. Vanderbilt, *First-principles approach to insulators in finite electric fields*, PRL 89, 117602 (2002). DOI: 10.1103/PhysRevLett.89.117602

**計算規模**：
- モード A: F5 スラブ × E_z スキャン、~ 数時間
- モード B: BZ メッシュ 21³ × 既存 TB、~数時間

**検証**：
- モード A: 2D RP slab で Stark shift ΔE_g ≈ e·E_z·d_slab の符号と桁
- モード B: 中心反転対称 CsPbI₃ で P = 0 (mod 量子化), Born effective charge Z*(Pb) ≈ 4.5（DFT 参照）

---

**単位系**：内部は eV / Å / V/Å / Tesla / Kelvin に統一。SI/Hartree 変換は I/O 層のみ。

## 4. アーキテクチャ統合方針

- 既存 `src/perovskite_tb/` に以下を追加：
  - `berry.py` — F1 (Berry curvature, AHC, SHC)
  - `topology.py` — F2 (Z₂, Wilson loop, surface)
  - `bse.py` — F3
  - `rashba.py` — F4
  - `slab.py` — F5 (2D RP)
  - `polaron.py` — F6
  - `cpge.py` — F7（既存 `shift_current.py` と統合可）
  - `nlo.py` — F8 (SHG, χ⁽²⁾)
  - `thermo.py` — F9
  - ~~`disorder.py` — F10~~（削除）
  - `edelstein.py` — F11
  - `bandengr.py` — F12 (strain/field)
  - `slab_stack.py` — F13 (2D RP infinite stack)
  - `efield.py` — F14 (Stark slab + Berry phase bulk)
- すべて既存 `velocity.py`, `models.py`, `g_factor.py` の共有モジュールを再利用
- 既存 PRODUCTION_RULES.md（収束確認3段階, MANIFEST.json, results/production/{theme}/{date}_{hash}/）に準拠
- 各機能のテストデータは `tests/golden/{feature}/` に凍結スナップショット

---

## 5. 段階的実装ロードマップ

| ステップ | 機能 | 工数 | 依存 |
|---|---|---|---|
| Phase A | F1 Berry/AHC/SHC | 2–3 週 | 既存 velocity |
| Phase B | F2 Topology (Z₂, Wilson) | 1–2 週 | F1 |
| Phase C | F4 Rashba 解析 | 1 週 | 既存 |
| Phase D | F6 Polaron 移動度 | 1–2 週 | 既存 |
| Phase E | F3 BSE 励起子 | 4–6 週 | F1 共有 |
| Phase F | F5 2D RP slab | 3–4 週 | F2, F3 |
| Phase G | F7 CPGE, F8 SHG | 2 週 each | F1 |
| Phase H | F9, F11, F12 | 可変 | |
| Phase I | **F13 2D RP infinite stack** | 3–4週 | F5 完了後 |
| Phase J | **F14 電場印加（モード A+B）** | 2–3週 | F5, F1 (Berry curvature) |

---

## 6. 受け入れテスト

| 機能 | テスト | 期待値 |
|---|---|---|
| F1 | 立方 CsPbI₃ (centrosym) AHC | = 0 (machine precision) |
| F1 | CsPbI₃ SHC | non-zero, > CsPbBr₃ (heavier SOC) |
| F2 | CsPbI₃ SOC on/off | Z₂ 切替 |
| F3 | MAPbI₃ E_b | ~16 meV (Yang 2017) |
| F4 | CsPbBr₃ surface | α_R ~ 1 eV·Å |
| F5 | n=1 2D RP | g-factor Kopteva 2026 と比較 |
| F6 | MAPbI₃ μ(300K) | ~ 100 cm²/V·s |
| F13 | (BA)₂(MA)$_{n-1}$Pb$_n$I$_{3n+1}$ n=1–4 stack | mini-band 幅 数 meV, E_g(n) を Blancon 2017 と一致 |
| F14 (Mode A) | n=2 2D RP slab @ E_z=0.01 V/Å | Stark shift ΔE_g ~ −e·E_z·d |
| F14 (Mode B) | バルク CsPbI₃ centrosym | P = 0 (機械精度), Z*(Pb) ≈ 4.5 (DFT 比較) |

---

## 7. 参考文献（BibTeX キー）

```bibtex
@article{Blancon2017,
  author = {J.-C. Blancon and others},
  journal = {Science}, volume = {355}, pages = {1288}, year = {2017},
  doi = {10.1126/science.aal4211}}

@article{Edelstein1990,
  author = {V. M. Edelstein},
  journal = {Solid State Commun.}, volume = {73}, pages = {233}, year = {1990}}

@article{Filip2014,
  author = {M. R. Filip and F. Giustino},
  journal = {Phys. Rev. B}, volume = {90}, pages = {245145}, year = {2014},
  doi = {10.1103/PhysRevB.90.245145}}

@article{Frost2017,
  author = {J. M. Frost},
  journal = {Phys. Rev. B}, volume = {96}, pages = {195202}, year = {2017},
  doi = {10.1103/PhysRevB.96.195202}}

@article{Fu2007,
  author = {L. Fu and C. L. Kane},
  journal = {Phys. Rev. B}, volume = {76}, pages = {045302}, year = {2007},
  doi = {10.1103/PhysRevB.76.045302}}

@article{Fukui2005,
  author = {T. Fukui and Y. Hatsugai and H. Suzuki},
  journal = {J. Phys. Soc. Jpn.}, volume = {74}, pages = {1674}, year = {2005},
  doi = {10.1143/JPSJ.74.1674}}

@article{Madsen2006,
  author = {G. K. H. Madsen and D. J. Singh},
  journal = {Comp. Phys. Commun.}, volume = {175}, pages = {67}, year = {2006},
  doi = {10.1016/j.cpc.2006.03.007}}

@article{Niesner2016,
  author = {D. Niesner and others},
  journal = {Phys. Rev. Lett.}, volume = {117}, pages = {126401}, year = {2016},
  doi = {10.1103/PhysRevLett.117.126401}}

@article{Onida2002,
  author = {G. Onida and L. Reining and A. Rubio},
  journal = {Rev. Mod. Phys.}, volume = {74}, pages = {601}, year = {2002},
  doi = {10.1103/RevModPhys.74.601}}

@article{Sinova2015,
  author = {J. Sinova and others},
  journal = {Rev. Mod. Phys.}, volume = {87}, pages = {1213}, year = {2015},
  doi = {10.1103/RevModPhys.87.1213}}

@article{Sipe2000,
  author = {J. E. Sipe and A. I. Shkrebtii},
  journal = {Phys. Rev. B}, volume = {61}, pages = {5337}, year = {2000},
  doi = {10.1103/PhysRevB.61.5337}}

@article{Xiao2010,
  author = {D. Xiao and M.-C. Chang and Q. Niu},
  journal = {Rev. Mod. Phys.}, volume = {82}, pages = {1959}, year = {2010},
  doi = {10.1103/RevModPhys.82.1959}}

@article{Yu2011,
  author = {R. Yu and others},
  journal = {Phys. Rev. B}, volume = {84}, pages = {075119}, year = {2011},
  doi = {10.1103/PhysRevB.84.075119}}
```

---

**(EOF)**
