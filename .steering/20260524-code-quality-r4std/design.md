# design — R4-STD-2 / R4-STD-3

## R4-STD-2: 定数一元化

### 新規ファイル `src/perovskite_tb/_constants.py`
```python
HBAR2_OVER_M0 = 7.619964  # hbar^2/m0 in eV*Angstrom^2 (= 2 * 3.80998 eV.A^2)
```
値は既存 4 モジュールと**完全一致**（変更なし）。

### 各モジュールの変更（定義 → import に置換）
| ファイル | 変更前 | 変更後 | 公開名の保持 |
|---|---|---|---|
| `exciton.py` | `HBAR2_OVER_M0 = 7.619964` | `from ._constants import HBAR2_OVER_M0` | `exciton.HBAR2_OVER_M0` 維持（import で module 属性化）→ test_exciton.py OK |
| `optical.py` | 同上 | `from ._constants import HBAR2_OVER_M0` | — |
| `velocity.py` | 同上（局所未使用だが API 保持のため re-export） | `from ._constants import HBAR2_OVER_M0` | — |
| `g_factor.py` | `C_HBAR2_OVER_M0 = 7.619964` | `from ._constants import HBAR2_OVER_M0 as C_HBAR2_OVER_M0` | `g_factor.C_HBAR2_OVER_M0` 維持 → scripts/plot_ge_universality.py OK |

**設計判断:** import エイリアスで既存の使用名（`HBAR2_OVER_M0` / `C_HBAR2_OVER_M0`）と module 属性アクセスを完全保持 → 使用箇所のロジック変更ゼロ。リスク最小。

## R4-STD-3: docstring 式番号 anchor
- `g_factor_kp`: 既に "(Kirstein 2021, Eqs. 5,6)" あり → 変更不要。
- `compute_g_factor`: docstring 冒頭に「Roth, Lax & Zwerdling, Phys. Rev. 114, 90 (1959)」の anchor を 1 行追加（モジュール docstring の M_gamma 式を参照）。出典はモジュール docstring に既出のもののみ使用。

## 影響範囲
- 数値計算ロジック: 変更なし（定数値同一、使用名同一）。
- テスト: test_exciton.py の `ex.HBAR2_OVER_M0` 参照は import 再エクスポートで維持。
- Production bundle: 影響なし（数値不変）→ rerun 不要。
- V&V: 既存 231 テストで回帰確認。
