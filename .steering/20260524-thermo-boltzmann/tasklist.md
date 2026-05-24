# tasklist — F9 thermo.py

## 実装 ✅
- [x] `_minus_dfde`, `transport_distribution`, `transport_coefficients`, `band_group_velocities_kashikar13`

## V&V ✅（`tests/test_thermo.py`, 6 ケース）
- [x] **Wiedemann-Franz**: 縮退極限 Lorenz → π²/3 (k_B/e)²（解析 Σ=ε^{3/2}, rtol 0.5%）— A
- [x] Sommerfeld Seebeck（符号・大きさ）, 正孔 S>0, Σ∝ε^{3/2}
- [x] 立方 CsPbI₃ 輸送 実行整合

## 実装中の修正（記録）
- WF: Fermi 窓 < グリッド分解で数値ばらつき → 解析 Σ=ε^{3/2} で検証し安定化。

## docs ✅
- [x] `docs/numerical-methods.md` §11
## commit ✅ — push 済
## honest 限界
- 絶対 σ/κ_e/Seebeck は D（τ 材料依存）。比・普遍定数のみ A。
