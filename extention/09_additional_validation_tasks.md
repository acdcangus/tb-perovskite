# 追加検証タスク指示書（tb-perovskite 実装エージェント向け）

**作成日**: 2026-05-24
**前提**: ユーザ指示「**追加機能は全部やりたいね**」（2026-05-24）
**起点**: `08_validation_status_quantitative.md` の §5.1, §5.2 で挙げた追加検証項目を **全件着手** する
**目的**: F1–F14 の検証ステータスを「内部アンカー（B）」中心から「論文値との定量 % 比較（A）」へ拡充し、仕様書 `00_README.md` §4-B（妥当性）を強化する

---

## 0. 全体方針

### 0.1 honest 限界の継承

実装エージェントが既に honest に宣言している **SK-TB / Blount caveat 由来の絶対値限界** は引き続き尊重する。本タスクの目的は **絶対値の主張ではなく**：

1. **トレンド・比 (ratio) の定量比較** — n 依存、ε 依存、材料間比
2. **対称性・位相量子化の精度向上**
3. **既存ベンチマーク文献との %差を明示**

### 0.2 ハルシネーション再防止

handoff §0.1 のサイクル A（引用文献の DOI 事前 web 検証）を **すべての追加文献に対して再実施**。本タスクで新規参照する Buin 2014, Grumet 2018, Blancon 2017, Frohna 2018 等の DOI を着手前に検証する。

### 0.3 既存ベンチマークの不変性

既存 314 テストは **一切変更せず**、追加検証は **新規テストファイル** または **既存テストの append** として実装。

---

## 1. Tier-1: 即実施可能（既存ベンチマーク文献あり）

### T1-1 ★★★ F5 (2D RP slab) — Blancon 2017 の n 依存 E_g 再現

**動機**: 2D Ruddlesden-Popper ペロブスカイトの量子閉じ込めギャップは、薄板層数 n に対し有名な減衰を示す。**Blancon 2017 Science の Fig. 2** が実験基準。

**入力データ**：
- 系：(BA)₂(MA)_{n-1}Pb_nI_{3n+1}, n = 1, 2, 3, 4
- ハードバリア理想化（Even 2014 ChemPhysChem 15, 3733）
- 既存 `slab.py` でスラブ計算 + n 変化

**期待される論文値（Blancon 2017 Science 355, 1288, Fig. 2）**：
| n | E_g (eV) |
|---|---|
| 1 | 2.43 |
| 2 | 2.16 |
| 3 | 2.03 |
| 4 | 1.91 |
| ∞ (3D) | 1.65 |

**比較対象（2 通り）**：
1. **絶対値**：SK-TB caveat により 100-300 meV のズレを想定 → "**模型 vs 実験**" として記録（A カテゴリだが %差は大きい）
2. **トレンド ΔE_g(n) = E_g(n) − E_g(∞)**：減衰の形（指数 / 1/n²）が一致するかを定量比較 → これが本質

**Acceptance**:
- E_g(n) を n=1,2,3,4,∞ で計算
- 減衰トレンド（log-log プロット）の傾きが Blancon 2017 と **15% 以内**で一致
- 絶対値の deviation を README / docstring に明記

**実装ノート**:
- 既存 `tests/test_slab.py` に `test_blancon_layer_dependence` 追加
- 結果は `results/figures/blancon_E_g_n.png` に保存

**文献（DOI 事前確認必須）**:
- J.-C. Blancon et al., *Scaling law for excitons in 2D perovskite quantum wells*, Science 355, 1288 (2017). DOI: 10.1126/science.aal4211
- J. Even, L. Pedesseau, C. Katan, ChemPhysChem 15, 3733 (2014). DOI: 10.1002/cphc.201402428（**訂正済み**）

---

### T1-2 ★★★ F12 (strain) — Buin 2014 / Grumet 2018 の dE_g/dε 比較

**動機**: バンドギャップの歪み感度 dE_g/dε は太陽電池応用で重要。DFT 値が複数文献で報告されている。

**入力データ**：
- 系：CsPbI₃, MAPbI₃（既存 SK-TB パラメータ）
- 歪み：静水圧 ε = −2%, −1%, 0, +1%, +2%
- 既存 `bandengr.py` で線形フィット

**期待される論文値**：
- **Buin et al., Nano Lett. 14, 6281 (2014)**: MAPbI₃ で dE_g/dε ≈ −30 to −50 meV/%（圧縮で gap 増加）
- **Grumet et al., 2018**: 類似値 — DOI を事前確認

