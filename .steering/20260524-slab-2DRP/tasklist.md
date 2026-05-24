# tasklist — F5 / F13 / F14-A slab.py

## 実装 ✅
- [x] `_orbital_z`, `layer_blocks`, `reconstruct_3d`, `slab_hamiltonian`, `slab_eigenvalues`, `slab_gap`

## V&V ✅（`tests/test_slab.py`, 8 ケース）
- [x] 層ブロック再構成 == 3D H（機械精度）
- [x] 周期スタック == k_z=2πm/(Na) の 3D バンド和（F13）
- [x] ミニバンド崩壊（inter_layer→0）
- [x] open スラブ閉じ込め収束（F5）
- [x] Stark: E=0 回復, 幅 ~eE(N−1)a（F14-A）
- [x] 【T1-1】Blancon トレンド比較: 減衰指数 p_TB≈0.93 vs p_exp≈0.85（15%以内）

## docs ✅
- [x] `docs/numerical-methods.md` §17
- [x] 引用訂正: 2D RP 量子閉じ込め = ChemPhysChem 15,3733（JPCC 118,11566 は誤帰属）; E_g(n)=Nat.Commun.9,2254(2018)（Science 2017 は別論文）
## commit ✅ — push 済
## honest 限界
- 絶対 E_g(N) は D（無機 CsPbI₃ vs MAPbI₃系RP + SK-TB）。Blancon 比較は `.steering/20260524-additional-validation/`。
