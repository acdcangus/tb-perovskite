# 拡張機能 実装進捗（6 機能） — Claude Code — 2026-05-24 18:10

PI 指示「すすめて／どんどん実装」に対し、**グラウンディング + 厳密 V&V が確立できる機能から順に**実装継続。

## 実装済み（6 機能, 全 push 済, 新規テスト 56, 全 287 passed）
| 機能 | モジュール | テスト | 厳密 V&V アンカー | commit |
|---|---|---|---|---|
| **F1** Berry 曲率→AHC/SHC/Chern | `berry.py` | 22 | Dirac 解析解 / QWZ 整数 Chern / 立方 AHC=0 (1e-15) | `24fa03a` |
| **F2(部分)** Wilson ループ/WCC | `topology.py` | 12 | Wilson Chern == Fukui Chern（2 手法一致） | `981f1f8` |
| **F9** Boltzmann 熱電 | `thermo.py` | 6 | Wiedemann-Franz Lorenz=π²/3 / Sommerfeld Seebeck | `6773898` |
| **F4** Rashba スピン分裂 | `rashba.py` | 8 | 解析 Rashba α_R 厳密回復 / 立方→0 / 極性→≠0 | `188d28d` |
| **F11** Edelstein 効果 | `edelstein.py` | 4 | 中心反転→0 / Rashba 直交 χ / 符号反転 | `b3e2b99` |
| **F7** CPGE / injection current | `cpge.py` | 4 | de Juan 式簡約 / 中心反転→0 / **Weyl 量子化プラトー+chirality+|Tr|≈1/(4π)** | `92b2ac5` |

引用 **14 件すべて web 実在確認**。式は原典精読でグラウンディング（Berry 曲率 Xiao Eq.1.13 / CPGE de Juan を ar5iv で確認）。
記憶ベースの式・数値はゼロ。一貫した「Berry 位相・スピン軌道輸送・熱電」パッケージで、既存 velocity operator 上に構築・相互再利用。

## 未実装（具体的ブロッカー — ハルシネーション絶対禁止のため、満たせない前提があるものは未着手）
| 機能 | ブロッカー（着手に必要な前提） |
|---|---|
| F2 残（Fu-Kane parity Z₂ / 時間反転 Z₂） | 反転演算子の基底表現が in-repo 未確定 / 検証用 3D-Z₂ 模型なし |
| F3 BSE 励起子 | 4–6 週規模（TB Coulomb 行列 + model dielectric） |
| F5 2D RP slab / F13 stack / F14 電場 | slab 構築が大規模; F13/F14 は F5 依存 |
| **F6 Polaron 移動度** | 材料別 ε_static・ω_LO（LO フォノン）の**文献値**が必要。α 公式の SI 前因子はベンチ材料の published 値で検証すべき → 値の出典確保が前提 |
| **F8 SHG (χ⁽²⁾)** | Aversa-Sipe χ⁽²⁾ は多項で intricate。cubic→0 以外の定量検証が確立しにくい（2 バンド解析 χ² の導出が必要） |
| F12 strain | 変形ポテンシャル文献値 + Harrison スケーリング仮定の妥当性確認が必要 |

## 標準ルール準拠
全 6 機能で `.steering/`（各 requirements）+ `docs/numerical-methods.md` §9–§14 + `docs/repository-structure.md` 更新、
SPDX、honest 限界記述（SHC/Rashba/Edelstein/CPGE の絶対値はベンチ材料/規約依存で未確定 → 対称性・構造・量子化・相対のみ信頼 + Blount 限界）を既存流儀と統一。

## 次の選択肢（PI 判断）
残機能は「(a) 大規模実装（F3/F5/F13/F14）」「(b) 材料別データ一次収集（F6/F12）」「(c) 原典 χ² 精読 + 2 バンド解析検証（F8）」のいずれかが前提。
- **F6/F12** は ε_static・ω_LO・変形ポテンシャル等の値の出典をいただければ（or OA 収集を許可いただければ）着手可。
- **F8** は Aversa-Sipe χ² を精読し 2 バンド解析で検証してから実装可。
いずれも同じ規律（DOI 検証 → 原典式精読 → 解析/既知模型/量子化で V&V → docs/steering）で進めます。
