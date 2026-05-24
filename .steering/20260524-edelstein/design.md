# design — F11 edelstein.py

## モジュール構成 `src/perovskite_tb/edelstein.py`
- `edelstein_susceptibility(energies, spin_a, velocity_b, mu, T)`:
  χ_{ab}/(eτ) = −(1/N_k) Σ (−∂f/∂E) ⟨S_a⟩ v_b（CRTA Fermi 面平均, Edelstein 1990）。
- `band_data_polar_kashikar13(kpts, params, a, disp, spin_axis, vel_axis)`:
  極性 Kashikar から (E, ⟨S⟩, v) を組み立て（`shift_current.make_polar_kashikar13_builders` 再利用）。
- **【追加 T2-4】** `longitudinal_conductivity`（σ_bb/(e²τ)）, `edelstein_ratio`（τ非依存効率 χ/σ）。

## 設計判断
- `thermo._minus_dfde`（T はケルビン, kT=k_B T）・`berry.spin_operators`・`rashba.spin_texture` を再利用。
- 立方は全k Kramers 縮退 → per-band は gauge 依存 → **極性 P4mm（非縮退）**で評価。絶対 χ は τ 依存で D（/eτ で返す）。比 χ/σ は τ がキャンセル。
