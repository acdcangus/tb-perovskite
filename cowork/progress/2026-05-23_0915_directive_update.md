# Directive Update: A6 追加（TB-derived Kane parameter P）— 簡略版

**発行:** Cowork, 2026-05-23 09:15
**更新:** 2026-05-23 09:30 — ユーザー判断「いったん 2-band でいい」を反映
**契機:** ユーザーから「g 因子は TB ではなく k·p でやったのか」という鋭い指摘あり。
現状の Theme A は **TB の貢献が Sn/Ge の Δ=3λ のみ**で、g 因子値そのものは k·p 公式 + 普遍 P=6.8 で出ている。これを補強する。

**ユーザー判断:** 4-band 拡張は将来の楽しみに温存。**現在のフレームワーク（2/3-band Kirstein-Nestoklon k·p）のまま**、TB-derived P を入れる軽量拡張のみ実施。

---

## A6: TB 速度演算子から材料別 Kane parameter P を抽出

### 目的
Theme A の論文骨格を「TB から導いた SOC 分裂 Δ」だけでなく「**TB から導いた Kane 運動量行列要素 P**」も含む内容に格上げする。これで「9 材料の g 因子を全て TB Hamiltonian の物理量から予測した」と主張できる。

### 文献根拠
- **Nestoklon 2023 SI Eq.(S2)**（arXiv:2305.10586）: `P = i⟨Z|p_z|S⟩ = i⟨X|p_x|S⟩ = i⟨Y|p_y|S⟩` の定義
- **Kane 1957**, J. Phys. Chem. Solids 1, 249: k·p 摂動論の原典（既に常識として通用）
- 本リポ既存実装: `velocity.py` の解析 ∂H/∂k はそのまま使える

### 計算手順

```python
# Pseudo-code, implement in src/perovskite_tb/kane_parameter.py
def extract_kane_parameter(hamiltonian_builder, params, k_band_edge=R_point):
    """
    P_material = (m₀/ℏ) · |⟨CBM(k=R) | v_z | VBM(k=R)⟩|
    
    where v_z is the analytic velocity operator (from velocity.py).
    
    Returns: P in units of eV·Å (i.e., ℏP/m₀ which is what Kirstein uses).
    """
    H = hamiltonian_builder(k_band_edge, params)
    eigenvalues, eigenvectors = diagonalize(H)
    # CBM, VBM indices (既存の n_filled から)
    CBM_state = eigenvectors[:, n_filled]
    VBM_state = eigenvectors[:, n_filled - 1]
    
    v_z = velocity_operator_z(k_band_edge, params)  # 既存
    
    P_matrix_element = np.vdot(CBM_state, v_z @ VBM_state)
    # スピン縮退対の中で最大成分を取る
    P_eVA = abs(P_matrix_element) * hbar_over_m0_eVA  # = 7.62 eV·Å · |⟨v_z⟩|
    return P_eVA
```

### タスクリスト

**Step A6-1.** 文献確認（5 分）
- Nestoklon 2023 SI Eq.(S2) を再読し、P の定義と単位を確認

**Step A6-2.** 実装（30-60 分）
- `src/perovskite_tb/kane_parameter.py` 作成
- 9 材料 × 2 軌道基底（Kashikar 13軌道 / Nestoklon sp³d⁵s\* CsPbI₃）で P を計算
- 結果を `results/g_factors/kane_parameters.csv` に保存

**Step A6-3.** k·p 公式の再評価
- 既存 `scripts/scan_g_factors.py` を **材料別 P でも計算**するオプションを追加
- 2 通り出力：
  - (i) 普遍 P=6.8（既存）
  - (ii) TB-derived 材料別 P（新規）

**Step A6-4.** 検証
- Pb 系で TB-derived P が Kirstein の 6.8 ± 1.0 eV·Å に近いか
- もし大きく違う場合は、その物理的理由を考察（例: Nestoklon sp³d⁵s\* と Kashikar 13軌道で P が違うか）

**Step A6-5.** 報告書 `reports/theme_A_g_factor.md` 更新
- §3 主要結果に「TB-derived P の表」を追加
- §5 物理的考察に「P の材料依存性」を追加
- 「g_e の普遍性が真の普遍か、見かけの普遍か」を論じる：
  - もし TB-derived P が材料ほぼ一定 → 真の普遍
  - もし P が大きく変動 → 普遍性は見かけ
- §1 動機・§6 論文化見通しで「TB ベース計算」と明確に主張

### テスト追加（A6-6）

`tests/test_kane_parameter.py`:
1. **対称性**: 立方相で P_x = P_y = P_z
2. **Pb 系で Kirstein 普遍値との一致**: |P_CsPbI3 − 6.8| < 1.5 eV·Å（許容ゆるめ、文献の範囲）
3. **Nestoklon vs Kashikar の交差検証**: 同じ材料（CsPbI₃）で異なる軌道基底から得られる P が ±20% 以内に一致

### 完了基準

- 9 材料の P が表に出ている
- 報告書 §3 が更新されている
- 既存 193 テスト維持 + A6 の新規テスト ~3 個通過
- `reports/theme_A_g_factor.md` の §6（論文化見通し）に「これで Theme A は完全に TB-based」と書ける

---

## なぜ A6 を入れるか（ユーザーへの応答として）

ユーザーから明確な問題提起：「g 因子は TB じゃなくて k·p でやったの？」

回答：今までは **k·p 公式 + TB-derived Δ (Sn/Ge) + 普遍 P** だった。これを **k·p 公式 + TB-derived Δ + TB-derived P** に格上げする。

これで Theme A は「TB Hamiltonian の物理量だけで 9 材料の g 因子を予測した」と言える。論文の中身としては：

> "We extract from our TB Hamiltonian (i) the conduction-band SO splitting Δ via the analytic R-point eigenvalues (Kashikar Eq. 9) and (ii) the Kane momentum matrix element P via the analytic velocity operator. Substituting both into the k·p universal formula gives material-specific g-factors that constitute the first TB-based prediction for Sn- and Ge-based halide perovskites."

これで論文の「Methods」セクションが綺麗に書ける。

---

## 進め方

- A6 は A5 完了の **発展**として扱う（破壊変更ではなく純拡張）
- Phase 1.5（光学）と並行可能。**両方並行で構わない**
- 完了したら `progress/.../A6_complete.md` で Cowork に通知

がんばってください。
