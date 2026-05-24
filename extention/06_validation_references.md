# モデル妥当性検証 (Validation) 用 参考文献リスト

**作成日**: 2026-05-24
**目的**: 各プロジェクトに追加実装する機能について、計算結果を **実験値・既存の参照計算・標準データ集** と照合するための文献を一覧化する。

> アルゴリズム実装の "**出典**"（必須参考文献）は各仕様書本文に記載。本ファイルは **計算結果の妥当性を裏付ける比較対象** をまとめる。

---

## 0. 全体に共通する Validation 哲学

各機能について、以下の3階層で妥当性を確認する：

1. **解析解 / バルク極限**（最も厳密）：例 — バルク k·p 分散、有効質量 → 物質パラメータの整合性
2. **既存の標準的計算結果との照合**（コード相互検証）：例 — nextnano, QuantumATK, Wannier90, ABINIT
3. **実験データとの照合**（最終目標）：例 — PL 線位置、利得スペクトル、移動度、ARPES、磁化応答

---

## 1. kp-qw-simulator（QW）の Validation 文献

### 1.1 標準材料パラメータ集（k·p 入力データの正典）

- **I. Vurgaftman, J. R. Meyer, L. R. Ram-Mohan**, *Band parameters for III–V compound semiconductors and their alloys*, J. Appl. Phys. **89**, 5815 (2001). DOI: 10.1063/1.1368156 — **ZB III-V 全般の標準**
- **I. Vurgaftman, J. R. Meyer**, *Band parameters for nitrogen-containing semiconductors*, J. Appl. Phys. **94**, 3675 (2003). DOI: 10.1063/1.1600519 — **窒化物 (GaN/InN/AlN)**
- **P. Rinke et al.**, *Consistent set of band parameters for the group-III nitrides AlN, GaN, and InN*, Phys. Rev. B **77**, 075202 (2008). DOI: 10.1103/PhysRevB.77.075202 — **GW corrected nitride parameters**

### 1.2 F1 多体補正利得 — 実験/既存コード比較

- **W. W. Chow, S. W. Koch, M. Sargent III**, *Semiconductor-Laser Physics*, Springer (1994). — Free-carrier vs many-body 比較データ
- **W. W. Chow, S. W. Koch**, *Semiconductor-Laser Fundamentals*, Springer (1999). — Fig. 10.x 系列を直接照合可能 [PDF 同梱]
- **J. Hader, J. V. Moloney, S. W. Koch**, *Influence of internal fields on gain and spontaneous emission in InGaN quantum wells*, APL **89**, 171120 (2006). DOI: 10.1063/1.2369541 — InGaN MQW
- **J. Piprek**, *Nitride Semiconductor Devices*, Wiley-VCH (2007). — GaN/InGaN 利得実験比較

### 1.3 F2 励起子 — 実験

- **L. C. Andreani**, *Optical transitions, excitons, and polaritons in bulk and low-dimensional semiconductor structures*, in *Confined Electrons and Photons*, ed. Burstein, Plenum (1995). — レビュー、QW 励起子の標準
- **R. T. Greene, K. K. Bajaj, D. E. Phelps**, *Energy levels of Wannier excitons in GaAs–Ga$_{1-x}$Al$_x$As quantum-well structures*, PRB **29**, 1807 (1984). DOI: 10.1103/PhysRevB.29.1807 — 解析的計算
- **D. C. Reynolds et al.**, *Quantum-well systems – PL and excitons*, PRB **31**, 2236 (1985). — PL 実験
- **R. L. Greene, K. K. Bajaj**, *Effect of magnetic fields on the energy levels of a hydrogenic system in a Ga(1-x)Al(x)As–GaAs quantum well structure*, PRB **31**, 6498 (1985). — 磁場下励起子

### 1.4 F3 Auger — 実験/コード比較

- **E. Kioupakis, P. Rinke, K. T. Delaney, C. G. Van de Walle**, *Indirect Auger recombination as a cause of efficiency droop in nitride LEDs*, APL **98**, 161107 (2011). — first-principles InGaN Auger
- **A. R. Beattie, P. T. Landsberg**, Proc. R. Soc. A **249**, 16 (1959). — 原典の解析公式
- **J. Iveland, L. Martinelli, J. Peretti, J. S. Speck, C. Weisbuch**, *Direct measurement of Auger electrons emitted from a semiconductor light-emitting diode under electrical injection*, PRL **110**, 177406 (2013). — Auger 直接測定実験

