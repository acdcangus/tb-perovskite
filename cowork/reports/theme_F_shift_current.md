# Theme F: 立方晶 CsBX₃ の shift-current バルク光起電力効果（BPVE）

**ステータス:** F1–F6 完了。F4 で符号・手法確定、F5 Production（9 材料 × δ, n_kpts=48）完了。
主結果: **鉛フリー Sn/Ge ハライド（特にヨウ化物）が Pb 系より大きい shift current**。
**モデル:** Kashikar-13 経験 TB（9 材料）/ Nestoklon（CsPbI₃ クロスチェック）。
**主成果（手法）:** tight-binding shift current の一般化微分に **Fregoso 2017 Eq.(C2) の第2微分 w 項が必須**であることを
Rice-Mele 閉形式で実証し、符号・prefactor を in-repo 一次出典に anchor した。

---

## 1. 動機と問い

- **shift current / BPVE**: 反転対称が破れた単相結晶で、バンド間遷移時の波動関数の実空間「シフト」により
  生じる二次の直流光電流（von Baltz-Kraut 1981, Young & Rappe 2012）。p-n 接合不要・above-gap 電圧可能。
- **主問い（F5）:** 立方 CsBX₃（B=Ge/Sn/Pb, X=Cl/Br/I）に [001] 極性変位を入れたとき、
  **鉛フリー（Sn/Ge）で shift current σ_zzz が大きい組成があるか**（毒性 Pb 代替の光起電ポテンシャル）。

## 2. 方法

### 2.1 支配方程式（velocity gauge, sum-over-states）
σ_zzz(ω) = (1/N_k) Σ_k Σ_{v∈occ, c∈unocc} Im[ r^z_cv · r^z_{vc;z} ] · δ(E_cv − ℏω)（Lorentzian 幅 η）。
r^z_cv = 干渉性 Berry connection、r^z_{vc;z} = 一般化（共変）微分。

### 2.2 ★ TB 一般化微分は Fregoso Eq.(C2) の w 項が必須（本テーマの手法的核心）
```
r^a_{vc;a} = -(1/(i ω_vc)) [ 2 v^a_vc Δ^a_vc/ω_vc − w^{aa}_vc
                            + Σ_{p≠v,c} v^a_vp v^a_pc (1/ω_pc − 1/ω_vp) ]
```
- `w^{aa}_vc = ⟨v|∂²H/∂k_a²|c⟩`（速度演算子の第2 k 微分の off-diagonal 成分）。
- Fregoso 2017（arXiv:1701.00172）が Eq.(C2) 直後に明記するとおり、連続模型 `H=p²/2m+V` では w は対角で
  off-diagonal 寄与ゼロ（= 標準 Sipe-Shkrebtii 形）。**TB では ∂²H/∂k² が off-diagonal を持つため w 項が効く。**
  この項を落とすと **2-band では σ が恒等的に 0**（§4-A）。Kramers(SOC) 縮退は縮退中間状態スキップで処理。

### 2.3 symmetry breaker と歪み
- 立方 Pm-3m は中心対称 → σ⁽²⁾=0。**B カチオン [001] 極性変位 δ（→ P4mm 非中心対称）**で破る。
- B-X_z 結合のみ非対称化（+z: a/2−δ, −z: a/2+δ）、ホッピングは Harrison 距離則 `t∝d⁻²`（η=2.0）でスケール。
- δ=0 で σ=0 を機械精度で検証（中心対称消失）。

### 2.4 計算条件（F5 Production）
Kashikar-13、n_occ=20（B-s² + 3·X-p⁶）、n_kpts=48、η=0.10 eV、ω∈[0.3,5.0] eV、δ∈{0.10,0.15,0.20} Å。
single-thread BLAS（性能上必須）。3 段収束: k=24/32/48, η=0.05/0.08/0.15, ω 分解能=150/300/600。

## 3. 主要結果（F5 Production, n_kpts=48, η=0.10, δ=0.15, 相対単位）

bundle: `results/production/theme_F_shift_current/2026-05-23_ef575e3/`。δ=0 で σ_zzz=6.9e-15（中心対称消失）。

