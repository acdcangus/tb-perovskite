# tasklist — F12 bandengr.py

## 実装 ✅
- [x] `strained_hopping_params`, `gap_at_R`, `gap_under_hydrostatic_strain`, `hydrostatic_deformation_potential`
- [x] 【T1-2】`pressure_coefficient`

## V&V ✅（`tests/test_bandengr.py`, 9 ケース）
- [x] Harrison 則 t_*(1+ε)⁻²（オンサイト/SOC 不変）
- [x] ε=0 で無歪みギャップ（CsPbI₃ 0.6298 eV, theme_F 一致）回復
- [x] 線形性, 引張/圧縮逆符号, 全材料で a_g 有限
- [x] 【T1-2】文献比較: 符号一致（加圧で gap 減; Pieniazek 2023, C）/ 大きさ ~5-16×過大（D, tilting欠如）

## docs ✅
- [x] `docs/numerical-methods.md` §16
- [x] 引用訂正: Buin 2014（trap論文）/ Grumet PRB98,155143（GW手法論文）削除 → Pieniazek 2023 + Liu 2023(B) 採用
## commit ✅ — push 済
## honest 限界
- 絶対 a_g は D（cubic-frozen, tilting なし, Harrison 粗さ）。符号は C（実験一致）。
- T1-2 の詳細は `.steering/20260524-additional-validation/`。
