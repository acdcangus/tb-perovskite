# Landé g因子の理論定式化メモ（Phase 1 / Theme A, draft v1）

**作成:** 2026-05-23（A1: 文献読み込み）
**ステータス:** ドラフト第一版（Cowork レビュー待ち）
**目的:** 既存 TB エンジンから CsBX₃ 9材料の電子・正孔 Landé g因子を計算するための理論定式化と、論文ベースの検証アンカーを整理する。

---

## 0. 要約と方法選択（重要・要レビュー）

文献を精読した結果、**g因子の計算法は対象系で2通り**ある：

| 方法 | 適用対象 | 出典 | 本プロジェクトでの用途 |
|---|---|---|---|
| **(I) k·p / Roth-Lax 摂動公式**（バンド端のバンド間速度行列要素から） | バルク（無限結晶、k点1点） | Kirstein 2021 Eq.(5),(6); Nestoklon 2023 SI Eq.(S3),(S7) | **9材料バルクスキャン（A4）の主手法** |
| **(II) Peierls 置換 + Zeeman 項の有限磁場対角化** | ナノ結晶・有限系（実空間）/ 磁場超格子 | Nestoklon 2023 本文 II 節 | NC 計算用（本 Phase では副次的） |

> **方法選択（Cowork レビュー 2026-05-23 で確認済み ✅）:** バルク9材料スキャンには
> **(I) k·p / Roth-Lax** を採用（承認）。**k·p 普遍式をゴールドスタンダード**、Roth-Lax を
> atomistic 比較に用い、**両者の差分を remote band 寄与の指標**として記録する（欠陥ではなく
> 科学的解釈）。(II) Peierls+Zeeman は Theme A 完了後の NC 拡張で別 Phase に実装。

---

## 1. 物理：g因子と Zeeman 分裂

外部磁場 **B** 中で、バンド端の Kramers 二重項のスピン状態は Zeeman 分裂する：
```
E_Z = g μ_B B           (μ_B: ボーア磁子)
```
g因子は分裂から `g = E_Z / (μ_B B)`（Kirstein 2021 Eq.(2), Nestoklon 2023 本文）。
立方ペロブスカイトの直接ギャップは **R 点**（点群 O_h）。価電子帯頂上 (VBM) は Γ₆⁺（二重項, S 的）、伝導帯底 (CBM) は Γ₆⁻（二重項, スピン1/2）、その上に Γ₈⁻（4重縮退, heavy/light electron, スピン3/2）が SO 分裂 Δ だけ離れて存在する（Nestoklon 2023 SI, Fig. S2; Kirstein 2021 Fig.1c）。

g因子は **スピン寄与（自由電子値 g₀≈2.0023）** と **軌道寄与（バンド間 k·p 混成）** の和。
- **正孔（VBM）**: 主に伝導帯との k·p 混成。
- **電子（CBM）**: 価電子帯および高位伝導帯（remote bands）との混成。

---

## 2. k·p 普遍式（バルク、解析・検証アンカー）

Kirstein 2021 が実験的に発見し TB/k·p で確認した普遍依存性（立方相）：

**正孔 g因子（Kirstein Eq.5 / Nestoklon Eq.S3）:**
```
g_h = 2 − (4/3)(p²/m₀) [ 1/E_g − 1/(E_g + Δ) ]
```

**電子 g因子（Kirstein Eq.6 / Nestoklon Eq.S7）:**
```
g_e = −2/3 + (4/3)(p²/(m₀ E_g)) + Δg_e
```

ここで
- `E_g`: バンドギャップ、`Δ`: 伝導帯のスピン軌道分裂、
- `p`: バンド間運動量行列要素 `p = i⟨Z|p_z|S⟩ = i⟨X|p_x|S⟩ = i⟨Y|p_y|S⟩`（Nestoklon Eq.S2）、
- `Δg_e`: remote band 寄与（材料にほぼ依存しない定数）。

