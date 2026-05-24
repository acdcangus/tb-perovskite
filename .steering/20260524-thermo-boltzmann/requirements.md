# requirements — F9 Boltzmann 熱電輸送（CRTA）

**発行元:** `extention/03_tb-perovskite_spec.md` F9
**日付:** 2026-05-24
**依存:** 既存 bandstructure / velocity（群速度）。berry.velocity_matrix を再利用。

## スコープ
- 定緩和時間近似 (CRTA) の Seebeck S・電気伝導 σ/τ・電子熱伝導 κ_e/τ・Lorenz 数。
- 絶対値（τ 依存）はスコープ外 → 相対値 + 比（Lorenz, Seebeck の k_B/e 単位）のみ。

## 引用（実在確認済み 2026-05-24, web）
| 文献 | 確認 |
|---|---|
| Madsen, Singh, Comp. Phys. Commun. 175, 67 (2006), DOI 10.1016/j.cpc.2006.03.007 (arXiv:cond-mat/0602203) — BoltzTraP | ✅ |

## 受け入れ条件（厳密 anchor, バンド非依存）
- **Wiedemann-Franz**: 縮退極限で Lorenz 数 → π²/3 (k_B/e)²（解析 Σ=ε^{3/2} で rtol 0.5%）。
- **Sommerfeld Seebeck**: S ≈ −(π²/3)(k_B T) dlnΣ/dε|_μ、放物バンドで符号・大きさ一致。
- 正孔 S>0、σ/κ_e>0、Σ ビルダ ε^{3/2} 形状、立方 CsPbI₃ 実行整合。
- 既存テスト不変（271 passed = 265 + 6）。

## 結果
- `src/perovskite_tb/thermo.py` + `tests/test_thermo.py`（6 ケース, 全 green）。
- docs/numerical-methods.md §11, repository-structure.md 更新。
- 設計上の注意（記録）: WF/Seebeck の数値検証は k サンプリング由来の解像度問題（Fermi 窓 ≪ グリッド間隔）を避けるため、**解析 Σ=ε^{3/2} に対して transport_coefficients を単体検証**（Σ ビルダは別途形状検証）。
