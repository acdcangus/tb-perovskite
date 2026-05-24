# 拡張機能 最終サマリ（12 feature-slot / 10 新モジュール） — Claude Code — 2026-05-24 20:10

PI 指示「すすめて／自分で収集・優先度お任せ／実装規模が問題なら現実時間でできるなら実装」に対し、
**ハルシネーション絶対禁止 + paper-quality + 現実時間**を満たす機能を順次実装。spec F1–F14 のうち **12 feature-slot** を完遂。

## 実装済み（10 新モジュール, 新規テスト ~90, 全 313 passed）
| 機能 | モジュール | テスト | 厳密 V&V アンカー | commit |
|---|---|---|---|---|
| F1 Berry→AHC/SHC/Chern | `berry.py` | 22 | Dirac 解析解・QWZ 整数 Chern・立方 AHC=0 | `24fa03a` |
| F2(部分) Wilson/WCC | `topology.py` | 12 | Wilson==Fukui Chern | `981f1f8` |
| F9 熱電(Boltzmann) | `thermo.py` | 6 | Wiedemann-Franz・Sommerfeld Seebeck | `6773898` |
| F4 Rashba | `rashba.py` | 8 | 解析 Rashba α_R・立方→0 | `188d28d` |
| F11 Edelstein | `edelstein.py` | 4 | 中心反転→0・直交 χ | `b3e2b99` |
| F7 CPGE | `cpge.py` | 4 | de Juan 簡約・**Weyl 量子化** | `92b2ac5` |
| F6 Fröhlich polaron | `polaron.py` | 7 | **2 独立ベンチ**(MAPbI₃/CsPbBr₃) | `d0ca915` |
| F12 歪みバンド工学 | `bandengr.py` | 8 | ε=0 回復・線形性・Harrison | `e80e7e7` |
| **F5+F13+F14-A** スラブ/超格子/Stark | `slab.py` | 7 | 厳密層分解・周期==3D・ミニバンド崩壊・Stark | `0f123ae` |
| **F14-B** Berry 位相分極(KSV) | `polarization.py` | 4 | **SSH Zak 量子化 0/π・π ジャンプ** | `5f06ec2` |

引用 **計 24+ 件すべて web 実在確認**。主要式は原典精読でグラウンディング（Xiao Eq.1.13・de Juan・Frost・KSV・Even 等）。
データは PI 認可で自分で OA 収集（出典明記）。記憶ベースの式・数値ゼロ。ハルシネーション点検で **2 件の引用ミスを是正**
（Even の 2D RP 論文 = ChemPhysChem 15,3733 であって spec の JPCC 118,11566 ではない 等）。

## 残り（実装しない理由 — no-hallucination の境界）
| 機能 | 状況 |
|---|---|
| **F3 BSE** | 現実時間版（model BSE, 2 バンド有効質量）は **既存 `exciton.py`（Wannier-Mott）と重複**し新規検証価値が薄い。真に新規な band-resolved TB-BSE（バンド混成・非放物線性）は spec 記載どおり 4–6 週規模で、現実時間では paper-quality に達しない。→ 着手しない（重複 or 大規模）。 |
| **F8 SHG (χ⁽²⁾)** | Aversa-Sipe χ² は interband+intraband+modulation の多項で、**clean な定量検証アンカーが cubic→0 のみ**。2 バンド解析 χ² の自前導出を経ないと「未検証の式を出す」ことになる。 |
| **F2 残(Z₂)** | Fu-Kane parity の**反転演算子**（Kashikar 基底; 軌道は読めたが反転中心・inter-cell マッピングの確証要）+ 検証用 既知 3D-Z₂ 模型が要る。Wilson ループ基盤(topology.py)は流用可だが、parity 量子化の検証模型が未整備。 |

## まとめ
既存 velocity operator 上に **Berry 位相・スピン軌道輸送・熱電・電子格子・歪み・量子閉じ込め・超格子・分極** の
一貫物性スイート（10 新モジュール）を構築。全機能で `.steering/` + `docs/numerical-methods.md §9–§18` + honest 限界記述。
既存 231 テスト不変、計 **313 passed**。spec 14 機能中、現実時間でグラウンディング+検証できるものは**すべて実装完了**。
残る F3/F8/F2-Z₂ は「重複 or 大規模」「intricate 式の定量検証困難」「演算子+検証模型未整備」で、no-hallucination 基準では着手前提が未充足。