**比較対象**:
- **符号**：両者で同符号（負, 圧縮で gap 増加）を必須確認 → **C カテゴリ確保**
- **大きさ**：30-50 meV/% の範囲内で再現できれば **A カテゴリ達成**（30% 以内）

**Acceptance**:
- dE_g/dε（線形フィット）を CsPbI₃, MAPbI₃ で計算
- Buin 2014 / Grumet 2018 と **符号は厳密一致, 大きさは 30% 以内**
- 一軸（[001], [110]）も計算しトレンド比較

**実装ノート**:
- 既存 `tests/test_bandengr.py` に `test_strain_gap_sensitivity_lit` 追加
- `data/parameters/strain_benchmark.json` に文献値を集約

**文献（DOI 事前確認必須）**:
- A. Buin et al., *Materials Processing Routes to Trap-Free Halide Perovskites*, Nano Lett. 14, 6281 (2014). DOI: 10.1021/nl502612m **要確認**（タイトル/DOI/年）
- A. Grumet et al., 2018 — **DOI 不明、事前確認必須**

---

### T1-3 ★★ F6 (polaron) — 9 材料 α マップ完成 + CsPbBr₃ の % 明記

**動機**: 既に MAPbI₃ で <1% 達成済み。残り 8 材料の ε_S / ω_LO を文献収集し、α マップ完成。

**追加対象材料**：
| 材料 | ε∞ | ε_S | ω_LO (meV) | m* (electron) | 出典候補 |
|---|---|---|---|---|---|
| MAPbI₃ | 6.5 | 25.7 | 16.5 | 0.21 | Frost 2017 (既収) |
| MAPbBr₃ | 4.7 | 29.8 | 17.5 | 0.23 | Sendner 2018 |
| MAPbCl₃ | 4.0 | 23.9 | 21.0 | 0.27 | Sendner 2018 |
| CsPbI₃ | 6.1 | 18.1 | 13.6 | 0.20 | Frost 2017 |
| CsPbBr₃ | 4.8 | 20.5 | 19.2 | 0.22 | Sendner 2021 (既収) |
| CsPbCl₃ | 4.1 | 17.0 | 22.6 | 0.27 | Sendner 2018 |
| FAPbI₃ | 6.5 | 25.0 | 14.0 | 0.20 | Frost 2017 |
| FAPbBr₃ | 5.0 | 26.0 | 15.0 | 0.22 | Sendner 2018 |
| FAPbCl₃ | 4.1 | 20.5 | 18.0 | 0.27 | 推定値要確認 |

**Acceptance**:
- 全 9 材料で α 計算
- **MAPbI₃ <1%, CsPbBr₃ <1% を明示的 % で記録**（既存 V&V を defensive にハードコード）
- 残り 7 材料は **Frost 2017 / Sendner 2018,2021 の報告値と <5%** で一致

**文献（DOI 事前確認必須）**:
- J. M. Frost, PRB 96, 195202 (2017). DOI: 10.1103/PhysRevB.96.195202（既収・確認済）
- A. M. A. Leguy, ... K. Sendner et al., *Materials Horizons* 5, 118 (2018). DOI: 10.1039/c7mh00829e — 9 ハライドペロブスカイトの ε / LO **要事前確認**
- K. Sendner et al., Nat. Commun. 12, 4945 (2021). DOI: 10.1038/s41467-021-25008-5（既収・確認済）

---

## 2. Tier-2: 中期検討（既存実装の拡張要）

### T2-1 ★★ F4 (Rashba) — バルク極性相での DFT 値比較

**動機**: Niesner 2016 は表面 Rashba（spin-LEED）で MAPbBr₃ 室温 α_R ~ 11 eVÅ を報告したが、本実装は **バルク極性相** を扱う。バルク値の DFT 比較対象を探す必要がある。

**候補文献**（要事前確認）：
- Brivio et al., PRB 89, 155204 (2014) — MAPbI₃ DFT
- Even et al., J. Phys. Chem. Lett. 4, 2999 (2013) — Rashba in halide perovskites
- Etienne et al., J. Phys. Chem. Lett. 7, 1638 (2016) — dynamic Rashba

**Acceptance**:
- 文献選定理由を明記（バルク極性相での DFT 値）
- 値を **桁レベル**（同じ eVÅ オーダ）で一致
- 表面 Rashba 比較は明示的に除外

---

### T2-2 ★ F1 (AHC) — Berry 統合インフラの 3D 模型ベンチ

**動機**: 立方ペロブスカイトでは AHC = 0 を機械精度で確認済み。トリビアル ↔ トポロジカルの相転移を 3D 模型（Fu-Kane-Mele 等）で再現すれば、SHC/AHC の **相対符号** が信頼できる。