| 材料 | gap@R (eV) | ピーク σ_zzz (rel) | ピーク ω (eV) | ∫_[Eg,2Eg] (rel) |
|---|---|---|---|---|
| **CsSnI₃** | 0.175 | **−3.43** | 1.64 | −0.017* |
| **CsGeI₃** | 0.640 | **−2.67** | 1.73 | −0.63 |
| CsSnBr₃ | 0.383 | −1.31 | 2.19 | −0.074* |
| CsGeBr₃ | 1.031 | +1.30 | 4.01 | −0.34 |
| CsPbI₃ | 0.630 | +0.97 | 3.96 | −0.24 |
| CsGeCl₃ | 1.767 | +0.66 | 5.00† | −0.36 |
| CsSnCl₃ | 1.056 | −0.44 | 2.94 | −0.14 |
| CsPbBr₃ | 1.100 | −0.31 | 2.74 | −0.14 |
| CsPbCl₃ | 2.127 | −0.11 | 4.87 | −0.13 |

### ★ 主結果: 鉛フリー（Sn/Ge）ハライドが Pb 系より大きい shift current
- **ピーク |σ_zzz| は CsSnI₃ > CsGeI₃ > CsSnBr₃ ≈ CsGeBr₃ > CsPbI₃ の順**。
  鉛フリー Sn/Ge のヨウ化物・臭化物が **Pb 同族（CsPbX₃）をすべて上回る**（CsPbI₃ を除く全 Pb 系は |σ|<0.5）。
  → **主問いの答え: YES。毒性 Pb の代替として Sn/Ge ペロブスカイトは BPVE 的に有望。**
- **σ はバンドギャップと逆相関**（小 gap → 大 σ; エネルギー分母 1/E_cv² 由来、Tan&Rappe 2016 の観察とも整合）。
  Sn/Ge は Pb より gap が小さく（特に I 系）、これが大 σ の主因。
- **符号**: I/Br 系の多くで σ_zzz<0（極性変位 +z に対し）。CsGeBr₃/CsGeCl₃/CsPbI₃ は +。
  符号は組成依存（バンド対称性の詳細）で、F4-3/F4-2 で確立した符号規約に基づく確定値。

### 注意（メトリクスの解釈）
- `*` **[Eg,2Eg] ω 積分は極小 gap 材料（CsSnI₃ 0.175 eV, CsSnBr₃ 0.38 eV）を過小評価**:
  これらの主ピーク（1.6–2.2 eV）は 2Eg より遥か上にあり、狭い band-edge 窓 [Eg,2Eg] が捉えない。
  → **ピーク強度が小 gap 材料には適切な指標**。band-edge 積分は中 gap 材料（CsGeI₃ −0.63 が最大）を反映。
- `†` CsGeCl₃ のピークは ω=5.0 eV（窓端）にあり、真のピークは >5 eV の可能性（広 gap のため高エネルギー側）。
- **収束**: k 32→48 で L2rel=1.4%、ω 分解能は完全収束。n_kpts=24↔48 で順位不変（CsGeI₃ −2.65→−2.67）→ **順位は頑健**。
- CsPbI₃ は δ により主ピーク位置が 3.96→1.93 eV に切替（2 つの競合ピーク）。

図: `outputs/figures/sigma_zzz_9materials.png`、全数値: `outputs/raw/peak_summary.csv` + `MANIFEST.json key_numbers`。

## 4. 検証（V&V — 完了）

### ★ A. F4-3 Rice-Mele 解析閉形式（符号・prefactor 確定）
Fregoso 2017 Appendix D の 1D Rice-Mele 模型に対し、per-k 積分核が **Eq.(D15) `Im[r^z_cv r^z_vc;z]=a³tδΔ/(32E³)`
と全 k で rel<1e-7 一致**（符号・magnitude とも）。full σ_zzz(ω) は **Eq.(D16) と同符号（t,δ,Δ>0 で負）**。
w 項を落とすと 2-band 積分核が 0 になることもテスト化（continuum 形が TB で誤り）。
→ **符号・prefactor を in-repo 一次閉形式に anchor**。`tests/test_shift_current_rice_mele.py`。

