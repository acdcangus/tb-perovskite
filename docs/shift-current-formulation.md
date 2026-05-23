# Shift current / Bulk Photovoltaic Effect の理論定式化メモ（Phase 2 / Theme F, F2 draft v1）

**作成:** 2026-05-23（F2）
**ステータス:** ドラフト第一版（Cowork レビュー待ち。**F3 実装は本 doc 承認後**）
**目的:** 既存 TB エンジン + velocity operator（A2）から、ハライドペロブスカイトの
shift current 伝導度 σ⁽²⁾_abc(ω)（bulk photovoltaic effect, BPVE）を計算する定式化。

> **注意（文献取得状況, `progress/2026-05-23_1130_theme_F_pdf_status.md`）:** 本 draft の主方法論
> 参照は **Passos et al. 2018（arXiv:1712.04924, 取得・検証済み）**。shift current の原典
> **Young & Rappe 2012** と検証アンカー **Tan & Rappe 2016** は **PDF 未取得**（Cowork が示した
> arXiv ID 1207.5462 / 1612.09194 は検証の結果**別分野の無関係論文**で削除済み）。よって
> 本 draft の σ⁽²⁾ 表式は **directive 引用式 + Sipe-Shkrebtii 標準形 + Passos 2018** から
> 再構成したものであり、Young&Rappe / Tan&Rappe の式番号・検証値は PDF 取得後に照合する。

---

## 0. 方針
- g因子・光学と **同じ velocity operator `∂H/∂k`（`velocity.py`）を再利用**。
- shift current は **2次の非線形光学応答**で、Berry connection とその covariant derivative が要る。
- **立方ペロブスカイト（Pm-3m）は中心対称 → σ⁽²⁾ ≡ 0**。非ゼロにするには **空間反転対称の破れ**が必須（§4）。
- F3（実装）は本 doc の Cowork 承認後（CLAUDE.md「1ファイルごと承認」）。

## 1. 動機・適用範囲
Bulk photovoltaic effect (BPVE) / shift current は、**p-n 接合を必要とせず**単一の非中心対称
結晶バルクで光起電力を生む機構。shift current は電子の実空間 Wannier 中心の遷移（"shift vector"）
に由来。鉛フリー（Sn/Ge）系での系統予測は未踏（2025-2026 ホットトピック）。

## 2. 支配方程式（shift current; Young & Rappe 2012 / Sipe-Shkrebtii 2000）
$$
\sigma^{(\text{shift})}_{abc}(\omega) = -\frac{\pi e^3}{\hbar^2}
  \int\!\frac{d\mathbf k}{(2\pi)^3}\sum_{n,m} f_{nm}\,
  \mathrm{Im}\!\big[r^a_{mn}\, r^b_{nm;c}\big]\,\delta(\omega-\omega_{nm})
$$
- `f_{nm}=f_n-f_m`（占有差）、`ℏω_{nm}=E_m-E_n`。`a,b,c` はデカルト成分。
- **Berry connection（off-diagonal, n≠m）**:
  $$ r^a_{mn} = \frac{i\,p^a_{mn}}{m_0\,\omega_{nm}}
     = \frac{i\,\langle m|\partial_{k_a}H|n\rangle}{E_n - E_m}\quad(n\neq m) $$
  （`p^a_{mn}=m_0 v^a_{mn}`, `v^a=(1/ℏ)∂_{k_a}H`。`velocity.py` の `∂H/∂k` をそのまま使用。）
- **covariant derivative（generalized derivative）**:
  $$ r^b_{nm;c} = \partial_{k_c} r^b_{nm} - i\,(r^c_{nn}-r^c_{mm})\,r^b_{nm} $$
  `r^c_{nn}` は intra-band Berry connection（対角, gauge 依存）。covariant derivative 自体は
  gauge-covariant で物理的。
- δ → Lorentzian（η≈0.05 eV）。

shift vector 表現（等価, Fregoso 2017 系）: `R^{abc}_{nm} = ∂_{k_c}φ^{ab}_{nm} + r^c_{nn}-r^c_{mm}`
（`φ` は `r^a_{mn}r^b_{nm}` の位相）。σ⁽²⁾ ∝ Σ |r^a|² R^{abc} δ。F3 ではどちらの形でも実装可。

