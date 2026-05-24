# requirements — F12 歪みバンド工学（変形ポテンシャル）

**発行元:** `extention/03_tb-perovskite_spec.md` F12
**日付:** 2026-05-24

## スコープ
- 一様歪み下の R 点ギャップ E_g(ε) と変形ポテンシャル a_g=dE_g/dε（SK-TB + Harrison d⁻² スケーリング）。

## 引用（実在確認済み 2026-05-24, web）
| 文献 | 用途 | 確認 |
|---|---|---|
| W. A. Harrison, *Electronic Structure and the Properties of Solids*, Freeman (1980) | ホッピング d⁻² 普遍スケーリング | ✅ |
| Bir, Pikus, *Symmetry and Strain-Induced Effects*, Wiley (1974) | 変形ポテンシャル枠組み | ✅（spec 既出） |
| Buin 2014 / Grumet 2018 | ペロブスカイト歪み文脈 | spec 既出 |

## 受け入れ条件（構造的・模型内で厳密）
- Harrison 則 t_*(1+ε)⁻²、オンサイト/SOC 不変。
- ε=0 で無歪みギャップ（CsPbI₃ 0.6298 eV, theme_F 一致）回復。
- 小 ε で線形、引張/圧縮逆符号、全材料 a_g 有限。
- 既存テスト不変。

## honest 限界
SK-TB + Harrison 推定。a_g 絶対値は近似（DFT-fit TB への Harrison は粗い）→ DFT/実験との定量一致は非主張。
R 点では Bloch 位相が π 固定 → 歪み応答は Harrison ホッピング繰り込み由来。

## 結果
- `src/perovskite_tb/bandengr.py` + `tests/test_bandengr.py`（8 ケース, green）。docs §16, repository-structure 更新。
