# tasklist — F6 polaron.py

## 実装 ✅
- [x] `frohlich_alpha`（SI 前因子）, `weak_coupling_polaron_mass`, 単位変換
- [x] `data/parameters/frohlich_polaron_params.json`（出典付き; MAPbI₃, CsPbBr₃）
- [x] 【T1-3】`bandstructure.effective_mass`（全9材料 TB m*）+ TB駆動 α（CsPbBr₃=1.66）

## V&V ✅（`tests/test_polaron.py`, 10 ケース）
- [x] MAPbI₃ α=2.39(e)/2.68(h) を **<1%**（Frost 2017）— A
- [x] CsPbBr₃ α≈2（Sendner 2021）, 単位変換, √m*・(1/ε∞−1/ε_S) スケーリング, 弱結合質量 1+α/6
- [x] 【T1-3】合成放物線で m* 厳密回復, R点等方性, TB駆動 α=1.66（差−17%＝√(0.151/0.22)）

## docs ✅
- [x] `docs/numerical-methods.md` §15
## commit ✅ — push 済（API キー漏洩なし; キーは gitignore）
## honest 限界
- 9材料αマップは **Cs系無機の誘電/LO 一次文献が存在しない**ため部分（捏造回避）。MA系の Sendner 2016/Wright 2016 では代用不可。
- 中間結合 α~2 の移動度は完全 variational 要（未実装）。詳細は `.steering/20260524-additional-validation/`。
