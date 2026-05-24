# tasklist — F4 rashba.py

## 実装 ✅
- [x] `spin_texture`, `doublet_splitting`, `rashba_coefficient`, `analytic_rashba_builder`

## V&V ✅（`tests/test_rashba.py`, 9 ケース）
- [x] 解析 2バンド Rashba で α_R 厳密回復, spin ⊥ k
- [x] 立方 CsBX₃ → 分裂 0（Kramers, <1e-6）
- [x] 極性 CsPbI₃ → 分裂発生, Γ で 0, |k| で増大
- [x] 【T2-1】バルク DFT 比較: CBM>VBM 順序一致（C）, 絶対値 ~40×小（D）

## docs ✅
- [x] `docs/numerical-methods.md` §12
## commit ✅ — push 済
## honest 限界
- 絶対 α_R は D（剛体変位 + Blount, ~40× 過小）。表面 Rashba（Niesner ~11 eVÅ）は別系で除外。
- バルク DFT 比較（Bhumla 2021 CsPbF₃）は `.steering/20260524-additional-validation/` で実施。
