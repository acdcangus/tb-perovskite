# design — berry.py

## モジュール構成 `src/perovskite_tb/berry.py`

### 低レベル（行列演算, 模型非依存）
- `velocity_matrix(evecs, dHk_alpha) -> Vα`:  Vα = U† (∂H/∂k_α) U（バンド基底の速度行列要素）。
- `berry_curvature_kubo(evals, evecs, dHx, dHy, *, degen_tol=1e-6) -> Ω[n]`:
  Xiao 2010 Eq.(1.13): Ω_n^{xy} = −2 Σ_{m≠n} Im(Vx[n,m] Vy[m,n]) / (E_n−E_m)²。
  準縮退 (|E_n−E_m|<degen_tol) は和から除外（特異点回避; 値は NaN ではなく 0 寄与、bands 縮退時は警告）。
- `spin_berry_curvature_kubo(evals, evecs, jx, dHy, ...)`: 上の Vx を **スピン流行列** Jx=U† j^z_x U に置換。
  j^z_x = ½ {s_z, v_x} = ½ (s_z v_x + v_x s_z)（Sinova 2015）。
- `link_variable_chern(eigvec_grid) -> C`: Fukui 2005 法。占有多様体の重なり行列式 U_μ(k)=det⟨u(k)|u(k+μ̂)⟩/|…|、
  field strength F_12 = Im ln(U_1 U_2(k+1) U_1(k+2)^{-1} U_2^{-1})、Chern = (1/2π)Σ F_12。非アーベル（多バンド占有）対応。

### 高レベル（積分・伝導率）
- `anomalous_hall_sum(curv_grid, occ) -> Σ`:  Σ_k Σ_{n∈occ} Ω_n（次元なし BZ 和）。
- `spin_hall_sum(...)`: spin Berry 曲率版。
- 単位付き σ は係数 −(e²/ℏ)·(1/V)·(BZ measure) を別関数で（cubic では結果 0 が主検証なので係数は文書化のみ）。

### 模型ヘルパ（テスト/スキャン用, 既存再利用）
- `kashikar13_batch(kpts, params, a) -> (H[k], dHx[k], dHy[k], dHz[k])`:  既存 `models_kashikar.kashikar13_hamiltonian` と
  `velocity.dH_dk_kashikar13` をループ/バッチ呼び出し。
- `spin_z_operator(n_orb=13) -> Sz`:  spin-major 基底 ⇒ Sz=½ diag([+1]*13 + [−1]*13)（_soc/ models と整合）。Sx,Sy も kron(σ,I)/2。
- テスト専用模型は test 内に閉じる（Dirac, QWZ）。

## 既存との整合
- spin-major 基底（`kashikar13_hamiltonian` の np.kron(eye(2),H0)+SOC）に一致させ Sz を構築。
- ℏ=1（`velocity_from_dHdk` の既定）。v=∂H/∂k。
- `_constants.py` は今回不要（無次元検証主体）。SPDX ヘッダ付与。

## V&V（tests/test_berry.py）
1. `test_dirac_berry_curvature_matches_analytic`: H=d·σ, Ω₋ vs +m/(2|d|³) を複数 k で（rtol 1e-6）。
2. `test_dirac_berry_curvature_sign_upper_lower`: Ω₊ = −Ω₋。
3. `test_qwz_chern_phase_diagram`: Fukui 法 Chern が m=1→−1, m=−1→+1, m=3→0（21×21 グリッドで整数, atol 1e-6）。
4. `test_kubo_vs_fukui_consistency`: QWZ gapped 点で Kubo BZ 和 ≈ Fukui Chern（粗グリッドで概一致）。
5. `test_cubic_perovskite_PT_zero_curvature`: Kashikar-13 立方 CsPbI₃, 一般 k で Ω(k)≈0（atol 1e-8）→ AHC=0。
6. `test_velocity_matrix_hermiticity` / `test_curvature_real`。
7. `test_spin_berry_curvature_runs_real`: CsPbI₃ で spin Berry 曲率が実数・有限（絶対値検証は限界として skip 理由明記）。

## docs 更新
- `docs/numerical-methods.md`: 「Berry 曲率・AHC・SHC」節（式 + 出典 + 離散法 + 限界）。
- `docs/repository-structure.md`: `src/perovskite_tb/berry.py` を追加。

## 影響範囲
- 新規ファイルのみ。既存 import/挙動変更なし → 231 テスト不変。Production 数値不変。
