# design — F2 topology.py

## モジュール構成 `src/perovskite_tb/topology.py`
- `wilson_loop(occ_line)`: 非アーベル Wilson ループ（重なり行列を SVD 極分解で unitary 化, Yu 2011）。
- `wannier_charge_centers(W)`: 固有位相/2π = WCC（(−½,½]）。
- `polarization_phase(W)`: Im ln det W（U(1) Berry 位相）。
- `chern_from_wcc(occ_grid)`: 分極位相の巻き付き = Chern（符号は Fukui/Xiao 規約に整合）。
- **【追加 T2-2】** `parity_delta_at_trim(H_trim, parity_op, n_occ)`, `z2_invariant_from_parities(deltas)`: Fu-Kane parity Z₂。

## 設計判断（honest）
- 当初スコープ: Wilson/WCC/Chern のみ（QWZ で検証）。Fu-Kane parity と TR-Z₂ は**反転演算子/3D-Z₂参照模型が無い**ため保留（捏造防止）。
- 【T2-2】Fu-Kane parity は**手法として**実装し、標準 Wilson-Dirac (BHZ型) 模型で検証。実ペロブスカイト適用は反転演算子（Kashikar基底）未確定で引き続き保留。