### B. F4-2 Tan & Rappe 2016 多バンド対称則
同論文 1D SSH/Rice-Mele 模型 Eq.(14) の定性則を多バンド Nestoklon/Kashikar-polar で確認:
δ=0 or Δ=0 で消失、**δ→−δ で σ_zzz 符号反転（機械精度）**、|δ| 増大で |σ| 増大。s↔p spσ 符号交替が起源。

### C. 対称選択則（F4-4）
立方 δ=0 で σ_xxx=σ_yyy=σ_zzz=0（機械精度）。P4mm（[001] δ>0）で σ_zzz≠0 だが σ_xxx≈σ_yyy≈0。

### D. 数値整合
batched 一般化微分 = 明示 (v,c,p) ループと機械精度一致。batched σ = per-k σ（1e-14）。

## 5. 限界（Blount 1962 統一ナラティブ）

TB の位置演算子 `r=i∂_k` は **intra-atomic 成分を欠く**（Blount 1962）。→ shift current の**絶対振幅は系統的に過小**
（g因子 Roth-Lax 過小・光学 f-sum ~0.21 と同根）。**相対傾向・対称性・スペクトル形状・符号は信頼可、絶対量は Wannier
ベース位置演算子が要**。本テーマは**相対比較を一次成果**とし、絶対 μA/V²（Young&Rappe 2012 Eq.1 prefactor
`πe³/(ℏ⁴V_cell)`）は規約敏感 + Blount 限界のため deferred（formula は記録）。

## 6. 物理的考察

- **鉛フリーが有利な機構**: shift current の積分核は ~1/E_cv² のエネルギー分母を持ち、小 gap で増大する。
  Sn/Ge は Pb より p 軌道オンサイトが低く gap が小さい（特に I 系で顕著）→ band-edge 近傍の遷移強度・shift vector が大きい。
  毒性 Pb を避けつつ BPVE を増やせる可能性を示す（定性レベル）。
- **SOC の含意**: Sn/Ge は Pb より SOC（λ）が弱く CBM 分裂が小さい。本計算は各材料の Kashikar λ を含むが、
  SOC on/off 比較（F-D8 予定）で shift current への SOC 寄与の組成依存を切り分ける価値がある。
- **絶対値の限界**: 相対単位での比較（順位・符号・スペクトル形状）は頑健だが、絶対 μA/V² は Blount 1962 の
  TB intra-atomic 欠落で系統的に過小（§5）。実デバイス効率の見積りには Wannier ベース位置演算子か実験アンカーが要。
- **構造の単純化**: 立方相 + [001] 単一極性モードのみ。実 Sn/Ge ペロブスカイトは八面体傾斜・Jahn-Teller を伴うため、
  実材料の σ は本値と定量的に異なりうる（傾斜歪みは別の symmetry breaker、F5+ で検討可）。
- ダブルペロブスカイト（Cs₂AgBiBr₆ 等）との比較は射程外（`cowork/research_ideas.md`）。

## 7. 再現コマンド

```bash
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 PYTHONPATH=src \
  python scripts/scan_shift_current_9materials.py production
PYTHONPATH=src python -m pytest tests/test_shift_current.py tests/test_shift_current_rice_mele.py -q
```

## 8. 関連ファイル

- 実装: `src/perovskite_tb/shift_current.py`（builders, 一般化微分, Rice-Mele）
- テスト: `tests/test_shift_current.py`, `tests/test_shift_current_rice_mele.py`
- 定式化: `docs/shift-current-formulation.md`
- 出典: Fregoso 2017 (arXiv:1701.00172), Tan & Rappe 2016 (npj CM 2:16026),
  Young & Rappe 2012 (PRL 109 116601 / arXiv:1202.3168), Kashikar 2021 (arXiv:2101.08562)
- Production: `results/production/theme_F_shift_current/2026-05-23_ef575e3/`（MANIFEST.json; git_dirty:false）
