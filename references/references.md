# Tight-Binding × ペロブスカイト 文献リスト（光デバイス材料）

**収集日:** 2026-05-23
**検索クエリ:** arXiv 全文検索 `"tight binding" perovskite`
**期間:** 2016年以降（直近10年）
**件数:** 49 件（全件 PDF 取得済み）
**保存場所:** `./pdfs/arxiv_<arxiv_id>.pdf`

## このフォルダで何ができるか（Claude Code 向けメモ）

このディレクトリにあるPDFは、ペロブスカイト系材料の電子構造をタイトバインディング（TB）モデル、Slater-Koster、Wannier、DFTB（GFN1-xTB含む）、k·p などで記述した論文を網羅的に集めたものです。研究関心は **光デバイスに使える材料**（太陽電池、LED、光検出器、非線形光学、円二色性、量子閉じ込め発光など）が中心です。

主な分析の切り口の例:

- 各論文で使われているTBモデルの **軌道基底（sp3d5s\*, p-only, s-p, d-only など）** とパラメータ数を表化する
- 対象材料を **ハライド系 / 酸化物系 / 窒化物系 / 二次元層状系** に分類して傾向を見る
- スピン軌道相互作用（SOC）の取り扱い・ランデg因子・励起子効果の扱いを比較
- DFT→TB パラメータ化手法（Wannier90、DFTB再パラメータ化、Slater-Koster fit）の系譜
- 光学応答計算（誘電関数、円二色性、バルク光起電力、非相反輸送）の手法比較

---

## 全論文一覧（新しい順）

### 2026

| arXiv ID | 著者 | タイトル | PDF |
|---|---|---|---|
| 2605.22453 | Surajit Adhikari et al. | Harnessing Linear and Nonlinear Optical Responses in Ferroelectric LaMoN₃ for Enhanced Photovoltaic Efficiency | [PDF](pdfs/arxiv_2605.22453.pdf) |
| 2605.15807 | Nataliia E. Kopteva et al. | Layer-dependent Landé g-factors of electrons, holes, and excitons in two-dimensional Ruddlesden-Popper lead halide perovskites | [PDF](pdfs/arxiv_2605.15807.pdf) |
| 2602.19637 | Taeung Kim et al. | Data-Driven Bath Fitting for Hamiltonian-Diagonalization Dynamical Mean-Field Theory | [PDF](pdfs/arxiv_2602.19637.pdf) |

### 2025

| arXiv ID | 著者 | タイトル | PDF |
|---|---|---|---|
| 2512.13663 | Zihan Zhang et al. | Nonreciprocal Transport with Quantum Geometric Origin in Layered Hybrid Perovskite | [PDF](pdfs/arxiv_2512.13663.pdf) |
| 2511.14029 | Kristoffer Eggestad et al. | Twin-boundary-induced nonrelativistic spin splitting | [PDF](pdfs/arxiv_2511.14029.pdf) |
| 2510.03406 | Maryam A. Nasir et al. | Spin-orbit coupling and the Edelstein effect at conducting ferroelectric domain walls | [PDF](pdfs/arxiv_2510.03406.pdf) |
| 2507.07039 | Ziye Zhu et al. | Emergent Multiferroic Altermagnets and Spin Control via Noncollinear Molecular Polarization | [PDF](pdfs/arxiv_2507.07039.pdf) |
| 2506.23167 | Pol Benítez et al. | Band-Gap Tunability in Anharmonic Perovskite-like Semiconductors Driven by Polar Electron-Phonon Coupling | [PDF](pdfs/arxiv_2506.23167.pdf) |
| 2505.18027 | Dongkeun Lee et al. | A variational quantum eigensolver tailored to multi-band tight-binding simulations of electronic structures | [PDF](pdfs/arxiv_2505.18027.pdf) |
| 2502.20261 | Andrew Grieder et al. | Carrier Localization and Spontaneous Formation of Two-Dimensional Polarization Domain in Halide Perovskites | [PDF](pdfs/arxiv_2502.20261.pdf) |
| 2501.06503 | Misbah Shaheen et al. | Density Functional Leveraged Tight-binding Insights into Inorganic Halide Perovskites | [PDF](pdfs/arxiv_2501.06503.pdf) |

### 2024

