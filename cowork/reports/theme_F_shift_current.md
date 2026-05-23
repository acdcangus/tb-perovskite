# Theme F: 立方晶 CsBX₃ の shift-current バルク光起電力効果（BPVE）

**ステータス:** F1–F4 完了（手法確立・符号確定）、F5 Production 実行・集計中（§3 は確定値で更新予定）。
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

## 3. 主要結果（F5 — Production 集計後に確定値で更新）

<!-- TODO: production run 完了後に peak_summary.csv / key_numbers から確定値を記入 -->
- 9 材料 × δ の σ_zzz(ω)（相対単位）→ `results/production/theme_F_shift_current/<date>_<hash>/`。
- 鉛フリー比較: ピーク強度・[Eg,2Eg] ω 積分・gap 正規化で評価（§6 観点）。
- 図: `outputs/figures/sigma_zzz_9materials.png`、数値: `MANIFEST.json key_numbers`。

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

## 6. 物理的考察（F5 結果確定後に拡充）

- 主問い: Sn/Ge は SOC が Pb より弱い → CBM 構造・遷移強度が異なる。ピーク強度だけでなく [Eg,2Eg] ω 積分・
  gap 正規化 σ で比較（Cowork 1840 §6）。
- ダブルペロブスカイト（Cs₂AgBiBr₆ 等）との比較は F5+ の射程外（research_ideas）。

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
- Production: `results/production/theme_F_shift_current/<date>_<hash>/`（MANIFEST.json）
