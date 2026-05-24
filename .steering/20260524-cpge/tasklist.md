# tasklist — F7 cpge.py

## 実装 ✅
- [x] `cross_gap_connection` / `berry_curvature_vector` / `cpge_tensor`（一般式, ベクトル化）/ `cpge_tensor_2band`
- [x] `berry` 再利用、Levi-Civita ε、Gaussian δ

## V&V ✅（`tests/test_cpge.py`, 4 ケース）
- [x] 2バンド簡約 −Im(ε_jkl r^k r^l)=Ω^j（解析一致）
- [x] 中心反転対称 → β=0
- [x] Weyl 量子化: Tr[β] ω非依存プラトー、カイラリティ符号反転、|Tr|≈1/4π を 20%（A部分）

## 実装中の修正（記録）
- ε縮約 np.real → ~0（純虚数）→ −np.imag(np.cross) に修正、符号を Berry 規約に整合。
- Weyl テスト高速化: batched eigh + einsum + batch-aware builders（8.7s→0.83s）。旧ループと 8.3e-16 一致。

## docs ✅
- [x] `docs/numerical-methods.md` §14
## commit ✅ — push 済（key leak なし）
## deferred
- 材料絶対値は D（Berry 規約 + Blount）。F8 SHG は別途（χ² が intricate）。