| arXiv ID | 著者 | タイトル | PDF |
|---|---|---|---|
| 2412.07016 | Junke Jiang et al. | Flexible and Efficient Semi-Empirical DFTB Parameters for Electronic Structure Prediction of 3D, 2D Iodide Perovskites and Heterostructures | [PDF](pdfs/arxiv_2412.07016.pdf) |
| 2411.16497 | Daniel T. Larson et al. | Stacking-dependent electronic structure of ultrathin perovskite bilayers | [PDF](pdfs/arxiv_2411.16497.pdf) |
| 2410.19142 | Emily G. Ward et al. | Tight-Binding Models for Lone Pair, Heteroanionic Solids, and Application to Layered Oxyhalides | [PDF](pdfs/arxiv_2410.19142.pdf) |

### 2023

| arXiv ID | 著者 | タイトル | PDF |
|---|---|---|---|
| 2310.06043 | B. C. Cornell et al. | Influence of a Realistic Multiorbital Band Structure on Conducting Domain Walls in Perovskite Ferroelectrics | [PDF](pdfs/arxiv_2310.06043.pdf) |
| 2309.14002 | Sofia Apergi et al. | Calculating the Circular Dichroism of Chiral Halide Perovskites: A Tight-Binding Approach | [PDF](pdfs/arxiv_2309.14002.pdf) |
| 2307.09464 | Efstratios Manousakis | Towards understanding the electronic structure of the simpler members of two-dimensional halide-perovskites | [PDF](pdfs/arxiv_2307.09464.pdf) |
| 2305.10586 | M. O. Nestoklon et al. | Tailoring the electron and hole Landé factors in lead halide perovskite nanocrystals by quantum confinement and halide exchange | [PDF](pdfs/arxiv_2305.10586.pdf) |
| 2303.00390 | Edgar Abarca Morales et al. | Hierarchy of Lifshitz transitions in the surface electronic structure of Sr₂RuO₄ under uniaxial compression | [PDF](pdfs/arxiv_2303.00390.pdf) |
| 2302.13773 | Ankita Phutela et al. | Strain-driven topological quantum phase transition in the family of halide perovskites | [PDF](pdfs/arxiv_2302.13773.pdf) |
| 2302.01545 | Arindam Sarkar et al. | Ligand hole driven metal-insulator transition in a prototypical transition metal double perovskite oxide Ca₂FeMnO₆ | [PDF](pdfs/arxiv_2302.01545.pdf) |

### 2022

| arXiv ID | 著者 | タイトル | PDF |
|---|---|---|---|
| 2210.01324 | (Lead halide perovskite NC excitons) | Excitons and their Fine Structure in Lead Halide Perovskite Nanocrystals from Atomistic Modeling | [PDF](pdfs/arxiv_2210.01324.pdf) |
| 2209.13267 | Subhayan Roychoudhury et al. | Investigating the Electronic Structure of Prospective Water-splitting Oxide BaCe₀.₂₅Mn₀.₇₅O₃₋δ Before and After Thermal Reduction | [PDF](pdfs/arxiv_2209.13267.pdf) |
| 2203.11308 | Emanuel A. Martínez et al. | BinPo: An open-source code to compute the band structure of two-dimensional electron systems | [PDF](pdfs/arxiv_2203.11308.pdf) |

### 2021

