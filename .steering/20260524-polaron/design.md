# design — F6 polaron.py

## モジュール構成 `src/perovskite_tb/polaron.py`
- `omega_from_THz` / `omega_from_meV`: LO フォノン角振動数変換。
- `frohlich_alpha(eps_inf, eps_static, omega_LO_rad_s, m_eff_rel)`:
  α = (1/4πε₀)(1/2)(1/ε∞ − 1/ε_S)(e²/ħΩ)√(2m_bΩ/ħ)（Frost 2017, ar5iv 原典確認）。SI 定数（CODATA）。
- `weak_coupling_polaron_mass(alpha)`: m_p/m_b = 1 + α/6（Feynman 弱結合）。

## データ
- `data/parameters/frohlich_polaron_params.json`: cited 誘電/LO/m*（MAPbI₃=Frost, CsPbBr₃=Sendner 2021）。捏造なし。

## 設計判断
- 前因子は **2 独立ベンチ**（Frost MAPbI₃, Sendner CsPbBr₃）で固定。完全 Feynman variational 移動度は intricate→未実装(flag)。
- 【T2-3拡張】m* は本来 literature だが、**コアTB の band 曲率から取得可**（`bandstructure.effective_mass`）→ TB駆動 α へ。
