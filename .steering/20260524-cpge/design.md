# design — F7 cpge.py

## モジュール構成 `src/perovskite_tb/cpge.py`
- `cross_gap_connection(V, evals, n, m)`: r^a_{nm} = −i v^a_{nm}/(E_n−E_m)（バンド間Berry接続）。
- `berry_curvature_vector(evals, evecs, dH, band)`: Ω^j_n を `berry.berry_curvature_kubo` で構成。
- `cpge_tensor(kpts, H_fn, dHk_fn, omega, eta, ...)`: de Juan 一般式
  β_ij = π Σ_k Δ^i_{nm} w · (−Im[r×r])。**batched eigh + einsum("knmi,knmj->ij")** でベクトル化。
- `cpge_tensor_2band(...)`: 2バンド Berry 曲率形（検証用）。

## 設計判断
- ε縮約は −Im(np.cross(r_nm, r_mn))（純虚数=iΩ なので real ではなく imag）。
- 符号は Xiao/Berry 規約に整合（cross-check 済）。ħ=e=1, 前因子 π。絶対値は τ/規約依存でスコープ外(D)。
