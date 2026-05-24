# design — F4 rashba.py

## モジュール構成 `src/perovskite_tb/rashba.py`
- `spin_texture(evecs, s_op)`: ⟨n|S|n⟩。
- `doublet_splitting(H, band_index)`: E[b+1]−E[b]（Kramers doublet 分裂）。
- `rashba_coefficient(H_fn, band_index, k_mag, axis)`: α_R = ΔE/(2|k|)（線形 k 係数）。
- `analytic_rashba_builder(alpha_R, meff)`: H=(ħ²k²/2m*)I + α_R(k_xσ_y−k_yσ_x)（Bychkov-Rashba 検証用）。

## 設計判断
- 立方は P·T で全k Kramers（α_R=0）。極性は `shift_current.make_polar_kashikar13_builders`（delta=0 で立方と bit 一致）で生成。
- 絶対 α_R は剛体変位 + Blount で過小評価 → 符号/順序のみ主張。
