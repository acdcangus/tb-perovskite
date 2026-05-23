# Shift current / Bulk Photovoltaic Effect の理論定式化メモ（Phase 2 / Theme F, F4 更新 v2）

**作成:** 2026-05-23（F2）／**更新:** 2026-05-23（F4-3/F4-2 完了）
**ステータス:** **F4-3（Rice-Mele 閉形式）+ F4-2（Tan & Rappe 多バンド sanity）で符号・実装確定**。
F3 実装に欠落していた TB 第2微分項 `w^{ab}`（Fregoso Eq.(C2)）を追加（§3, §5-A）→ 旧 F3 σ_zzz は
符号逆・~2.4× 過小だったため破棄・置換。symmetry breaker = [001] 極性変位 (P4mm)、SK 距離スケーリング
= Harrison η=2.0。残: F5（9 材料 × δ, Production, 絶対 μA/V² 較正）。
**目的:** 既存 TB エンジン + velocity operator（A2）から、ハライドペロブスカイトの
shift current 伝導度 σ⁽²⁾_abc(ω)（bulk photovoltaic effect, BPVE）を計算する定式化。

> **注意（文献取得状況, 更新 2026-05-23 後半）:** Cowork correction #2 が正しい arXiv ID を
> 1次情報確認で提供し、**主要文献は全て取得・タイトル検証済み**:
> Passos 2018 (arXiv:1712.04924, primary), Young & Rappe 2012 (arXiv:1202.3168, shift current 原典),
> Fregoso 2017 (arXiv:1701.00172, shift vector 形式), Tan & Rappe 2016 (npj OA,
> `doi_10.1038_npjcompumats.2016.26.pdf`, 検証アンカー・レビュー)。
> Cowork が当初示した ID 1207.5462 / 1612.09194 は検証の結果**無関係論文**で削除済み。
> σ⁽²⁾ 表式は Sipe-Shkrebtii 標準形 + Passos 2018 から再構成。Young&Rappe/Tan&Rappe の
> **具体的検証値（MAPbI₃ ピーク等）は F4 で精密照合**（PDF は取得済み）。

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
3. covariant derivative `r^b_{nm;c}`: **採用 = (B) 解析的 sum-over-states**（velocity gauge,
   Kramers 退化を退化中間状態スキップで処理 → δ=0 の中心対称消失が機械精度で成立）。
   - **★ TB では Fregoso 2017 Eq.(C2) の第2微分項 `w^{ab}_nm = ⟨n|∂²H/∂k_a∂k_b|m⟩` が必須**
     （`shift_current.py::shift_current_integrand_aaa`）:
     ```
     r^a_{nm;b} = -(1/(iω_nm))[ (v^a_nm Δ^b + v^b_nm Δ^a)/ω_nm − w^{ab}_nm
                              + Σ_{p≠n,m}(v^a_np v^b_pm/ω_pm − v^b_np v^a_pm/ω_np) ]
     ```
     Fregoso が明記（Eq.(C2) 直後）するとおり、連続模型 `H=p²/2m+V` では `w^{ab}_nm=δ_nm δ_ab/m`
     が**対角**で off-diagonal 寄与なし（= Sipe-Shkrebtii の標準形）。**TB では ∂²H/∂k² が
     off-diagonal を持つ**ため w 項が効き、これを落とすと 2-band では σ が**恒等的に 0**になる
     （F4-3 で検出した F3 の bug; §5-A 参照）。→ builder は `d2Hdk_fn`（解析的 ∂²H/∂k²）も返す。
   - virtual sum は `R[i,j]=v_ij/(E_i−E_j)`（対角・縮退ペア 0）で `Va@R − R@Va` にベクトル化、
     明示 (v,c,p) ループと機械精度一致を確認済み。
   - (A) k 有限差分は補助（gauge 固定要）。F4-1 として length-gauge 同値性確認は符号衝突時のみの tiebreaker に格下げ（Cowork 1540 承認）。
4. 退化・対角項 `n=m` は除外（intra-band は別途 Drude/injection 項、shift current には不要）。

## 4. 対称性と symmetry breaker（**確定方針; Cowork F2 review 2026-05-23 12:00 承認**）
shift current σ⁽²⁾_abc は **3階極性テンソル** → **空間反転対称下で恒等的にゼロ**。

| 操作 | 結晶系 | 反転中心 | σ⁽²⁾ |
|---|---|---|---|
| 無歪み Pm-3m | cubic | あり | **= 0** |
| [001] uniaxial strain | P4/mmm | **あり** | **= 0**（依然消失）|
| **[001] 極性変位（Pb off-center）** | **P4mm** | **なし** | **≠ 0** ✓（採用）|
| octahedral tilt（非中心対称） | 各種 | tilt 依存 | tilt 依存 |

