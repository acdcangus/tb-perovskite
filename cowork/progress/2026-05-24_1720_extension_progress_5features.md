# 拡張機能 実装進捗（5 機能） — Claude Code — 2026-05-24 17:20

PI 指示「どんどん実装」に対し、**グラウンディング可能なものから順に実装継続**。全機能 paper-quality + フル V&V +
引用実在確認（記憶ベースの式・数値ゼロ）。

## 実装済み（5 機能, 全 push 済）
| 機能 | モジュール | テスト | 主要 V&V anchor | commit |
|---|---|---|---|---|
| **F1** Berry 曲率→AHC/SHC/Chern | `berry.py` | 22 | Dirac 解析解 / QWZ 整数 Chern / 立方 AHC=0 (1e-15) | `24fa03a` |
| **F2(部分)** Wilson ループ/WCC | `topology.py` | 12 | Wilson Chern == Fukui Chern（2 手法一致） | `981f1f8` |
| **F9** Boltzmann 熱電 | `thermo.py` | 6 | Wiedemann-Franz Lorenz=π²/3 / Sommerfeld Seebeck | `6773898` |
| **F4** Rashba スピン分裂 | `rashba.py` | 8 | 解析 Rashba α_R 厳密回復 / 立方→0 / 極性→≠0 | `188d28d` |
| **F11** Edelstein 効果 | `edelstein.py` | 4 | 中心反転→0 / Rashba 直交 χ / 符号反転 | （本コミット） |

新規テスト計 **52**。引用 **9 件すべて web 実在確認**（Xiao2010・Fukui2005・Sinova2015・QWZ2006・Yu2011・
SoluyanovVanderbilt2011・MadsenSingh2006・BychkovRashba1984・Niesner2016・Edelstein1990）。
Berry 曲率は ar5iv で **Eq.(1.13) 本文確認**。

## テーマ的まとまり
F1/F2/F4/F11 = **Berry 位相・スピン軌道輸送**、F9 = **熱電** — 既存 velocity operator 上に構築した一貫パッケージ。
相互再利用: F2←F1（link 変数）、F4←F1（spin ops）、F11←F4+F9+F1（spin texture + Fermi 窓 + spin ops）。

## 未実装（具体的ブロッカー付き — ハルシネーション回避でスキップ, PI 指示準拠）
| 機能 | ブロッカー |
|---|---|
| F2 残（Fu-Kane parity Z₂ / 時間反転 Z₂） | 反転演算子の基底表現が in-repo 未確定 / 検証用 3D-Z₂ 模型なし |
| F3 BSE 励起子 | 4–6 週規模（TB Coulomb 行列 + model dielectric） |
| F5 2D RP slab / F13 stack / F14 電場 | slab 構築が大規模; F13/F14 は F5 依存 |
| F6 Polaron 移動度 | 材料別 ε_s・ω_LO（LO フォノン）の文献値が必要 → 記憶投入は捏造リスク。要一次収集 |
| F7 CPGE / F8 SHG | injection-current / χ⁽²⁾ の式が intricate → 原典（Sipe-Shkrebtii 等）の式を精読してから実装すべき（sign/factor 捏造リスク） |
| F12 strain | 変形ポテンシャル文献値が必要 |

## 標準ルール準拠
全機能で `.steering/` + `docs/numerical-methods.md`（§9–§13）+ `docs/repository-structure.md` 更新、SPDX、honest 限界記述
（SHC/Rashba/Edelstein の絶対値はベンチ材料なく未検証 + Blount 限界 → 対称性・構造・相対のみ信頼）を既存流儀と統一。

## 次の方針
残機能は「大規模実装」「材料別データ一次収集」「原典の式精読」のいずれかが前提。同じ規律（DOI 検証→原典式確認→
解析/既知模型で V&V→docs/steering）で順次着手可能。F7 CPGE は原典式を fetch 精読すれば次に着手しやすい。
