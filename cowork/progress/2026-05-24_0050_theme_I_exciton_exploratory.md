# Theme I（Wannier-Mott 励起子）exploratory 完了 + 要 PI 判断 — 2026-05-24 00:50

2125 nudge の Option B（Theme I）に着手。**module + tests 完了、9 材料 exploratory E_b 算出**。
commit `2a4fe38`。Production 化の前に **ε_∞ の信頼性** で PI 判断を仰ぎたい点あり（§3）。

## 1. 実装（commit 2a4fe38）

- `src/perovskite_tb/exciton.py`: `effective_mass`（R 点バンド曲率 m*/m0 = (ℏ²/m0)/(d²E/dk²)、3 方向平均）、
  `reduced_mass`、`wannier_mott_binding_eV`（E_b=(μ/m0)/ε_r²·Ry）。
- `tests/test_exciton.py`（3 通過）: 合成放物線で m* 厳密回復、CsPbI₃ で m_e/m_h が物理的、公式の算術。

## 2. 9 材料 exploratory 結果（n_kpts=8, ε_∞=optical KK の eps_real[0]）

| 材料 | m_e | m_h | μ | ε_∞ | E_b (meV) |
|---|---|---|---|---|---|
| CsGeCl₃ | 0.228 | −0.168 | 0.097 | 2.51 | 210 |
| CsGeBr₃ | 0.148 | −0.101 | 0.060 | 3.70 | 60 |
| CsGeI₃ | 0.111 | −0.100 | 0.053 | 4.67 | 33 |
| CsSnCl₃ | 0.177 | −0.110 | 0.068 | 2.31 | 173 |
| CsSnBr₃ | 0.075 | −0.050 | 0.030 | 3.42 | 35 |
| CsSnI₃ | 0.035 | −0.025 | 0.015 | 4.70 | **9** |
| CsPbCl₃ | 0.237 | −0.225 | 0.116 | 1.45 | 743 ⚠ |
| CsPbBr₃ | 0.151 | −0.144 | 0.074 | 2.35 | 182 |
| CsPbI₃ | 0.106 | −0.134 | 0.059 | 3.46 | 67 |

- **有効質量は物理的に妥当**（CsPbI₃ m_e=0.11/m_h=0.13 は文献 ~0.1–0.15 と一致）。最も信頼できる出力。
- **トレンドは頑健**: E_b は Cl→Br→I で減少（ε_∞ 増 + 質量軽）。Sn ヨウ化物が最小（9 meV、超軽量質量）。

## 3. ★ 要 PI 判断: ε_∞ の信頼性と絶対 E_b

- **絶対 E_b は実験を ~3–4× 過大評価**（CsPbI₃ 67 meV vs 実験 ~15–20 meV）。理由 2 つ:
  1. **物理的**: Wannier-Mott の正しい遮蔽は ε_∞ と ε_static の中間（フォノン寄与）。ε_∞ のみは上限を与える（spec 通りだが過大）。
  2. **数値的**: 本実装の ε_∞ は **TB-optical の KK eps_real[0]** で、光学テーマの **f-sum=0.21（Blount で 5× 過小）**を継承
     → ε_imag 過小 → ε_∞ 過小 → E_b 過大。特に **広 gap Cl で深刻**（CsPbCl₃ ε_∞=1.45 は明らかに低すぎ＝実測 ~3–4、E_b 743 meV は非物理）。
- **推奨**: (a) **有効質量マップ**は publishable（信頼可）。(b) **E_b は相対トレンドのみ論じる**、または
  (c) Production E_b には **実験/DFT の ε_∞ を外部入力**として使う（TB-optical ε_∞ の Blount 過小を回避）。
  → **PI 判断**: E_b を (b) 相対のみ / (c) 外部 ε_∞ で Production 化 / 有効質量のみ報告、のどれにするか。

## 4. 次

PI 判断待ち。判断あるまでは Production 化を保留（非物理な Cl ε_∞ を bundle しないため）。
有効質量マップだけ先に Production 化することも可能。報告書 `cowork/reports/theme_I_exciton_binding.md` は判断後に確定。