| arXiv ID | 著者 | タイトル | PDF |
|---|---|---|---|
| 2112.15384 | E. Kirstein et al. | The Landé factors of electrons and holes in lead halide perovskites: universal dependence on the band gap | [PDF](pdfs/arxiv_2112.15384.pdf) |
| 2110.15827 | Sander Raaijmakers et al. | A Reparameterized Density Functional Tight-Binding Method for Engineering phase-stable CsPbX₃ Perovskites | [PDF](pdfs/arxiv_2110.15827.pdf) |
| 2109.08104 | Derek Churchill et al. | Competing multipolar orders in a face-centered cubic lattice: Application to the osmium double perovskites | [PDF](pdfs/arxiv_2109.08104.pdf) |
| 2109.07769 | Wataru Kobayashi | Thermopower in transition-metal perovskites | [PDF](pdfs/arxiv_2109.07769.pdf) |
| 2107.05906 | Hyeong Jun Lee et al. | Hund's metallicity enhanced by van Hove singularity in cubic perovskite systems | [PDF](pdfs/arxiv_2107.05906.pdf) |
| 2107.00348 | Maximilian E. Merkel et al. | Charge disproportionation and Hund's insulating behavior in a five-orbital Hubbard model applicable to d⁴ perovskites | [PDF](pdfs/arxiv_2107.00348.pdf) |
| 2105.11310 | Sangeeta Rajpurohit et al. | A non-perturbative study of bulk photovoltaic effect enhanced by an optically induced phase transition | [PDF](pdfs/arxiv_2105.11310.pdf) |
| 2105.06525 | David J. Abramovitch et al. | Thermal fluctuations and carrier localization induced by dynamic disorder in MAPbI3 described by a first-principles based tight-binding model | [PDF](pdfs/arxiv_2105.06525.pdf) |
| 2104.07771 | Mohammad Reza Benam et al. | Holes' character and bond versus charge disproportionation in s-p ABX₃ perovskites | [PDF](pdfs/arxiv_2104.07771.pdf) |
| 2104.01738 | J. M. Vicent-Luna et al. | Efficient Computation of Metal Halide Perovskites Properties using the Extended Density Functional Tight Binding: GFN1-xTB Method | [PDF](pdfs/arxiv_2104.01738.pdf) |
| 2101.08562 | Ravi Kashikar et al. | A Generic Slater-Koster Description of the Electronic Structure of Centrosymmetric Halide Perovskites | [PDF](pdfs/arxiv_2101.08562.pdf) |

### 2020

| arXiv ID | 著者 | タイトル | PDF |
|---|---|---|---|
| 2012.14705 | M. O. Nestoklon | Tight-binding description of inorganic lead halide perovskites in cubic phase | [PDF](pdfs/arxiv_2012.14705.pdf) |
| 2005.11961 | D. Takegami et al. | Charge transfer energy in iridates: a hard x-ray photoelectron spectroscopy study | [PDF](pdfs/arxiv_2005.11961.pdf) |
| 2001.01169 | Shreemoyee Ganguly et al. | Study of Nontrivial Magnetism in 3d-5d Transition Metal based Double Perovskites | [PDF](pdfs/arxiv_2001.01169.pdf) |

### 2019

| arXiv ID | 著者 | タイトル | PDF |
|---|---|---|---|
| 1908.09436 | Yeongsu Cho et al. | Thickness-dependent optical properties of layered hybrid organic-inorganic halide perovskites: A tight-binding GW-BSE study | [PDF](pdfs/arxiv_1908.09436.pdf) |
| 1905.07962 | Vu Thi Ngoc Huyen et al. | Topology analysis for anomalous Hall effect in the non-collinear antiferromagnetic states of Mn₃A N (A = Ni, Cu, Zn, Ga, Ge, Pd, In, Sn, Ir, Pt) | [PDF](pdfs/arxiv_1905.07962.pdf) |
| 1902.06646 | Shuxia Tao et al. | Absolute energy level positions in tin and lead based halide perovskites | [PDF](pdfs/arxiv_1902.06646.pdf) |

### 2018

| arXiv ID | 著者 | タイトル | PDF |
|---|---|---|---|
| 1811.11081 | Ravi Kashikar et al. | Second Neighbor Electron Hopping and Pressure Induced Topological Quantum Phase Transition in Insulating Cubic Perovskites | [PDF](pdfs/arxiv_1811.11081.pdf) |
| 1807.07168 | Arash Khazraie et al. | Bond versus charge disproportionation in the bismuth perovskites | [PDF](pdfs/arxiv_1807.07168.pdf) |
| 1802.09677 | Amrita Pal et al. | Influence of the aggregate state on band structure and optical properties of C60 computed with different methods | [PDF](pdfs/arxiv_1802.09677.pdf) |
| 1802.00034 | Arash Khazraie et al. | Oxygen holes and hybridization in the bismuthates | [PDF](pdfs/arxiv_1802.00034.pdf) |

### 2017