- **directive (1055) §1.2 の「uniaxial strain」は撤回**（Cowork 承認）: cubic→正方晶 P4/mmm は
  **依然 中心対称** → σ⁽²⁾=0 のまま。
- **主 symmetry breaker（確定）= (III) [001] 極性変位 δ**: B カチオン（Pb）を halide ケージに対し
  [001] に δ [Å] off-center（→ P4mm, 非中心対称）。**1 スカラ δ で系統スキャン**、確実に反転対称を破る。
  Tan & Rappe 2016 も強誘電/極性配置で扱っており文献整合。
  - F3 API: `polar_displacement_z: float = 0.0`（Å, default 0 = 中心対称 → σ⁽²⁾=0 を単体テストで保証）。
- (I) uniaxial strain / (II) octahedral tilt は**比較として記載のみ、本プロジェクトでは採用せず**。
- **SK ホッピングの歪み修正（出典確定）**: 結合長 `d` 依存は **Harrison universal scaling
  `t(d) = t(d_0)·(d_0/d)^{η}`、η = 2.0（default）**。
  出典: W. A. Harrison, *Electronic Structure and the Properties of Solids* (Dover, 1989), Eq.(20-5)
  — s,p 系の普遍値は d⁻²（Kashikar/Nestoklon は s,p 基底で d 軌道なしのため d⁻² で十分）。
  感度: η ∈ {1.5, 2.0, 2.5} を CsPbI₃ で 1 回 sensitivity check → `results/shift_current/eta_sensitivity.md`。
  極性変位 δ で Pb-I_z(+z) 結合は `a/2-δ`、(-z) は `a/2+δ` と非対称になり、Harrison scaling 経由で
  ホッピングが非対称化 → 反転対称が破れる。
  <!-- 旧記述（出典要・撤回）: -->
## 5. 検証アンカー（F4; ★ = 完了）
1. ✅ **中心対称で消失**: 無歪み立方（δ=0）で σ⁽²⁾_abc ≈ 4.9e-15（機械精度）。3 方向（xxx/yyy/zzz）
   とも消失（`test_cubic_all_diagonal_components_vanish`）。**最重要・ハルシネーションproof**。
2. ✅ **極性変位で発現・|δ| で増大**: δ>0 で σ_{zzz}(ω)≠0、δ→0 で連続的に 0、|σ| が |δ| とほぼ線形
   増大（`test_polar_displacement_turns_on_and_scales`）。
3. **ピーク位置 = バンド端近傍**: σ⁽²⁾ の立ち上がりが直接ギャップ ~Eg（n_kpts 収束は F5 Production で確定）。

### ★ F4-3（Rice-Mele 解析閉形式; 符号・prefactor 確定）— **完了**
**A.** 2-band Rice-Mele 模型（Fregoso 2017 Eq.(D2): `H=t cos(ka/2)σx − δ sin(ka/2)σy + Δσz`）の
per-k 積分核を **Fregoso Eq.(D15) `Im[r^z_cv r^z_vc;z]=a³tδΔ/(32E³)` と全 k で rel<1e-7 一致**
（符号・magnitude とも）。`tests/test_shift_current_rice_mele.py`。
**B.** **w 項を落とすと 2-band 積分核は 0**（continuum 形が TB で誤り＝F3 の bug を検出・テスト化）。
**C.** δ=0 または Δ=0（反転対称）で消失。**D.** full σ_zzz(ω) は **t,δ,Δ>0 で負**（Fregoso Eq.(D16) 符号一致）、
ピークは下側バンド端 ω≈2E_min。→ **符号・prefactor は in-repo 一次閉形式で確定**。

### ★ F4-2（Tan & Rappe 2016 多バンド sanity check）— **完了（qualitative 一致）**
出典: `doi_10.1038_npjcompumats.2016.26.pdf`（Tan, Zheng, Young, Wang, Liu, Rappe, npj Comput Mater
2:16026; レビュー）。同論文の 1D SSH/Rice-Mele 模型 Eq.(14) `H=Σ[Δ(−1)^j c†c + (t+(−1)^jδ)c†c_{j+1}]`
の定性則を多バンド Nestoklon-polar CsPbI₃ で確認:
- **δ=0 or Δ=0 で σ 消失**（反転対称）— 一致。
- **δ→−δ で σ_zzz 符号反転**（"changing the sign of δ changes the direction of the shift current"）
  — 多バンドで σ_zzz(−δ)=−σ_zzz(+δ) を**機械精度**で確認（`test_polar_sign_reverses_under_displacement_flip`）。
