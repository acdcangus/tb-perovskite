# design — F9 thermo.py

## モジュール構成 `src/perovskite_tb/thermo.py`
- `_minus_dfde(egrid, mu, T)`: −∂f/∂E（数値安定 sech² 形, T はケルビン）。
- `transport_distribution(energies, vx, egrid, eta)`: CRTA 輸送分布 Σ_xx(ε)（Gaussian δ, チャンク化ベクトル演算）。
- `transport_coefficients(egrid, Sigma, mu, T)`: L⁰/L¹/L² → σ/τ, Seebeck(k_B/e 単位), κ_e/τ, Lorenz 数。
- `band_group_velocities_kashikar13(kpts, params, a, alpha)`: コアTB群速度。

## 設計判断
- CRTA（定緩和時間）。絶対 σ/κ/S は τ 依存でスコープ外 → 相対値 + 比（Lorenz, Seebeck）。
- 厳密 anchor: Wiedemann-Franz（普遍定数, バンド非依存）+ Sommerfeld（解析 Σ=ε^{3/2}）。Madsen-Singh BoltzTraP 流。
