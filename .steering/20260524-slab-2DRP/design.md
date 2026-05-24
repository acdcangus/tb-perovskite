# design — F5 / F13 / F14-A slab.py

## モジュール構成 `src/perovskite_tb/slab.py`
- `_orbital_z(a)`: 26軌道の cell 内 z 位置（X_z は a/2, 他 0）。
- `layer_blocks(params, a, kx, ky)`: ゲージ変換 U(k_z)=diag(e^{-ik_z z_α}) で 2π/a 周期化 → 厳密 Fourier 分解で H_∥ と inter-cell T。
- `reconstruct_3d(Hpar, T, kz, a)`: H_∥ + T e^{ik_z a} + h.c.（自己検証用）。
- `slab_hamiltonian(Hpar, T, N, periodic, onsite_shift)`: ブロック三重対角（open/periodic, Stark シフト）。
- `slab_eigenvalues` / `slab_gap`: N セルスラブの固有値・閉じ込めギャップ（e_field_z で Stark, inter_layer_scale でミニバンド）。

## 設計判断
- spacer/passivation は **hard-barrier (open BC) 理想化**（Even 2014）。tilting なし。
- F5=open スラブ E_g(N), F13=periodic スタック, F14-A=Stark。F14-B(バルク分極)は polarization.py（別作業）。
- 絶対 E_g(N) は SK-TB/Blount caveat。トレンドのみ主張。