- **|δ| 増大で |σ| 増大**（Fig.3）— 一致。
- 物理的起源: s↔p の spσ 結合は符号交替（Eq.14 の δ）— Nestoklon の Pb-s/I-p SK 結合に対応。
注: MAPbI₃ vs CsPbI₃-polar は別構造・別手法（DFT vs 経験 TB, 相対単位）のため**絶対振幅の比較は不可**、
符号・対称則・|δ| スケーリングの**定性照合**にとどめる（Cowork 1655 §2.5 の方針どおり）。

4. **(F4-1, 格下げ)** length gauge 同値性: F4-3/F4-2 で符号確定済みのため tiebreaker のみ（未実施）。
5. **絶対 μA/V² 較正**: Eq.(D12) の e³/ℏ⁴ prefactor 付与は F5 で実施（現状は積分核の自然単位＝相対）。

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
1. ~~symmetry breaker~~ → **解決（Cowork F2 review 承認）**: [001] 極性変位 (P4mm) を採用。§4 参照。
2. ~~SK 距離スケーリング指数 η_l の出典~~ → **解決（Cowork F2 review）**: Harrison universal
   η=2.0（Harrison 1989 Eq.20-5, s,p 系の d⁻²）を default、感度 η∈{1.5,2.0,2.5}。§4 参照。
3. ~~Young & Rappe / Tan & Rappe / Fregoso PDF~~ → **全て取得・検証済み**（correction #2 の正 ID）。
4. ~~covariant derivative の符号・prefactor（Aversa-Sipe 1995 入手不可）~~ → **解決（F4-3）**:
   Fregoso 2017 Eq.(C2)（in-repo 一次出典）の TB 形（w 項込み）を実装し、Rice-Mele 閉形式 Eq.(D15)/(D16)
   と機械精度一致で符号・prefactor 確定。Aversa-Sipe 1995 原典は不要に。
5. **残（F5）**: 絶対 μA/V² 較正（Eq.(D12) prefactor）、k グリッド収束（shift current は遅い）、9 材料スキャン。

## 参考文献（出典; 取得状況明記）
- **D. J. Passos, G. B. Ventura, J. M. V. P. Lopes, J. M. B. Lopes dos Santos**, "Nonlinear optical
  responses of crystalline systems: Results from a velocity gauge analysis", *Phys. Rev. B* **97**,
  235446 (2018); arXiv:1712.04924. — **primary 方法論（取得・検証済み）**。velocity gauge, Berry
  connection, covariant derivative, Blount 分解。
- A. M. Sheikhabadi, Z. Bagheri, A. Sadeghi, "Theory of nonlinear optical response", arXiv:2207.00331
  (2022). — **sub**（disorder 入り 2nd-order response の formalism。取得・検証済み）。
- S. M. Young, A. M. Rappe, *Phys. Rev. Lett.* **109**, 116601 (2012); arXiv:**1202.3168**.
  — shift current BPVE の第一原理公式（**取得・検証済み**: "First principles calculation of the
  shift current photovoltaic effect in ferroelectrics"）。
- J. E. Sipe, A. I. Shkrebtii, *Phys. Rev. B* **61**, 5337 (2000). — 非線形応答 k 空間表式（未取得; 式は Passos 2018 経由）。
- L. Z. Tan, F. Zheng, S. M. Young, F. Wang, S. Liu, A. M. Rappe, *npj Comput. Mater.* **2**, 16026
  (2016); DOI:10.1038/npjcompumats.2016.26（**取得・検証済み**, `doi_10.1038_npjcompumats.2016.26.pdf`）。
  — polar materials の shift current レビュー・**検証アンカー（MAPbI₃, F4 で精密照合）**。
- B. M. Fregoso, T. Morimoto, J. E. Moore, *Phys. Rev. B* **96**, 075421 (2017); arXiv:**1701.00172**.
  — shift vector の幾何学的解釈・gauge invariance（**取得・検証済み**）。**★ 本実装の一次出典**:
  Eq.(C2)（TB 用 generalized derivative, w 項込み）・Eq.(D2/D15/D16)（Rice-Mele 閉形式, F4-3 照合）。
- E. I. Blount, *Solid State Phys.* **13**, 305 (1962); *Phys. Rev.* **126**, 1636 (1962). — 統一限界。
- S. Rajpurohit et al., arXiv:2105.11310. — bulk photovoltaic 背景（既収集）。
