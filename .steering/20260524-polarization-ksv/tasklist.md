# tasklist — F14-B polarization.py

## 実装 ✅
- [x] `zak_phase`, `occupied_along_kz`, `polarization_phase_z`
- [x] 【T2-3】`_occupied_along_kz_builder`, `ferroelectric_polarization_difference`

## V&V ✅（`tests/test_polarization.py`, 6 ケース）
- [x] SSH: Zak 0/π 量子化 + 転移で π ジャンプ（厳密アンカー）
- [x] Rice-Mele: 反転破れで連続シフト（非量子化）
- [x] ペロブスカイト電子 Zak が finite・実・決定論的
- [x] 【T2-3】ΔP(0)=0, ΔP(−d)=−ΔP(+d)（符号反転）, ~1–8 μC/cm²（DFT と同オーダ）

## docs ✅
- [x] `docs/numerical-methods.md` §18
## commit ✅ — push 済
## honest 限界
- 電子寄与のみ（DFT は total）→ ΔP は符号反転・参照ゼロ・オーダのみ主張。絶対分極は D。
- T2-3 の詳細は `.steering/20260524-additional-validation/`。