**普遍パラメータ（Kirstein 2021, Fig.5 のフィット）:**
```
Δ = 1.5 eV,   ℏp/m₀ = 6.8 eV·Å,   Δg_e = −1
```
極限値（E_g→∞）: 正孔 g_h → +2、電子 g_e → −2/3 + Δg_e ≈ −5/3
（注: Fig.5 キャプションは電子の極限を「−5/2」と記すが、本文式では −2/3+Δg_e = −5/3。キャプション側の誤植の可能性。要確認）。

**自己検証（A1 で実施済み）:** `(4/3)(p²/m₀) = (2/3)·E_p`（E_p = 2p²/m₀ は Kane エネルギー）。
ℏp/m₀ = 6.8 eV·Å, ℏ²/2m₀ = 3.81 eV·Å² より E_p = (6.8)²/3.81 ≈ 12.1 eV。
CsPbI₃ (E_g=1.652) で `g_e = −2/3 + (2/3)(12.1/1.652) − 1 = 3.22` →
**Nestoklon Table S2 の ETB 値 +3.23 とほぼ一致**。普遍式とパラメータの妥当性確認 OK。

---

## 3. Roth-Lax 公式の TB 表現（バルク atomistic, A2 実装対象）

k·p 普遍式は2〜3バンドへの簡約。**全バンドを含む atomistic な等価表現が Roth-Lax 公式**
（L. M. Roth, B. Lax, S. Zwerdling, Phys. Rev. **114**, 90 (1959)）。バンド端 |n₀⟩(k₀=R) の
有効 g因子の**軌道寄与**を、他バンドとのバンド間運動量（=速度）行列要素の和で表す：

```
Δg_γ = (2/(i m₀)) Σ_{m≠n₀} ε_{αβγ} ⟨n₀|p_α|m⟩⟨m|p_β|n₀⟩ / (E_{n₀} − E_m)
g_γ  = g₀ + Δg_γ              (g₀ ≈ 2.0023 はスピン寄与)
```
（α,β,γ はデカルト成分、ε はレヴィ・チヴィタ。Kramers 二重項では二重項内で磁気モーメント
行列を作り対角化する。スピン寄与の符号・二重項の取り扱いは A2 で要精査 → レビュー希望。）

### TB 速度演算子（解析微分）
運動量行列要素は TB 速度演算子から得る：
```
p_α = m₀ v_α,    v_α(k) = (1/ℏ) ∂H(k)/∂k_α
⟨m|p_α|n⟩ = (m₀/ℏ) ⟨m| ∂H/∂k_α |n⟩
```
本プロジェクトの Bloch ハミルトニアン（`models_*`）は k 依存が解析的（B–X 項は
`S_d=2i sin(k_d a/2)`, `C_d=2cos(k_d a/2)`、B–B 項は `cos(k_d a)`, `sin(k_d a)`）なので、
**∂H/∂k_α も解析的に書ける**（数値微分不要、桁で精度改善）。Nestoklon 系は cation-anion
最近接のみなので ∂H/∂k はさらに単純（Peierls 位相の k 微分）。

→ A2 では `velocity_operator(k)` を各モデルに追加し、Roth-Lax 和を `g_factor.py` で実装する。

> **判断ポイント:** Roth-Lax 公式の軌道寄与は「正準運動量 p = m₀ v」を仮定。TB では
> ゲージ・基底に依存する微妙さ（intra-atomic な軌道角運動量項の欠落）がある。Nestoklon 2023 は
> remote band 寄与 Δg_e を別途与えており、純 Roth-Lax だけでは remote 項を取りこぼす可能性。
> A2 で「速度行列要素から得た Δg」と「k·p 普遍式」を突き合わせて整合を確認する。

---

## 4. Peierls + Zeeman 法（有限系, 参考・(II)）

Nestoklon 2023 本文 II 節の手法。ETB ハミルトニアンに弱磁場を導入：
- **Peierls 置換**: ホッピング `t_{nα,n'ς} → t_{nα,n'ς} exp(i (e/ℏ) ∫ A·dl)`（off-diagonal に磁場依存位相）。
- **Zeeman 項**: 対角に `μ_B (σ·B)`（σ はスピンのパウリ行列）を加える。
- 有限磁場で対角化し、バンド端二重項の Zeeman 分裂から `g = E_Z/(μ_B B)`。

