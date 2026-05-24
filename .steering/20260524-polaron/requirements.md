# requirements — F6 Fröhlich ポーラロン結合

**発行元:** `extention/03_tb-perovskite_spec.md` F6
**日付:** 2026-05-24
**PI 認可:** データは自分で OA 収集（出典明記・検証, 見つからなければスキップ）。

## スコープ
- Fröhlich α + 弱結合ポーラロン質量（先頭次）。完全 Feynman variational 移動度は未実装（intricate, cf. PolaronMobility.jl）→ flag。

## 引用（実在確認済み 2026-05-24, web。α 式は ar5iv 原典で精読）
| 文献 | 用途 | 確認 |
|---|---|---|
| Frost, PRB 96, 195202 (2017), arXiv:1704.05404 | α 式 + MAPbI₃ ベンチ（α=2.39/2.68） | ✅ ar5iv で式・値確認 |
| Sendner et al., Nat. Commun. 12, 4945 (2021), PMC8494801 | CsPbBr₃ ベンチ（α≈2, ε∞=4.8, ε_S=20.5, LO=19.2 meV, m*=0.22/0.24） | ✅ PMC で値確認 |
| Fröhlich 1954 / Feynman 1955,1962 | 原典・弱結合質量 1+α/6 | ✅ |

## 受け入れ条件（2 独立ベンチで前因子固定）
- α 式が MAPbI₃ α=2.39(e)/2.68(h) を <1% で再現。
- α 式が CsPbBr₃ α≈2 を再現（第 2 独立検証）。
- 単位変換・スケーリング・弱結合質量極限。
- 既存テスト不変。

## データ収集（PI 認可で実施）
`data/parameters/frohlich_polaron_params.json`: MAPbI₃（Frost）+ CsPbBr₃（Sendner）の cited 値。
他 CsBX₃（CsPbCl3/CsPbI3/Sn/Ge）は clean な ε_S/ε_inf ペア + LO が一次出典で揃わず未収集 → `_pending`。捏造防止で未計算。

## 結果
- `src/perovskite_tb/polaron.py` + `tests/test_polaron.py`（7 ケース, green）。docs §15, repository-structure 更新。
- データ: `data/parameters/frohlich_polaron_params.json`。
