# requirements — F14-B Berry 位相分極（KSV）

**発行元:** `extention/03_tb-perovskite_spec.md` F14 モード B
**依存:** `topology.wilson_loop`/`polarization_phase`、`slab._orbital_z`（ゲージ）。

## 引用（実在確認済み 2026-05-24, web）
| 文献 | 確認 |
|---|---|
| King-Smith, Vanderbilt, PRB 47, 1651 (1993) | ✅ |
| Su, Schrieffer, Heeger, PRL 42, 1698 (1979)（SSH テスト模型） | ✅ |

## 受け入れ条件
- SSH: Zak 0/π 量子化 + 転移で π ジャンプ（厳密アンカー）。
- Rice-Mele: 反転破れで連続シフト。
- ペロブスカイト電子 Zak が finite・実・決定論的。

## honest 限界（重要）
ペロブスカイトの返り値は**電子 Berry 位相のみ**。物理量子化分極はイオン寄与+分極量子が必要（total のみ gauge 不変・量子化）。
立方の裸電子 Zak は X_z(z=a/2) ゲージオフセットで 0/π にならない → 量子化は主張せず、量子化は SSH で検証、用途は ΔP。

## 結果
- `src/perovskite_tb/polarization.py` + `tests/test_polarization.py`（4 ケース, green）。docs §18, repository-structure 更新。
