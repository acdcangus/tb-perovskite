# design — F14-B polarization.py

## モジュール構成 `src/perovskite_tb/polarization.py`
- `zak_phase(occ_loop)`: 占有多様体の Berry/Zak 位相（`topology.wilson_loop` 再利用）。
- `occupied_along_kz(params, a, kx, ky, n_occ, n_kz)`: ゲージ固定 H の k_z 沿い占有固有ベクトル。
- `polarization_phase_z(params, a, ...)`: 横BZ平均 Zak 位相（電子 P_z, mod 2π）。
- **【追加 T2-3】** `_occupied_along_kz_builder`（任意ビルダ）, `ferroelectric_polarization_difference`（電子 ΔP_z=(e/2πA)(φ(d)−φ(0)) μC/cm²）。

## 設計判断（honest）
- 返すのは**電子 Berry 位相のみ**。物理量子化分極はイオン寄与 + 分極量子が必要（total のみ gauge 不変）。
- 立方の裸の電子 Zak は X_z(z=a/2) のゲージオフセットで 0/π にならない → 量子化は SSH で検証、用途は **ΔP（gauge 不変な差）**。
- ΔP も電子寄与のみ → 符号反転と参照ゼロを主張、定量一致は非主張。
