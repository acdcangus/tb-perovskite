# tasklist — F2 topology.py

## 実装 ✅
- [x] `wilson_loop`, `wannier_charge_centers`, `polarization_phase`, `chern_from_wcc`
- [x] 【T2-2】`parity_delta_at_trim`, `z2_invariant_from_parities`（Fu-Kane parity Z₂）

## V&V ✅（`tests/test_topology.py`, 18 ケース）
- [x] QWZ で Wilson Chern == Fukui Chern（2手法一致, 整数）, 相図, unitary 性, gauge 不変, WCC∈(−½,½]
- [x] 【T2-2】Wilson-Dirac 模型で TRIM パリティ = −sign(M), 強指数 ν₀ が解析相図（1<|m₀|<3 で STI）再現
- [x] 【T2-2】Berry 曲率の質量符号反転（機械精度）

## docs ✅
- [x] `docs/numerical-methods.md` §10（Fu-Kane parity 追加, 引用 Fu-Kane PRB76,045302 / Fu-Kane-Mele PRL98,106803）
## commit ✅ — push 済
## honest 限界 / deferred
- 実ペロブスカイト Z₂ は**反転演算子（Kashikar基底）未確定**で保留（捏造せず）。手法は準備済 → 演算子確定で即適用可。
- T2-2 の詳細は `.steering/20260524-additional-validation/`。
