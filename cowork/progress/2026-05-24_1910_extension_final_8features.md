# 拡張機能 最終サマリ（8 機能実装） — Claude Code — 2026-05-24 19:10

PI 指示「すすめて／どんどん／自分で収集して優先度もお任せ」に対し、**ハルシネーション絶対禁止 + paper-quality** を
満たせる機能を**自分で優先度決定・データ収集して**実装。spec F1–F14 のうち **8 機能**を完遂。

## 実装済み（8 機能, 全 push 済, 新規テスト 71, 全 302 passed）
| 機能 | モジュール | テスト | 厳密 V&V アンカー | commit |
|---|---|---|---|---|
| **F1** Berry 曲率→AHC/SHC/Chern | `berry.py` | 22 | Dirac 解析解・QWZ 整数 Chern・立方 AHC=0 (1e-15) | `24fa03a` |
| **F2(部分)** Wilson ループ/WCC | `topology.py` | 12 | Wilson Chern == Fukui Chern（2 手法一致） | `981f1f8` |
| **F9** Boltzmann 熱電 | `thermo.py` | 6 | Wiedemann-Franz Lorenz=π²/3・Sommerfeld Seebeck | `6773898` |
| **F4** Rashba スピン分裂 | `rashba.py` | 8 | 解析 Rashba α_R 厳密回復・立方→0・極性→≠0 | `188d28d` |
| **F11** Edelstein 効果 | `edelstein.py` | 4 | 中心反転→0・Rashba 直交 χ・符号反転 | `b3e2b99` |
| **F7** CPGE / injection current | `cpge.py` | 4 | de Juan 式簡約・**Weyl 量子化（プラトー+chirality+|Tr|≈1/4π）** | `92b2ac5` |
| **F6** Fröhlich polaron | `polaron.py` | 7 | **2 独立ベンチ**: MAPbI₃ α=2.39/2.68(Frost)・CsPbBr₃ α≈2(Sendner) | `d0ca915` |
| **F12** 歪みバンド工学 | `bandengr.py` | 8 | ε=0 回復・線形性・Harrison 則・符号 | `e80e7e7` |

引用 **18 件すべて web 実在確認**。主要な式は**原典精読でグラウンディング**（Berry 曲率 Xiao Eq.1.13・CPGE de Juan・polaron Frost を ar5iv で確認）。
データは PI 認可で**自分で OA 収集**（`frohlich_polaron_params.json` に各値出典明記）。記憶ベースの式・数値ゼロ。

## 未実装（具体的ブロッカー — no-hallucination の境界）
| 機能 | ブロッカー |
|---|---|
| **F8 SHG (χ⁽²⁾)** | Aversa-Sipe χ² は interband+intraband+modulation の多項で、clean な定量アンカーが cubic→0 のみ → 2 バンド解析 χ² の導出無しでは「未検証の式を実装」になりかねず保留 |
| **F3 BSE 励起子** | 4–6 週規模（TB Coulomb 行列 + model dielectric の自己整合） |
| **F5 2D RP slab / F13 stack / F14 電場** | slab 構築が大規模; F13/F14 は F5 依存 |
| **F2 残（Z₂）** | 反転演算子の Kashikar 基底表現が in-repo 未確定（推測=捏造）/ 検証用 3D-Z₂ 模型なし |

## 総括
- **既存 velocity operator 上に一貫した「Berry 位相・スピン軌道輸送・熱電・電子格子・歪み」物性スイート**を構築（8 新モジュール）。相互再利用（F7/F4/F11←F1, F11←F9, F12←既存 model）。
- 各機能で `.steering/` + `docs/numerical-methods.md` §9–§16 + `docs/repository-structure.md` 更新、SPDX、honest 限界記述（絶対値が未検証なものは「対称性・構造・量子化・相対のみ信頼 + Blount/規約/近似」と明記）。
- 既存 231 テスト不変、新規 71、計 **302 passed**。
- 残 6 機能は「大規模実装（F3/F5/F13/F14）」「定量検証困難な intricate 式（F8）」「in-repo 未確定の演算子（F2-Z₂）」のいずれかで、**現状の厳密 V&V + 無捏造の基準では着手前提が未充足**。F8 は Aversa-Sipe χ² 精読 + 2 バンド解析検証を経れば、F3/F5 は腰を据えた実装期間を取れば、同じ規律で実装可能。