### 1.5 F4 g-tensor — 実験/コード比較

- **A. Malinowski, R. T. Harley**, *Anisotropy of the electron g factor in lattice-matched and strained-layer III-V quantum wells*, PRB **62**, 2051 (2000). DOI: 10.1103/PhysRevB.62.2051 — QW g 因子実験
- **W. Zawadzki, P. Pfeffer**, *Spin splitting of subband energies due to inversion asymmetry in semiconductor heterostructures*, Semicond. Sci. Technol. **19**, R1 (2004). — レビュー
- **C. E. Pryor, M. E. Flatté**, PRL **96**, 026804 (2006). — k·p 計算自体

### 1.6 F5 Z₂ Topology — 実験

- **M. König, S. Wiedmann, C. Brüne, A. Roth, H. Buhmann, L. W. Molenkamp, X.-L. Qi, S.-C. Zhang**, *Quantum spin Hall insulator state in HgTe quantum wells*, Science **318**, 766 (2007). DOI: 10.1126/science.1148047 — **HgTe QW QSH 実験**
- **I. Knez, R.-R. Du, G. Sullivan**, *Evidence for helical edge modes in inverted InAs/GaSb quantum wells*, PRL **107**, 136603 (2011). — InAs/GaSb QSH 実験
- **B. A. Bernevig, T. L. Hughes, S.-C. Zhang**, Science **314**, 1757 (2006). — 理論原典 (BHZ モデル)

### 1.7 F7 Non-Hermitian / F8 Disorder / F9 Polariton — 実験

- **L. Feng, R. El-Ganainy, L. Ge**, *Non-Hermitian photonics based on parity–time symmetry*, Nat. Photonics **11**, 752 (2017). — レビュー
- **F. Sacconi et al.**, *Optical and transport properties of stacked InGaN/GaN quantum wells*, PRB **86**, 085210 (2012). — alloy disorder
- **A. V. Kavokin et al.**, *Microcavities*, Oxford UP (2nd ed., 2017). — polariton 標準教科書
- **J. Kasprzak et al.**, *Bose–Einstein condensation of exciton polaritons*, Nature **443**, 409 (2006). — polariton BEC 実験

### 1.8 ベンチマークコード (cross-check 対象)