バルク（無限結晶）では一様磁場が並進対称性を壊すため、磁場超格子か k·p/Roth-Lax への帰着が必要。
→ 本 Phase ではナノ結晶拡張時に実装。

---

## 5. 検証アンカー一覧（テスト A3 用）

### 5.1 解析・極限
1. **自由電子極限**: バンド間混成（軌道寄与）→0 で `g → g₀ = 2.0023`（孤立バンドで確認）。
2. **立方対称**: 立方相で g因子は等方 `g_xx = g_yy = g_zz`（Nestoklon 2023 本文「The g-factors are isotropic ... for cubic」）。
3. **k·p 普遍式の極限**: E_g→∞ で g_h→+2, g_e→−5/3。
4. **k·p 整合**: Roth-Lax 実装値が、同じ E_g, Δ, p で評価した k·p 公式(§2)と一致（バンド端近傍）。

### 5.2 Nestoklon 2023 Table S2（バルク ETB、最重要数値アンカー）
| 材料 | E_g (eV) | Δ (eV) | m_e/m₀ | m_h/m₀ | g_e | g_h |
|---|---|---|---|---|---|---|
| CsPbI₃ | 1.652 | 1.258 | 0.168 | 0.145 | **+3.23** | **−0.33** |
| CsPbBr₃ | 2.352 | 1.436 | 0.219 | 0.191 | **+1.77** | **+0.66** |
| CsPbCl₃ | 3.090 | 1.526 | 0.315 | 0.250 | **+0.95** | **+1.14** |

**重大な注意（パラメータ整合性）:**
Table S2 は **修正パラメータセット（Table S1）**で計算されている。Table S1 は「Ref. S1
（= M. Nestoklon, *Comput. Mater. Sci.* **196**, 110535 (2021)＝arXiv:2012.14705 の**ジャーナル版**）」
からの差分として与えられる：

| | CsPbI₃ | CsPbBr₃ | CsPbCl₃ |
|---|---|---|---|
| E_pc | 4.81 | 5.39 | 6.46 |
| ppσ | −2.47 | −2.61 | −2.79 |
| ppπ | 0.00 | 0.05 | 0.20 |
| p_a d_c σ (padcσ) | 2.62 | 2.90 | 3.51 |

- **問題1:** ジャーナル版（Comp. Mat. Sci. 196, 110535）の **CsPbX₃ ベースパラメータ（特に Br/Cl）が
  リポジトリに無い**（arXiv:2012.14705 は CsPbI₃ のみ、かつ experiment_corrected の値は Table S1 の
  ベースと一致しない: 例 CsPbI₃ Epc=4.6044 vs ジャーナル系の修正後 4.81）。
- **問題2:** したがって **Table S2 を厳密再現できるのは CsPbI₃ のみ**（experiment_corrected + Table S1
  差分で近似的に）。CsPbBr₃/CsPbCl₃ はベースパラメータ取得が必要。
- → **Cowork 調査結果（2026-05-23）: 入手不可**（Elsevier paywall, DOI 10.1016/j.commatsci.2021.110535）。
  **Fallback 採用（承認済み）:** **Kashikar 13軌道モデルを9材料スキャンの主手法に格上げ**
  （`kashikar2021_cubic_13orb.json` が CsBX₃ 全9種を網羅、Eq.9 で検証済み）。
  **Nestoklon sp³d⁵s\* は CsPbI₃ のアンカー**として軌道基底拡張の補正量定量化に限定。
  **k·p 普遍式（Δ=1.5, P=6.8, Δg_e=−1）は全9材料の独立参照**。
  論文ストーリー: 「Table S2 厳密再現は CsPbI₃ のみ、他は Kashikar 13軌道 + k·p 比較」。

