# design — F12 bandengr.py

## モジュール構成 `src/perovskite_tb/bandengr.py`
- `strained_hopping_params(params, eps)`: Harrison d⁻²: t_* → t_*(1+ε)⁻²（オンサイト/SOC 不変）。
- `gap_at_R(params, a, n_occ)`: R 点ギャップ E[n_occ]−E[n_occ−1]。
- `gap_under_hydrostatic_strain(params, a, eps, n_occ)`: 一様歪み下の R 点ギャップ。
- `hydrostatic_deformation_potential(params, a, ...)`: a_g=dE_g/dε（中心差分）。
- **【追加 T1-2】** `pressure_coefficient(params, a, B)`: a_g → dE_g/dP[meV/GPa]（B=体積弾性率, dP/dε=−3B）。

## 設計判断（honest）
- R 点では Bloch 位相が π 固定 → 歪み応答は Harrison ホッピング繰り込みのみ。
- cubic-frozen TB は **octahedral tilting なし** → ボンド長寄与のみ捉える → 絶対 a_g は過大評価（符号は正しい）。