## 3. TB Hamiltonian での実装（velocity gauge; Passos et al. 2018, arXiv:1712.04924）
Passos 2018 は **velocity gauge** での任意次非線形伝導度を、位置演算子の Blount 分解
（`r = i∂_k + ξ`, ξ=Berry connection）と covariant derivative `D_k = ∂_k - iξ` で定式化。要点:
1. `p^a_{mn} = ⟨m|∂_{k_a}H(k)|n⟩`（= velocity matrix element, `velocity.py`）。**解析的 ∂H/∂k**。
2. off-diagonal Berry connection `r^a_{mn}` は §2 の式で固有ベクトルと ∂H/∂k から直接。
3. covariant derivative `r^b_{nm;c}`:
   - **(A) k 有限差分**: `∂_{k_c}r^b_{nm}` を MP グリッド上の中心差分で（Tan & Rappe 2016 Methods 流; 要 gauge 固定 or covariant 差分）。
   - **(B) 解析的（sum-over-states）**: `∂_{k_c}r^b_{nm}` を別バンド和で展開（Passos 2018 の covariant derivative 公式）。数値的に安定だが実装重。
   - F3 ではまず (A)、検証で (B) と比較。
4. 退化・対角項 `n=m` は除外（intra-band は別途 Drude/injection 項、shift current には不要）。

## 4. 対称性と symmetry breaker（**重要・directive への補正**）
shift current σ⁽²⁾_abc は **3階極性テンソル** → **空間反転対称下で恒等的にゼロ**。
- **立方 Pm-3m: σ⁽²⁾ = 0**（中心対称）。
- ⚠️ **directive (1055) §1.2 の推奨「(I) uniaxial strain [001]」は不十分**:
  cubic Pm-3m に一軸歪みを加えても **正方晶 P4/mmm（依然 中心対称）**になるだけで、
  **反転対称は破れず σ⁽²⁾ は依然ゼロ**。Tan & Rappe 2016 が扱った系は元々**強誘電/極性**
  （非中心対称）であり、純粋な一軸歪みでの inversion breaking ではない点に注意。
- **正しい symmetry breaker（CsPbX₃ を非中心対称化）**:
  - **(III) 極性変位（推奨）**: B カチオン（Pb）または A（Cs）を halide ケージに対し [001]
    方向に δ だけ off-center（強誘電的歪み, → P4mm）。**1 スカラ δ で系統スキャン可能**、
    確実に反転対称を破る。Slater-Koster ホッピングは結合長変化で修正（§下記）。
  - **(II) 反転を破る八面体傾斜**: 特定の tilt パターン（例: 非中心対称な a⁰a⁰c⁺ 以外）。
    Theme B 旧計画の規模。極性変位より複雑。
  - → **本 draft は (III) 極性変位 δ を主 symmetry breaker として推奨**。F3 で δ スキャン。
- **SK ホッピングの歪み修正（出典付き）**: 結合長 `d` 依存は Harrison/Slater-Koster 距離スケーリング
  `t(d) = t(d_0)·(d_0/d)^{η_l}`（η_l は軌道対依存の指数; 例: Harrison η=2 for s-p-d 系の標準値、
  または材料別フィット）。**この η_l は出典が必要**（Kashikar/Nestoklon は固定結合長で η を与えて
  いない）→ **Cowork 確認事項**（後述 §未解決）。極性変位では Pb-I_z 上下の結合長が ±δ 非対称に
  なり、これが反転対称を破る。

## 5. 検証アンカー（F4 テスト用）
1. **中心対称で消失**: 無歪み立方（δ=0）で σ⁽²⁾_abc ≈ 0（数値積分誤差以内）。**最重要・
   ハルシネーションproof**（対称性は厳密に保証されるべき）。
2. **極性変位で発現**: δ>0 で σ⁽²⁾_{zzz}(ω) ≠ 0、δ→0 で連続的に 0 へ。
3. **ピーク位置 = バンド端近傍**: σ⁽²⁾ の立ち上がりが直接ギャップ ~Eg。
4. **Tan & Rappe 2016 MAPbI₃**（**PDF 取得後**）: shift current ピーク位置（~2-3 eV）と振幅
   （~10-100 μA/V²）を ±0.1 eV / order-of-magnitude で照合。**現状プレースホルダ**。
