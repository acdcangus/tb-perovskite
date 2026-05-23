# 初回実装 設計 (design)

**作業ID:** 20260523-initial-implementation

## モデル選定理由

`references/` の49本を機械スクリーニング（TB/ペロブスカイト/パラメータのキーワード密度）し、
**TBアルゴリズムとパラメータが完全に明示され、かつ検証可能な数値を持つ**論文を選定した。

- **Kashikar (2101.08562)**: 13軌道 / 4軌道の Slater-Koster ハミルトニアンが式 (3)-(8) で
  陽に与えられ、R点固有値の**解析式 (9)** が独立に導出されている。これにより、数値実装の
  正しさを解析式との一致で**厳密に**検証できる（ハルシネーション排除に最適）。9材料を網羅。
- **Nestoklon (2012.14705)**: Jancu sp³d⁵s\* 最近接 TB。DFT/実験のバンドギャップ・SO分裂が
  **明示された数値**で与えられ、実験と直接比較できる「ゴールドスタンダード」。CsPbI₃。

## 結晶構造とジオメトリ

立方晶 ABX₃ (Pm-3m)。Cs は基底から除外（Boyer-Richard, Nestoklon に従う）。
- B (cation) を原点に置く。simple-cubic 副格子（B-B 距離 a）。
- 3つのハライド X を各軸上 a/2 に配置（X1 on x, X2 on y, X3 on z）。
- 最近接 B-X 結合（長さ a/2、立方軸方向）。

## ハミルトニアン構築

### ゲージ
**原子ゲージ** `H_ab(k) = Σ_R t_ab(R) exp(i k·(R + τ_b - τ_a))` を採用。
B を原点に置くと Kashikar の簡約因子 `S_d=2i sin(k_d a/2)`, `C_d=2cos(k_d a/2)` を厳密に再現。
B-B 項は full-a 位相（`cos(k_d a)`, `sin(k_d a)`）で、R点で B-p 三重項が混成しない
（Eq.9 が成立する）よう構成する。固有値はゲージ不変なので物理量に影響しない。

### Kashikar 13軌道
式 (4)-(8) を逐語的に転記。基底順: B-s, B-{px,py,pz}, X1{p}, X2{p}, X3{p}。
X-X ブロックはオンサイト対角（式7）。SOC は B-p に `λL·S`（式10）。

### Nestoklon sp³ / sp³d⁵s\*
一般 Slater-Koster 二中心積分（Slater-Koster 1954 Table I）を実装し、
立方軸方向の B-X 結合について評価。cation/anion で積分が異なる（極性結合）ため、
順序対 (typeA→typeB) ごとに正しい積分を選択する。ゼロ固定積分（Table I キャプション）を尊重。

### スピン軌道相互作用（重要な規約）
両論文とも λ は「Δ/3」型係数で、**p 軌道の分裂 = 3λ**。Kashikar 式(10) の行列要素は
大きさ {±i, ±1} = 2·(L·S) なので `H_SO = λ·(2 L·S)`。実装は `soc_p_matrix(2λ)`。
固有値 {+λ (×4, j=3/2), -2λ (×2, j=1/2)}。Pb で 3λ≈1.5 eV（Nestoklon の 1.48 eV と整合）。

## 電子占有数 (n_filled)

立方ハライドペロブスカイトの価電子数 VEC=20（Kashikar Sec. II）。
- Kashikar 13軌道（26状態）: 20 占有。R点で E1(2)+E2(16)+E4(2)=20。CBM=E3 (B-p)。
- Kashikar 4軌道（8状態）: 2 占有（s 由来反結合帯）。
- Nestoklon sp³d⁵s\*（80状態）/ sp³（32状態）: 26 占有
  （I⁻ 5s²5p⁶ ×3 = 24、Pb²⁺ 6s² = 2）。CBM=Pb-p。

## モジュール構成

```
src/perovskite_tb/
  _soc.py            p軌道 L·S（Δ/3規約対応）
  slater_koster.py   一般SK二中心積分（Nestoklon用）
  models_kashikar.py Kashikar 13/4軌道（陽に転記）+ Eq.9解析式
  models_nestoklon.py Nestoklon sp³/sp³d⁵s\*（SK+ジオメトリ）
  models.py          モデルレジストリ（model_kind→builder, n_filled）
  kpath.py           立方BZ高対称経路
  io_params.py       JSON ロード
  bandstructure.py   対角化・ギャップ
  plotting.py        バンド図
  cli.py / __main__.py  CLI
  _meta.py           再現性メタデータ
```

## 影響範囲

新規リポジトリのため既存テストへの影響なし。各モデルに単体テスト + V&V テストを付す。

## V&V 計画への追記

- `tests/test_kashikar.py`: Eq.9（全9材料）、SOC分裂=3λ、4軌道ギャップ閉形式。
- `tests/test_soc.py`: L·S 固有値・規約。
- `tests/test_slater_koster.py`: 軸方向の SK 要素を手計算値と照合、パリティ対称性。
- `tests/test_nestoklon.py`: R点ギャップ 1.017 eV（DFT セット）、実験補正 1.65/2.75 eV、SO分裂。