| arXiv ID | 著者 | タイトル | PDF |
|---|---|---|---|
| 1704.04211 | Bramhachari Khamari et al. | Topologically Invariant Double Dirac States in Bismuth based Perovskites: Consequence of Ambivalent Charge States and Covalent Bonding | [PDF](pdfs/arxiv_1704.04211.pdf) |
| 1703.03574 | S. Ashhab et al. | Effect of disorder on transport properties in a tight-binding model for lead halide perovskites | [PDF](pdfs/arxiv_1703.03574.pdf) |

### 2016

| arXiv ID | 著者 | タイトル | PDF |
|---|---|---|---|
| 1611.04641 | Marlou R. Slot et al. | Experimental realization and characterization of an electronic Lieb lattice | [PDF](pdfs/arxiv_1611.04641.pdf) |
| 1608.02983 | A. M. Cook | Individual band with higher Chern numbers in double perovskite {001} monolayers | [PDF](pdfs/arxiv_1608.02983.pdf) |

---

## 重要論文の分類タグ（分析の補助用）

### 光デバイス（直接的）に最も関連
- **2605.22453** ペロブスカイト系窒化物の光起電力
- **2506.23167** ペロブスカイト類似半導体のバンドギャップチューニング
- **2502.20261** ハライドペロブスカイトのキャリア局在
- **2309.14002** キラルハライドペロブスカイトの円二色性（TB）
- **2105.11310** バルク光起電力効果
- **2105.06525** MAPbI3の動的不規則性
- **1908.09436** 層状ハイブリッドペロブスカイトの光学（TB-GW-BSE）

### TB/Slater-Koster/DFTB の手法論
- **2505.18027** マルチバンドTB用の変分量子固有値解法
- **2412.07016** 3D・2D ヨウ化ペロブスカイト用 DFTB パラメータ
- **2410.19142** Lone pair 系・ヘテロアニオン固体の TB モデル
- **2110.15827** CsPbX₃ 用の再パラメータ化 DFTB
- **2104.01738** Metal halide perovskites の DFTB (GFN1-xTB)
- **2101.08562** 中心対称ハライドペロブスカイトの汎用 Slater-Koster 記述
- **2012.14705** 立方晶 inorganic 鉛ハライドペロブスカイトの TB
- **1703.03574** ハライドペロブスカイト用 TB（不規則性）

### Landé g因子・励起子・量子閉じ込め
- **2605.15807** 2D RP ハライドペロブスカイト
- **2305.10586** ナノ結晶の g因子チューニング
- **2210.01324** ナノ結晶の励起子微細構造
- **2112.15384** バンドギャップ依存の g因子普遍則

### 二次元・層状・ヘテロ
- **2411.16497** Ultrathin ペロブスカイト二層膜
- **2307.09464** 2D ハライドペロブスカイトの電子構造
- **1611.04641** Lieb 格子の実験（参考：TB 格子）

### トポロジカル・スピン軌道
- **2512.13663** 非相反輸送と量子幾何
- **2510.03406** 強誘電体ドメイン壁のスピン軌道（Edelstein）
- **2302.13773** ハライドペロブスカイトの歪み誘起トポロジカル相転移
- **1704.04211** ビスマス系ペロブスカイトの二重 Dirac 状態
- **1811.11081** 立方ペロブスカイトの圧力誘起トポロジカル相転移
- **1608.02983** ダブルペロブスカイト単層の高 Chern 数

### 酸化物・遷移金属系（光デバイス周辺の参考）
- **2310.06043** ペロブスカイト強誘電体の伝導ドメイン壁
- **2303.00390** Sr₂RuO₄ Lifshitz 転移
- **2302.01545** Ca₂FeMnO₆ 金属絶縁体転移
- **2209.13267** 水分解用 BaCeMnO₃
- **2203.11308** 2D 電子系バンド構造計算コード BinPo
- **2109.08104, 2109.07769, 2107.05906, 2107.00348, 2104.07771, 2005.11961, 2001.01169, 1807.07168, 1802.00034** その他遷移金属/ビスマス系ペロブスカイト

---

## 検索方法（再現可能性メモ）

検索クエリ:
```
"tight binding" perovskite
```
ソース: arXiv 全文検索 (`https://arxiv.org/search/?searchtype=all&query=...`)
結果総数: 74 件（うち 2016 年以降は **49 件**を取得）
取得日: 2026-05-23

PDFは `arxiv.org/pdf/<arxiv_id>.pdf` から直接取得。
