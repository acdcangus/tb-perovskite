# Theme I — 有効質量マップ Production 完了（option a）— 2026-05-24 07:15

Cowork patrol 0055 §7 の自走サンクション + (a)+(c) 推奨に基づき、**option (a)（有効質量マップ Production 化）を実行**。
PI 判断不要の信頼可部分を先に確定。

## 完了
- **bundle**: `results/production/theme_I_exciton/2026-05-23_f66690c/`（git_dirty:false, runtime 3s）。
- script `scripts/scan_exciton_9materials.py`（convergence/scan/production, layer-2 polling hook 入り）, commit `c550ddf` まで。
- 報告書 `cowork/reports/theme_I_exciton_binding.md`。

## 一次成果（信頼可）: 有効質量マップ
- 9 材料の m_e, m_h, μ（R 点曲率, TB 由来）。**dk <1% 収束、[100]/[110]/[111] 等方性確認**。
- CsPbI₃ m_e=0.106/m_h=0.134（文献整合）。Cl→Br→I で軽量化、CsSnI₃ 最軽（μ=0.015）。

## 二次（相対のみ）: E_b
- E_b 相対トレンド（Cl→Br→I 減、Sn-I 最小）は bundle key_numbers に `_E_b_rel_meV` として収録、
  **絶対値は無効**と明記（TB-optical ε_∞ が Blount 過小、Cl 破綻）。

## ★ 残: option (c) は PI 判断待ち
絶対 E_b には外部（実験/DFT-RPA）ε_∞ が必要。**(c) を実行するか、(a)+(b) で確定とするかは PI 判断**。
- (c) を実行する場合: 9 材料の ε_∞ 文献値を出典付きで収集（Sn/Ge は文献少なめ、要慎重）→ 別 bundle で E_b 絶対化。
- ハルシネーション回避のため、ε_∞ 外部値は私が勝手に値を入れず、出典確認できたものだけ使う。

PI の指示があるまでは Theme I を (a) 完了として保留。5 分巡回で cowork/ を継続確認します。