5. **sum rule / gauge 不変性**: velocity gauge (Passos) と length gauge の一致確認（Passos 2018 の主題）。

## 6. 既知の限界（Blount 1962 統一ナラティブの継続）
TB の位置演算子 `r = i∂_k`（+ξ）は **intra-atomic 成分を欠く**（E. I. Blount, *Solid State Phys.*
**13**, 305 (1962); *Phys. Rev.* **126**, 1636 (1962)）。Passos 2018 も Blount 分解を出発点とする。
→ shift current の **絶対振幅も系統的に過小**になる可能性大（g因子 Roth-Lax 過小評価・光学 f-sum
~20% と同根）。**論文の統一メッセージ**: 「TB-IPA は相対傾向・対称性・スペクトル形状は信頼可、
絶対量は Wannier ベース position operator が要」。Tan & Rappe 2016 の Wannier 比較を引用予定（PDF 待ち）。

## 7. 数値設計（F3-F4 計画）
- k グリッド: MP 8³→12³→16³ 収束（shift current は k 収束が遅いことが多い → 要 convergence.md）。
- η: 0.03/0.05/0.08 eV 感度。
- 極性変位 δ: 0〜~0.3 Å（or 格子定数比 0〜5%）でスキャン、σ⁽²⁾ ∝ δ（小 δ で線形）を確認。
- 9 材料 × δ で σ⁽²⁾_{zzz}(ω) → `results/shift_current/`。乱数なし（決定論的 k 和）。
- 計算結果に再現性メタデータ付与（`_meta.py`）。既存 205 テスト破壊なし（純拡張）。

## 8. 未解決・要判断（Cowork へ）
1. **symmetry breaker**: directive 推奨の uniaxial strain は中心対称を破らず σ⁽²⁾=0 のまま。
   **極性変位 (III) に変更**してよいか（物理的に必須）。あるいは元々非中心対称な低対称相を使うか。
2. **SK 距離スケーリング指数 η_l の出典**: 歪み下の hopping 修正に必要だが Kashikar/Nestoklon は
   固定結合長。Harrison 標準値（s,p,d で d⁻²等）を採用してよいか、材料別フィットが要るか。
   → 出典確定まで F3 実装は保留（推測しない）。
3. **Young & Rappe 2012 / Tan & Rappe 2016 / Fregoso 2017 の正しい PDF**（§冒頭注記）。
   検証アンカー（MAPbI₃ ピーク）と式番号・符号の照合に必須。

## 参考文献（出典; 取得状況明記）
- **D. J. Passos, G. B. Ventura, J. M. V. P. Lopes, J. M. B. Lopes dos Santos**, "Nonlinear optical
  responses of crystalline systems: Results from a velocity gauge analysis", *Phys. Rev. B* **97**,
  235446 (2018); arXiv:1712.04924. — **primary 方法論（取得・検証済み）**。velocity gauge, Berry
  connection, covariant derivative, Blount 分解。
- A. M. Sheikhabadi, Z. Bagheri, A. Sadeghi, "Theory of nonlinear optical response", arXiv:2207.00331
  (2022). — **sub**（disorder 入り 2nd-order response の formalism。取得・検証済み）。
- J. E. Young, A. M. Rappe, *Phys. Rev. Lett.* **109**, 116601 (2012). — shift current 第一原理公式
  （**PDF 未取得**, ID 要確認）。
- J. E. Sipe, A. I. Shkrebtii, *Phys. Rev. B* **61**, 5337 (2000). — 非線形応答 k 空間表式（未取得）。
- F. Tan, A. M. Rappe et al., *npj Comput. Mater.* **2**, 16026 (2016). — ペロブスカイト shift current
  TB 計算・検証アンカー（**PDF 未取得**, OA のはず）。
- B. M. Fregoso, T. Morimoto, J. E. Moore, *Phys. Rev. B* **96**, 075421 (2017). — shift vector 形式（未取得, ID 要確認）。
- E. I. Blount, *Solid State Phys.* **13**, 305 (1962); *Phys. Rev.* **126**, 1636 (1962). — 統一限界。
- S. Rajpurohit et al., arXiv:2105.11310. — bulk photovoltaic 背景（既収集）。
