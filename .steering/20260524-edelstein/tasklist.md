# tasklist — F11 edelstein.py

## 実装 ✅
- [x] `edelstein_susceptibility`, `band_data_polar_kashikar13`
- [x] 【T2-4】`longitudinal_conductivity`, `edelstein_ratio`

## V&V ✅（`tests/test_edelstein.py`, 6 ケース）
- [x] 中心反転（非縮退）→ χ=0（機械精度）
- [x] Rashba → χ_yx≠0, χ_xx≪χ_yx（直交）, χ_yx(−α)=−χ_yx(α)
- [x] 極性 CsPbI₃ 実行整合
- [x] 【T2-4】χ_yx/σ_xx = mα/(4μ)（2D Rashba 解析, 15%以内, α=0.05で3.6%）, χ_xx/σ≈0, α線形
- [x] 【T2-4】極性 CsPbI₃ τ非依存効率 有限

## docs ✅
- [x] `docs/numerical-methods.md` §13
## commit ✅ — push 済
## follow-up
- T2-4（χ/σ 比）は `.steering/20260524-additional-validation/` で実施・記録。
- 絶対 χ は D（τ 依存・Blount）。