**Acceptance**:
- Fu-Kane-Mele 模型（PRL 98, 106803, 2007）の Z₂ 相を Wilson loop で確認 → **既に F2 で部分実装、3D 版を追加**
- 質量項符号変化での Berry 曲率符号反転を確認

**実装ノート**:
- F2 と統合する形で、Z₂ parity 法（Fu-Kane parity）も同時実装し、§4 「未実装」リストから外す

---

### T2-3 ★★ F14-B (分極) — 強誘電ペロブスカイトでの ΔP 比較

**動機**: 電子寄与のみの絶対値は意味を持たないが、**強誘電遷移 (PE → FE) での ΔP** は gauge 不変な観測量で、実験・DFT で報告されている。

**候補文献**（要事前確認）：
- Frohna et al., Nat. Commun. 9, 1829 (2018) — MAPbI₃ Rashba/分極
- Stroppa et al., Nat. Commun. 5, 5900 (2014) — ハライドペロブスカイトの強誘電性 DFT

**Acceptance**:
- MAPbI₃ または類似系で PE → FE 構造変位を導入
- ΔP（電子寄与）を計算
- DFT 値（典型 1-5 μC/cm²）と **桁一致 + 符号一致**

---

### T2-4 ★ F11 (Edelstein) — 比 χ_yx / σ_xx

**動機**: χ の絶対値は τ 依存だが、**χ_yx / σ_xx の比** は τ がキャンセルする量で、Edelstein 効率の指標。

**Acceptance**:
- Rashba 模型解析値との一致を厳密に検証
- ペロブスカイト極性相での χ_yx / σ_xx を計算
- 実験報告（exists if any）と比較

---

## 3. Tier-3: 構造的限界（SK-TB / Blount caveat）

以下は **SK-TB の本質的限界** のため、**追加検証は GW or DFT スターターハミルトニアン**を要する。本タスクのスコープ **外**：

- F1 SHC 絶対値
- F4 α_R 絶対値（バルク, 任意材料）
- F11 χ 絶対値
- F7 CPGE 材料絶対値
- F14-B 絶対分極（イオン寄与込み）

これらの改善は別仕様（将来）として扱う。

---

## 4. 実装エージェントへの作業フロー

各タスク（T1-1 〜 T2-4）について：

```
[1] handoff §0.1 サイクル A — 引用 DOI を WebSearch で事前確認
[2] 文献の数値（表/図）を精読して引用
[3] 既存モジュール（berry, rashba, polaron, bandengr, slab, polarization）に検証関数を追加
[4] tests/test_*_lit.py または test_*.py に Acceptance テストを追加
[5] data/parameters/*_benchmark.json に文献値を出典付きで集約
[6] results/figures/ に比較プロット（log-log 等）を保存
[7] docs/numerical-methods.md §9-§18 の V&V 節を更新
[8] handoff §0.2 サイクル C — 3 回批判的レビュー（自己 → 別 Claude → 反復）
[9] 08_tb-perovskite_implementation_report.md §1 に「論文値定量比較 (A カテゴリ)」を追記
```

---

## 5. Acceptance（タスク全体）

本指示書全体の完了条件：

1. **Tier-1（T1-1, T1-2, T1-3）が全て A カテゴリ（論文値%比較）で達成**
2. **Tier-2（T2-1, T2-2, T2-3, T2-4）が桁・符号一致または明示的 caveat 付き**
3. **314 + 新規テスト全 pass**
4. **`08_tb-perovskite_implementation_report.md` の V&V カテゴリ A/B/C/D 分類を更新**
5. **`08_validation_status_quantitative.md` の マトリックスを更新**
6. **新規引用文献の DOI 全件実在確認済み**

---

## 6. 想定工数

| Tier | タスク | 工数 |
|---|---|---|
| T1-1 | F5 Blancon n 依存 | 1-2 週 |
| T1-2 | F12 strain dE/dε | 1 週 |
| T1-3 | F6 polaron 9 材料 | 1 週 |
| T2-1 | F4 Rashba バルク DFT | 1-2 週 |
| T2-2 | F1 AHC 3D 模型 + Z₂ parity 完成 | 2-3 週 |
| T2-3 | F14-B 強誘電 ΔP | 2 週 |
| T2-4 | F11 χ/σ 比 | 1 週 |
| **合計** | — | **9-13 週** |

---

**注**: 本指示書は `07_agent_handoff.md` §0.1（ハルシネーション防止）、§0.2（3 回批判的レビュー）、§0.3（非統合・3 プロジェクト独立）に従う。すべての追加文献は **DOI 事前確認 → 原典精読 → 実装** の順で進めること。

**(EOF)**