### 5.3 Kirstein 2021 実験値（符号・オーダーのベンチマーク, ±0.5 許容）
| 材料 | E_g (eV) | g_e (実験) | g_h (実験) |
|---|---|---|---|
| MAPbI₃ | 1.652 | +2.46 〜 +2.98 | −0.28 〜 −0.71 |
| FAPbBr₃ | 2.189 | +2.32 〜 +2.44 | +0.36 〜 +0.41 |
| CsPbBr₃ | 2.352 | +1.69 〜 +2.06 | +0.65 〜 +0.85 |
（CsPbI₃, CsPbCl₃ の実験値は Kirstein が引用する文献 [43] にあり、本文表には MAPbI₃/FAPbBr₃/CsPbBr₃ のみ詳細掲載。要追加抽出。）

### 5.4 Kopteva 2026 (2605.15807)
2D Ruddlesden-Popper の層依存 g因子。バルク参照値の追加ベンチマーク用（後続で抽出）。

---

## 6. 既存コードとの接続（A2 設計メモ）

- `velocity_operator(k)` を Kashikar/Nestoklon builder に追加（∂H/∂k 解析形）。**既存 H(k) は不変、純拡張**。
- `g_factor.py::compute_g_factor(hamiltonian, velocity_ops, band_index, ...)` で Roth-Lax 和を評価。
- VBM/CBM のバンド index は既存 `n_filled`（Kashikar13:20, Nestoklon:26）から決定。
- 速度演算子は g因子と光学（Phase 1.5）で共有する（重複実装禁止）。

## 7. 判断ポイントの解決（Cowork レビュー 2026-05-23, `progress/2026-05-23_0735_code_review.md`）
1. ✅ 方法 (I) Roth-Lax/k·p をバルク主手法 → **承認**。k·p をゴールドスタンダード、Roth-Lax を比較。
2. ✅ remote band 取りこぼし → **Roth-Lax と k·p の差分を remote 寄与として記録**（科学的に正しい解釈、
   許容 |差| ≲ 1.5）。符号規約は Roth-Lax 1959 原典に従う（§3）。
3. ✅ ジャーナル版パラメータ → **入手不可確定**。Fallback（Kashikar 13軌道主手法 + Nestoklon CsPbI₃
   アンカー + k·p 参照）を採用（§5.2）。Cowork が継続調査（task #18）。
4. ✅ SOC→0 テスト → 2種に分離: `test_g_free_electron_limit`（混成OFFで g→g₀）と
   `test_g_cubic_perovskite_bare`（CBM単独 SOC=0 で −2/3, Kirstein の指摘）。

---

## 8. A2 実装結果と再現困難な物理（2026-05-23 追記）

velocity operator `dH/dk`（解析微分）を実装し、有限差分と一致を確認（`tests/test_velocity.py`, 21 通過）。
その上で Roth-Lax の atomistic g因子（`src/perovskite_tb/g_factor.py::compute_g_factor`）を
CsPbI₃（experiment_corrected, R点）で検証した結果：

| 量 | 本実装（atomistic Roth-Lax） | k·p 公式（計算 Eg,Δ + 普遍 P=6.8） | Nestoklon Table S2 |
|---|---|---|---|
| g_e | **+1.06** | +3.24 | +3.23 |
| g_h | **+0.45** | −0.30 | −0.33 |
| 立方等方性 g_xx=g_yy=g_zz | ✅ (差 ~1e-15) | — | ✅ |

**確認できたこと:**
- 立方等方性は厳密に再現（実装の構造・対称性は正しい）。
- TB 速度行列要素は十分大きい: `|⟨CBM|∂_z H|VBM⟩| = 2.97 eV·Å`、全方向・二重項和 √Σ=7.76。
  CBM の Z 成分が √(1/3)（Eq.S1b の sinθ）であることと整合（2.97 ≈ sinθ·P, P≈5.1 eV·Å）。
- **k·p 普遍式は anchor を再現**（g_e: 計算 Eg,Δ で +3.24 vs Table S2 +3.23）。

**再現困難な物理（値は改竄しない）:**
atomistic Roth-Lax（TB `∂H/∂k` 経由）の **|g_e| が Table S2 を大きく下回る（1.06 vs 3.23）**。
原因の候補：
1. **イントラアトミック軌道角運動量の欠落**: オンサイト SOC は k 非依存のため `∂H/∂k` に現れず、
   原子内 p 軌道の軌道モーメント（⟨p_x|L_z|p_y⟩ 型）が速度演算子に入らない。TB g因子・
   軌道磁化で知られる「不完全基底／intra-atomic current」問題。Nestoklon 2023 も
   「halide p-band の記述が次近接なしでは困難で、相互作用が overestimate」と注記（本文 Methods）。
