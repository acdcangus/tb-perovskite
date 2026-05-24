# requirements — F11 Edelstein 効果（電流誘起スピン分極, CRTA）

**発行元:** `extention/03_tb-perovskite_spec.md` F11
**日付:** 2026-05-24
**依存:** `thermo`（Fermi 窓）、`berry.spin_operators`、`rashba.spin_texture`、`shift_current.make_polar_kashikar13_builders`。

## スコープ
- CRTA 線形応答 χ_{ab}（δS_a=χ_{ab}E_b）、絶対値（τ 依存）はスコープ外 → χ/(eτ) を返す。

## 引用（実在確認済み 2026-05-24, web）
| 文献 | 確認 |
|---|---|
| Edelstein, Solid State Commun. 73, 233 (1990), DOI 10.1016/0038-1098(90)90963-C | ✅ |

## 受け入れ条件
- 中心反転（非縮退）模型 → χ=0（機械精度）。
- Rashba 模型 → χ_yx≠0, χ_xx≪χ_yx（直交）、χ_yx(−α)=−χ_yx(α)（符号反転）。
- 極性 CsPbI₃ 実行整合。既存テスト不変。

## 適用範囲（重要・honest）
per-band 公式は**非縮退バンド前提**。立方 Pm-3m は Kramers 縮退で per-band gauge 依存（応答は対称性で 0）→
ペロブスカイトは反転破れ極性 (P4mm) 相で評価する。絶対値は τ 依存でスコープ外。

## 結果
- `src/perovskite_tb/edelstein.py` + `tests/test_edelstein.py`（4 ケース, green）。docs §13, repository-structure 更新。