- **nextnano** ([nextnano.com](https://www.nextnano.com)) — 商用 k·p / Schrödinger-Poisson。GaAs/AlGaAs QW、InGaN QW のベンチマークが公開
- **Sentaurus Workbench** (Synopsys) — 産業用
- **QuantumATK** — Atomistix
- **QtCAD / OMEN** — DFT-NEGF cross-check
- **WannierTools** ([wanniertools.com](http://wanniertools.org)) — トポロジー Wilson loop ベンチマーク（F5）

---

## 2. kp8band-qdsl（QD/QDSL）の Validation 文献

### 2.1 単一 QD ベンチマーク

- **O. Stier, M. Grundmann, D. Bimberg**, *Electronic and optical properties of strained quantum dots modeled by 8-band k·p theory*, PRB **59**, 5688 (1999). DOI: 10.1103/PhysRevB.59.5688 — **単一 InAs/GaAs QD の標準計算**
- **A. Schliwa, M. Winkelnkemper, D. Bimberg**, PRB **76**, 205324 (2007); PRB **79**, 075443 (2009). — atomistic 計算
- **W. Sheng, S.-J. Cheng, P. Hawrylak**, *Multiband theory of multi-exciton complexes in self-assembled quantum dots*, PRB **71**, 035316 (2005). — 多励起子
- **G. Bester, A. Zunger**, *Cylindrically shaped zinc-blende semiconductor quantum dots do not have cylindrical symmetry*, PRB **71**, 045318 (2005). — 対称性低下

### 2.2 QDSL ミニバンド・吸収 (F8 の照合点)

- **T. Kotani, S. Birner, P. Lugli, C. Hamaguchi**, JAP **115**, 143501 (2014). — **参照論文** [PDF 同梱]
- **S. Tomic, T. S. Jones, N. M. Harrison**, *Absorption characteristics of a quantum dot array induced intermediate band: implications for solar cell design*, APL **93**, 263105 (2008). — QDSL 吸収
- **M. Y. Levy, C. Honsberg**, *Solar cell with an intermediate band of finite width*, PRB **78**, 165122 (2008). — 2-step 吸収
- **A. Marti, L. Cuadra, A. Luque**, *Quantum dot intermediate band solar cell*, Conf. Rec. IEEE Photovolt. Spec. Conf. (2000), p. 940. — IBSC 提案

### 2.3 FSS 実験 (F1 の照合点)

- **M. Bayer et al.**, PRB **65**, 195315 (2002). — FSS 実験
- **R. M. Stevenson, R. J. Young, P. Atkinson, K. Cooper, D. A. Ritchie, A. J. Shields**, *A semiconductor source of triggered entangled photon pairs*, Nature **439**, 179 (2006). — entangled photon
- **R. Trotta et al.**, Nat. Commun. **7**, 10375 (2016). — strain-tuned FSS
- **D. Huber et al.**, PRL **121**, 033902 (2018). — GaAs droplet QD with FSS≈0

### 2.4 多励起子・CI ベンチマーク (F2)

- **M. Korkusinski, P. Hawrylak**, PRB **87**, 115310 (2013). — CI 計算 QD
- **S. Rodt, R. Heitz, A. Schliwa, R. L. Sellin, F. Guffarth, D. Bimberg**, *Repulsive exciton-exciton interaction in InAs/GaAs quantum dots*, PRB **68**, 035331 (2003). — 多励起子相互作用
- **R. J. Warburton, B. T. Miller, C. S. Dürr, C. Bödefeld, K. Karrai, J. P. Kotthaus, G. Medeiros-Ribeiro, P. M. Petroff, S. Huant**, *Coulomb interactions in small charge-tunable QDs*, PRB **58**, 16221 (1998). — charging energies

### 2.5 g-tensor 実験 (F3)

- **C. E. Pryor, M. E. Flatté**, PRL **96**, 026804 (2006). — 理論
- **A. Andlauer, P. Vogl**, PRB **79**, 045307 (2009). — k·p 計算
- **K. Vyborny, A. F. Kockum, P. Hyldgaard, L. K. Hyttinen**, PRB **80**, 165420 (2009). — small QD g-tensor

### 2.6 IBSC 実験 (F8 の照合点)

- **A. Marti et al.**, *Production of photocurrent due to intermediate-to-conduction-band transitions: a demonstration of a key operating principle of the intermediate-band solar cell*, PRL **97**, 247701 (2006). — **IBSC 動作原理実証**
- **Y. Okada et al.**, *Intermediate band solar cells: Recent progress and future directions*, Appl. Phys. Rev. **2**, 021302 (2015). — レビュー
- **A. Luque, A. Marti, C. Stanley**, *Understanding intermediate-band solar cells*, Nat. Photonics **6**, 146 (2012). — レビュー
- **A. Luque, A. Marti**, PRL **78**, 5014 (1997). — IBSC 原典 [PDF 同梱]

### 2.7 ベンチマークコード

- **nextnano** — single QD ベンチマークが豊富
- **Schliwa の TB code** (private) — atomistic 比較用 (公開はされていないが論文 figure 比較)
- **APSYS** — 商用 QD device simulator

---

## 3. tb-perovskite（TB）の Validation 文献

### 3.1 バンド構造 DFT/GW ベンチマーク

- **F. Brivio, J. M. Frost, J. M. Skelton, A. J. Jackson, O. J. Weber, M. T. Weller, A. R. Wadge, A. Walsh**, *Lattice dynamics and vibrational spectra of orthorhombic, tetragonal and cubic phases of methylammonium lead iodide*, PRB **92**, 144308 (2015). — phonon
- **F. Brivio, K. T. Butler, A. Walsh, M. van Schilfgaarde**, *Relativistic quasiparticle self-consistent electronic structure of hybrid halide perovskite photovoltaic absorbers*, PRB **89**, 155204 (2014). DOI: 10.1103/PhysRevB.89.155204 — QSGW MAPbI₃
- **G. Volonakis, M. R. Filip et al.**, *Lead-free halide double perovskites via heterovalent substitution of noble metals*, J. Phys. Chem. Lett. **7**, 1254 (2016). — 鉛フリー DFT
- **Y. Yang et al.**, *Top and bottom surfaces limit carrier lifetime in lead iodide perovskite films*, Nat. Energy **2**, 16207 (2017). — エネルギーバンド実験

### 3.2 励起子結合エネルギー (F3 BSE 照合)

- **K. Galkowski, A. Mitioglu, A. Miyata, P. Plochocka, O. Portugall, G. E. Eperon, J. T.-W. Wang, T. Stergiopoulos, S. D. Stranks, H. J. Snaith, R. J. Nicholas**, *Determination of the exciton binding energy and effective masses for methylammonium and formamidinium lead tri-halide perovskite semiconductors*, Energy Environ. Sci. **9**, 962 (2016). DOI: 10.1039/C5EE03435C — **E_b 実験標準**
- **A. Miyata, A. Mitioglu, P. Plochocka, O. Portugall, J. T.-W. Wang, S. D. Stranks, H. J. Snaith, R. J. Nicholas**, *Direct measurement of the exciton binding energy and effective masses for charge carriers in organic-inorganic tri-halide perovskites*, Nat. Phys. **11**, 582 (2015). — magneto-PL
- **Z. Yang, A. Surrente, K. Galkowski, A. Miyata, O. Portugall, R. J. Sutton, A. A. Haghighirad, H. J. Snaith, D. K. Maude, P. Plochocka, R. J. Nicholas**, *Impact of the halide cage on the electronic properties of fully inorganic cesium lead halide perovskites*, ACS Energy Lett. **2**, 1621 (2017). — CsPbX₃ Eb
- **M. R. Filip, F. Giustino**, PRB **90**, 245145 (2014). — GW-BSE 計算

### 3.3 Berry curvature / Hall (F1)

- **Y. Yao et al.**, PRL **92**, 037204 (2004). — bcc Fe AHC: 標準ベンチマーク
- **G. Y. Guo, S. Murakami, T.-W. Chen, N. Nagaosa**, PRL **100**, 096401 (2008). — 4d 金属 SHC ベンチマーク
- **N. P. Stern, M. Steuerman, S. Mack, A. C. Gossard, D. D. Awschalom**, *Time-resolved Kerr rotation imaging of the spin Hall effect*, Nat. Phys. **4**, 843 (2008). — SHC 実験
- **WannierTools** ([wanniertools.org](http://wanniertools.org)) — Z₂, Wilson loop コード比較

### 3.4 Rashba (F4)

- **D. Niesner et al.**, PRL **117**, 126401 (2016). — CsPbBr₃ ARPES Rashba
- **F. Zheng, L. Z. Tan, S. Liu, A. M. Rappe**, *Rashba spin-orbit coupling enhanced carrier lifetime in CH₃NH₃PbI₃*, Nano Lett. **15**, 7794 (2015). — DFT Rashba
- **M. Kim et al.**, *Rashba effect and large spin-orbit splitting in 2D and 3D perovskite oxides*, PNAS **111**, 6900 (2014). — perovskite oxide Rashba

### 3.5 2D RP (F5)

- **J.-C. Blancon et al.**, Science **355**, 1288 (2017). — n=1,2,3,4 of (BA)₂(MA)$_{n-1}$Pb$_n$I$_{3n+1}$ 系
- **C. Katan, N. Mercier, J. Even**, Chem. Rev. **119**, 3140 (2019). — レビュー
- **E. A. Kopteva et al.**, arXiv:2605.15807 (2026). — **層数依存 g-factor 実験** [PDF 同梱]

### 3.6 Polaron 移動度 (F6)

- **J. M. Frost**, PRB **96**, 195202 (2017). — Fröhlich α 計算
- **L. M. Herz**, *Charge-carrier mobilities in metal halide perovskites: Fundamental mechanisms and limits*, ACS Energy Lett. **2**, 1539 (2017). — μ レビュー
- **A. Filippetti, P. Delugas, A. Mattoni**, *Radiative recombination and photoconversion of methylammonium lead iodide perovskite by first principles: properties of an inorganic semiconductor within a hybrid body*, J. Phys. Chem. C **118**, 24843 (2014).
- **C. Wehrenfennig, G. E. Eperon, M. B. Johnston, H. J. Snaith, L. M. Herz**, *High charge carrier mobilities and lifetimes in organolead trihalide perovskites*, Adv. Mater. **26**, 1584 (2014).

### 3.7 Shift current / CPGE / SHG (F7, F8)

- **L. Z. Tan, F. Zheng, S. M. Young, F. Wang, S. Liu, A. M. Rappe**, *Shift current bulk photovoltaic effect in polar materials*, npj Comput. Mater. **2**, 16026 (2016). — Tan shift current
- **F. de Juan et al.**, Nat. Commun. **8**, 15995 (2017). — Weyl CPGE
- **F. Wang, S. Steinhauer, T. Lobo, D. Bonn, J. Kioseoglou, R. F. Werner, J. M. Frost, A. Walsh**, *Optical absorption and photoluminescence in CsPb(Br_x I_{1-x})_3 mixed halide perovskites*, J. Phys. Chem. C **120**, 27290 (2016).

### 3.8 熱電 (F9)

- **L. D. Whalley et al.**, APL Mater. **4**, 091502 (2016). — perovskite thermoelectric

### 3.9 ベンチマークコード

- **Wannier90** — TB→Wannier 変換、Berry phase, topology
- **WannierTools** — Z₂, surface bands
- **BoltzTraP / BoltzTraP2** — 熱輸送
- **PythTB** — TB toolbox （Berry curvature 公式比較）
- **abinit** — DFT-BSE
- **YAMBO** — GW-BSE for solids

---

## 4. 「論文化に向けた」標準ベンチマーク表

各機能の妥当性確認のために **最低限再現すべき** 既存結果：

| プロジェクト | 機能 | 最低再現対象 | 期待精度 |
|---|---|---|---|
| QW | F1 多体利得 | GaAs/AlGaAs SQW @ T=300K, N=2×10¹² cm⁻²。BGR ~ −15 meV | ±5 meV |
| QW | F2 励起子 | GaAs/Al₀.₃Ga₀.₇As Lw=10nm, Eb ~ 9 meV (Andreani 1990) | ±1 meV |
| QW | F3 Auger | InGaAsP λ=1.55μm Cp(300K) ≈ 7×10⁻²⁹ cm⁶/s (Kioupakis 2011) | ±50% (order) |
| QW | F4 g-tensor | バルク GaAs g* = −0.44 (Roth–Lax 解析解) | ±0.02 |
| QW | F5 Z₂ | HgTe QW d_c ≈ 6.3 nm (König 2007) | ±0.5 nm |
| QDSL | F1 FSS | 対称形 InGaAs/GaAs QD で FSS=0±数μeV | < 10 μeV |
| QDSL | F2 CI | InGaAs/GaAs biexciton Δb ≈ +2 meV (Bayer 2002) | ±1 meV |
| QDSL | F3 g-tensor | バルク InAs g* ≈ −14.9 | ±1 |
| QDSL | F8 IBSC | Kotani 2014 Fig. 9 の Lz 依存吸収端 | 定性的 + 半定量的 |
| TB | F1 AHC | bcc Fe AHC ≈ 750 (Ω·cm)⁻¹ (Yao 2004) | ±10% |
| TB | F2 Z₂ | Bi₂Se₃ Z₂=1 (Fu-Kane parity) | bit-identical |
| TB | F3 BSE | MAPbI₃ E_b ≈ 16 meV (Yang 2017) | ±3 meV |
| TB | F4 Rashba | CsPbBr₃ surface α_R ~ 1 eV·Å (Niesner 2016) | ±30% |
| TB | F5 2D RP | n=1,2,3,4 (BA)₂(MA)$_{n-1}$Pb$_n$I$_{3n+1}$ g-factor Kopteva 2026 | ±0.2 |
| TB | F6 Mobility | MAPbI₃ μ(300K) ~ 100 cm²/V·s (Wehrenfennig 2014) | ±50% (Fröhlich limit) |

---

## 5. PDF 同梱状況

`references_pdf/` フォルダに同梱済みの Validation 文献：

- `Marti1997_PRL78_5014.pdf` — Luque–Marti IBSC 原典
- `Chichibu_Presen.pdf` — InGaN PL 実験
- `Kotani2014_JAP115_143501.pdf` — QDSL ベース論文
- `Kotani2013_APL102_011128.pdf` — QW ベース論文
- `arxiv_1908.09436.pdf` — Cho 2019 GW-BSE
- `Kopteva2026_arxiv_2605.15807.pdf` — 2D RP g-factor 実験
- 他、`05_references_index.md` を参照

未同梱の Validation 文献は DOI/URL から取得すること。**実装着手前に必ず該当論文を取得し、Figure / Table を確認** する。

---

## 6. 検証フロー（推奨）

各機能の実装エージェントは：

1. **解析解テスト** — バルク k·p、Hydrogenic limit、自由電子 limit
2. **既存コード比較** — nextnano, Wannier90, WannierTools などの公開結果と1点照合
3. **論文 Figure 再現** — 上記 §4 表の対象を pytest として固定
4. **実験データ比較** — 該当機能の代表実験（§1.2–1.8 / 2.3–2.6 / 3.2–3.8）と1点比較
5. **収束テスト** — メッシュ・基底数・カットオフ依存性を確認

これらを **全て** 通過したものを「論文に出せる品質」と認める。