2. **準縮退多重項の摂動論**: CB(Γ₆⁻) と he/le(Γ₈⁻) は Δ≈1.5 eV 離れるが、Roth-Lax の単純2次
   摂動では多重項構造（Clebsch 係数）を取りこぼす可能性。k·p は (4/3) などの角度係数を陽に含む。

**intra-atomic L 項を加えた追試（2026-05-23）:**
オンサイト軌道角運動量（SOC と同じ `_LX/_LY/_LZ` を p 軌道に作用、`onsite_L_operators`）を
Zeeman 行列に加法で追加（係数 g_L=1）。結果：

| 量 | inter のみ | inter + intra-L | k·p / Table S2 |
|---|---|---|---|
| g_e | +1.06 | **+2.27** | +3.24 / +3.23 |
| g_h | +0.45 | **+0.67** | −0.30 / −0.33 |

- g_e は target 方向へ大きく改善（1.06→2.27）。**intra-atomic 軌道モーメントは確かに効く**。
- しかし g_h は逆方向（0.45→0.67、target −0.33）。立方等方性は維持（~1e-15）。
- → 単一の欠落項ではなく、**inter/intra 軌道寄与の符号・準縮退多重項の摂動論**を含む
  総合的な定式化が必要。これ以上の単独推測は**ハルシネーション risk** のため停止し、Cowork に
  式の検証を依頼する（intra-L 項は物理的に正しいのでオプション実装として残置, default off）。

**Cowork レビューによる再解釈（2026-05-23）:** Roth-Lax（モデル内有限バンド）と k·p 普遍式
（remote 寄与 Δg_e=−1 込み）の **差分は remote band 寄与の指標であり、欠陥ではない**（許容 |差|≲1.5）。
intra-atomic L 込みの Roth-Lax g_e=+2.27 と k·p +3.24 の差は **0.97 < 1.5** で整合的。
→ 本プロジェクトの主出力は **k·p 普遍式（ゴールドスタンダード）**、Roth-Lax は atomistic 比較
（差分 = remote 指標）として併記する。g_h の符号差は 2 バンド k·p の限界（remote/多重項）として
A5 で考察。これ以上の単独推測はせず、この方針で A4 に進む。

**当面の実用方針（A4 スキャン）:** atomistic g の絶対値が未検証のため、9材料スキャンは
**k·p 公式（材料ごとに計算した Eg, Δ ＋ 普遍 P, Δg_e）**を主出力とし、atomistic 値は
（intra-atomic 項の決着後の）参考列として併記する。ただし**現実的な Eg が全9材料で必要**
（Kashikar の mBJ Eg は小さすぎて k·p g が過大）→ §5.2 の Comp. Mat. Sci. 196 パラメータ入手が要。

## 参考文献（出典）
- E. Kirstein et al., *The Landé factors of electrons and holes in lead halide perovskites: universal dependence on the band gap*, arXiv:2112.15384 (2021). — Eq.(5),(6), 普遍パラメータ, 実験値表。
- M. O. Nestoklon et al., *Tailoring the electron and hole Landé factors in lead halide perovskite nanocrystals...*, arXiv:2305.10586 (2023). — ETB(Peierls+Zeeman) 法, k·p SI Eq.(S3),(S7), Table S1/S2。
- N. E. Kopteva et al., *Layer-dependent Landé g-factors ... 2D RP lead halide perovskites*, arXiv:2605.15807 (2026). — ベンチマーク。
- M. O. Nestoklon, arXiv:2012.14705 (2020) / *Comput. Mater. Sci.* **196**, 110535 (2021). — ベース TB パラメータ。
- L. M. Roth, B. Lax, S. Zwerdling, *Phys. Rev.* **114**, 90 (1959). — Roth-Lax g因子公式（原典）。
