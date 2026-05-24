# tasklist — R4-STD-2 / R4-STD-3

- [x] `src/perovskite_tb/_constants.py` 新規作成（`HBAR2_OVER_M0 = 7.619964`, SPDX ヘッダ）
- [x] `exciton.py`: 定義削除 → `from ._constants import HBAR2_OVER_M0`
- [x] `optical.py`: 同上
- [x] `velocity.py`: 同上（re-export, noqa F401）
- [x] `g_factor.py`: `from ._constants import HBAR2_OVER_M0 as C_HBAR2_OVER_M0`
- [x] `compute_g_factor` docstring に Roth-Lax-Zwerdling 1959 anchor 追加（R4-STD-3）
- [x] `pytest` 全 231 テスト通過確認（231 passed in 62.85s）
- [x] 定数の grep で重複定義が `_constants.py` のみになったこと確認（exciton L22 残りは docstring 説明文）
- [x] smoke test: exciton/optical/velocity.HBAR2_OVER_M0 + g_factor.C_HBAR2_OVER_M0 == 7.619964 統一
- [ ] commit + push（key leak ガード）← 本コミットで実施

## deferred（本サイクル外・追跡）
- [ ] R4-STD-1: `shift_current.py` 内部 helper 型ヒント（戻り値型を関数本体で検証してから付与）
