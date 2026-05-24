# requirements — F5 / F13 / F14-A 有限 z スラブ・超格子・Stark

**発行元:** `extention/03_tb-perovskite_spec.md` F5 + F13 + F14（モード A）
**日付:** 2026-05-24
**PI 認可:** 実装規模が問題なものは現実時間でできるなら実装。

## スコープ
- F5: 2D RP 量子閉じ込め（open スラブ E_g(N)）。
- F13: 周期スタック（ミニバンド、3D 極限）。
- F14-A: Stark スラブ（z 電場 scalar potential）。
- F14-B（バルク Berry 位相分極, KSV）は未実装（別途）。

## 手法・引用（実在確認済み 2026-05-24, web）
| 文献 | 用途 | 確認 |
|---|---|---|
| Smith-Mailhiot, RMP 62, 173 (1990) | 超格子 TB | ✅ |
| Even-Pedesseau-Katan, **ChemPhysChem 15, 3733 (2014)** | 2D RP 量子閉じ込め（spec の JPCC 118,11566 は誤帰属→訂正） | ✅ |
| Blancon et al., Science 355, 1288 (2017) | E_g(n) | spec 既出 |
| Kopteva 2026 arXiv:2605.15807 | g(n) 実験 | in-repo |
| Neugebauer-Scheffler, PRB 46, 16067 (1992) | F14 scalar potential | spec 既出 |

層分解: ゲージ変換 U=diag(e^{-ik_z z_α})（X_z は z=a/2, 軌道 index 10-12; _HALIDE_BLOCK[2]=10）で 2π/a 周期化 → FFT で H∥, T。

## 受け入れ条件（model-internal で厳密）
- 層ブロック再構成 H∥+T e^{ik_z a}+h.c. == 3D H（機械精度）。
- 周期スタック == 3D バンド（k_z=2πm/(Na)）。
- ミニバンド崩壊（inter-layer→0）。
- open スラブのギャップ収束（バルク極限）。
- Stark: E=0 回復 + 幅 ~eE(N-1)a。
- 既存テスト不変。

## honest 限界
spacer は hard barrier（open BC）理想化。E_g(n) 絶対値は SK-TB/Blount caveat。F14-B 未実装。

## 結果
- `src/perovskite_tb/slab.py` + `tests/test_slab.py`（7 ケース, green）。docs §17, repository-structure 更新。
