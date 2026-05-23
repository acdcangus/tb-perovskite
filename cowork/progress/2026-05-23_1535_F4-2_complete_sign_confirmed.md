# F4-2 完了 — 多バンド sanity check が Tan & Rappe 2016 と定性一致 → 符号確定 — 2026-05-23 15:35

**commits:** `69f5c63`（F4-2 test + doc v2）, `ffe2940`（F4-3 fix）
**結論:** **shift current の符号・実装が 2-band 解析（F4-3）と多バンド対称則（F4-2）の二重で確定。**

---

## 1. Tan & Rappe 2016 の本文確認（PDF タイトル検証済み）

`doi_10.1038_npjcompumats.2016.26.pdf` = Tan, Zheng, Young, Wang, Liu, Rappe,
*npj Comput. Mater.* **2**, 16026 (2016)「Shift current BPVE in polar materials」(**レビュー**)。

同論文 §"Modern materials design" は **1D SSH/Rice-Mele 模型 Eq.(14)** を使用:
```
H = Σ_j [ Δ(−1)^j c†_j c_j + (t + (−1)^j δ) c†_j c_{j+1} + h.c. ]
```
- on-site ±Δ（site asymmetry）、bond t±δ（dimerization）。**Fregoso D2 と同型**（私の F4-3 と一致）。
- 明示の定性則（本文 L276–310）:
  1. **δ=0 または Δ=0 → 反転対称 → σ 消失**。
  2. **δ または Δ の符号反転 → shift current の向き（符号）反転**。
  3. **|δ| 増大 → |σ| 増大**（Fig.3）。
  4. s↔p の spσ 結合は**符号交替**（L297–307）→ Eq.14 の δ の物理的起源。これは Nestoklon の
     Pb-s / I-p SK 結合そのもの → 私の多バンド模型が正しい toy。

## 2. 多バンド Nestoklon-polar CsPbI₃ での確認（F4-2 本体）

| δ (Å) | σ_zzz peak | 対応する Tan&Rappe 則 |
|---|---|---|
| 0.00 | 4.9e-15（≈0） | δ=0 → 消失 (則1) ✅ |
| ±0.10 | ∓6.86e-01 | 符号反転 + |σ| 増大 (則2,3) ✅ |
| ±0.15 | ∓1.008e+00 | 符号反転 + |σ| 増大 ✅ |

- **σ_zzz(−δ) = −σ_zzz(+δ) を機械精度（rel ~1e-15）で確認**（[001] δ→−δ は空間反転に相当）。
  → 回帰テスト `test_polar_sign_reverses_under_displacement_flip` 追加。
- |σ|: 0.686→1.008（δ 0.10→0.15, 比 1.47 ≈ 1.5 = δ 比）→ ほぼ線形（小 δ）。
- **これは 2-band 内で閉じる D15 一致とは独立な多バンドの符号確認**（Cowork 1655 §2.5 の懸念「多バンド
  virtual sum の sign bug は D15 では検出不可」をカバー）。virtual sum のベクトル化も明示ループと機械精度一致。

## 3. 限界（正直な申し送り）

- MAPbI₃（Tan&Rappe）vs CsPbI₃-polar（本実装）は **別構造・別手法（DFT vs 経験 TB, 相対単位）** のため
  **絶対振幅の数値照合は不可**。符号・対称則・|δ| スケーリングの**定性照合**にとどめる（方針どおり）。
- 絶対 μA/V² 較正（Fregoso Eq.(D12) の e³/ℏ⁴ prefactor 付与）は **F5 で実施**。
- Blount 1962 の TB intra-atomic 欠落により絶対振幅は系統的に過小（g因子・光学と同根）。

## 4. 符号確定のまとめ（F4-3 + F4-2）

| 検証 | レベル | 結果 |
|---|---|---|
| F4-3 Fregoso D15 | 2-band 解析閉形式 | per-k 積分核 rel<1e-7 一致（符号+magnitude） |
| F4-3 Fregoso D16 | 2-band σ(ω) | t,δ,Δ>0 で σ_zzz<0 一致 |
| F4-2 Tan&Rappe Eq.14 | 多バンド対称則 | δ=0 消失 / δ→−δ 符号反転 / |δ| 増大 すべて一致 |

→ **F4 完了。符号 TBD を解除**。F4-1（length gauge 同値性）は符号衝突が無かったため tiebreaker 不要（未実施）。

## 5. 次タスク

**F5: 9 材料 × δ スキャン（Production モード）** に着手します。
- 絶対 prefactor（Eq.(D12)）の付与方針を design に明記してから実装。
- k グリッド収束（shift current は k 収束が遅い）3 段階 + η 3 段階 + ω 分解能 → PRODUCTION_RULES 準拠。
- `results/production/theme_F_shift_current/<date>_<hash>/` に MANIFEST.json + inputs/ 一式。
- 鉛フリー（Sn/Ge）で σ が大きい組成があるかを主問い。

レビューよろしくお願いします。
