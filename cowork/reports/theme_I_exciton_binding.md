# Theme I: 立方晶 CsBX₃ の有効質量マップと Wannier-Mott 励起子結合エネルギー

**ステータス:** 一次成果（有効質量マップ）Production 完了。E_b は相対トレンドのみ（絶対値は ε_∞ 較正待ち = option c, PI 判断）。
**bundle:** `results/production/theme_I_exciton/2026-05-23_f66690c/`（dirty:false）。

---

## 1. 動機
ハライドペロブスカイトの励起子結合エネルギー E_b は LED・太陽電池設計で重要（E_b 大 → 励起子発光が明るい）。
既存 TB から **バンド端有効質量** を出し、**Wannier-Mott 水素様模型** で E_b を推定する：
`E_b = (μ/m₀)/ε_r² × Ry（13.6057 eV）`、`1/μ = 1/m_e + 1/|m_h|`。

## 2. 方法
- **有効質量（一次成果, TB 由来・信頼可）**: R 点（直接ギャップ端, π/a(1,1,1)）でバンド曲率
  `m*/m₀ = (ℏ²/m₀)/(d²E/dk²)`、ℏ²/m₀=7.619964 eV·Å²。中央差分、3 方向平均。Kashikar-13, n_occ=20。
- **ε_∞**: Phase 1.5 の TB-optical（Kubo-Greenwood + KK）の `eps_real[0]`。
- 実装: `src/perovskite_tb/exciton.py`、scan: `scripts/scan_exciton_9materials.py`。

## 3. 主要結果

| 材料 | m_e | m_h | μ | ε_∞(TB) | E_b(rel, meV) |
|---|---|---|---|---|---|
| CsGeCl₃ | 0.228 | −0.168 | 0.097 | 2.51 | 210 |
| CsGeBr₃ | 0.148 | −0.101 | 0.060 | 3.70 | 60 |
| CsGeI₃ | 0.111 | −0.100 | 0.053 | 4.67 | 33 |
| CsSnCl₃ | 0.177 | −0.110 | 0.068 | 2.31 | 173 |
| CsSnBr₃ | 0.075 | −0.050 | 0.030 | 3.42 | 35 |
| CsSnI₃ | 0.035 | −0.025 | 0.015 | 4.70 | 9 |
| CsPbCl₃ | 0.237 | −0.225 | 0.116 | 1.45 | 743 ⚠ |
| CsPbBr₃ | 0.151 | −0.144 | 0.074 | 2.35 | 182 |
| CsPbI₃ | 0.106 | −0.134 | 0.059 | 3.46 | 67 |

### 一次成果: 有効質量マップ（信頼可・publishable）
- **CsPbI₃ m_e=0.106, m_h=0.134** は文献（~0.1–0.15 m₀）と整合。
- 質量は **Cl→Br→I で軽くなる**（gap 減少と整合）、**Sn 系が最軽量**（CsSnI₃ μ=0.015、超分散バンド）。
- **立方点群どおり等方的**（[100]/[110]/[111] で同一、検証済み）。

### 二次（相対トレンドのみ）: E_b
- E_b は **Cl→Br→I で減少**、**Sn-I が最小（9 meV）**、Pb/Ge-Cl が最大。LED 観点: 大 E_b（広 gap Cl）ほど励起子発光が明るい傾向。

## 4. 検証
- **dk 収束**: m_e 0.107→0.106（dk 0.01→0.001）, m_h −0.135→−0.134。<1% 収束（`convergence/effmass_convergence.csv`）。
- **方向異方性**: [100]/[110]/[111] で機械精度一致（cubic 等方性確認）。
- 合成放物線で m* 厳密回復・CsPbI₃ で m_e>0/m_h<0、公式の算術（`tests/test_exciton.py`, 3 通過）。

## 5. 限界（★ E_b 絶対値は信頼不可）
- **絶対 E_b は実験を ~3–4× 過大評価**（CsPbI₃ 67 meV vs 実験 ~15–20 meV）。原因 2 つ:
  1. **物理**: Wannier-Mott の正しい遮蔽は ε_∞ と ε_static の中間（フォノン寄与）。ε_∞ 単独は上限。
  2. **数値**: TB-optical の ε_∞ は **f-sum=0.21（Blount で 5× 過小）**を継承 → ε_∞ 過小 → E_b 過大。
     **広 gap Cl で破綻**（CsPbCl₃ ε_∞=1.45 は非物理＝実測 ~3–4、E_b 743 meV は無効）。
- **→ E_b は相対トレンドのみ論じる**。有効質量マップは TB 由来で完結・信頼可。
- **option (c)（PI 判断待ち）**: 絶対 E_b には **実験/DFT-RPA の ε_∞ を外部入力**し、出典を MANIFEST に明記して
  Production 化（ε_∞ 由来系統誤差を Theme I から切り離す）。Cowork patrol 0055 §5 推奨。

## 6. 再現
```bash
OMP_NUM_THREADS=1 PYTHONPATH=src python scripts/scan_exciton_9materials.py production
PYTHONPATH=src python -m pytest tests/test_exciton.py -q
```

## 7. 関連ファイル
- 実装: `src/perovskite_tb/exciton.py`、scan: `scripts/scan_exciton_9materials.py`、test: `tests/test_exciton.py`
- bundle: `results/production/theme_I_exciton/2026-05-23_f66690c/`（MANIFEST.json）
- 出典: Yang 2017 PRB 96 035301 / Tanaka 2003 SSC 127 619 / Cho 2019 (arXiv:1908.09436) / Kashikar 2021 (arXiv:2101.08562)
