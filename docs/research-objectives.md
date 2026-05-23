# 研究・開発目的定義書 (research-objectives)

## 背景

ハライドペロブスカイト `ABX₃`（A = Cs, MA, FA …；B = Pb, Sn, Ge；X = Cl, Br, I）は、
太陽電池・LED・光検出器・レーザなどの光デバイス材料として急速に注目されている。
デバイス設計やナノ構造（量子ドット・薄膜・層状構造）の電子状態を理解するには、
バンド構造を**安価かつ再現性高く**計算できる手法が必要である。第一原理計算 (DFT) は
ナノ構造には計算コストが大きく、経験的タイトバインディング (ETB) / Slater-Koster (SK)
法が有力な代替となる。

## 目的

`references/pdfs` に蓄積される論文から、ペロブスカイトのバンド構造を記述する
**タイトバインディングのアルゴリズムとパラメータ**を精査し、それを **Python で実装**して
**論文の値を厳密に再現**する。再現性のため、用いた物性値（パラメータ）を出典付きで保管し、
材料・パラメータ・k 経路を **JSON で入力**できる形にする。

## 解決したい課題

1. ペロブスカイトのバンド構造（特に直接ギャップ・スピン軌道分裂）を、論文に裏付けられた
   パラメータで安価に再現する。
2. 異なる材料（CsBX₃ 9種など）を JSON 差し替えだけで計算できるようにする。
3. **ハルシネーションを排除**し、すべての数式・数値に出典を持たせ、検証で裏付ける。

## 対象とする現象・系・問題領域

- 立方晶（α相, Pm-3m）の無機ハライドペロブスカイト `CsBX₃`（B=Ge/Sn/Pb, X=Cl/Br/I）。
- 立方晶 `CsPbI₃` のバルクバンド構造（DFT 再現セット・実験補正セット）。
- バンドギャップ（R点直接ギャップ）、伝導帯スピン軌道分裂、高対称点エネルギー。

> 低対称相（正方晶 β・斜方晶 γ）、2D/層状系、ナノ構造表面は将来の拡張対象。
> 現時点では実装していない（[verification-validation.md](verification-validation.md) のスコープ参照）。

## 想定ユーザー

ペロブスカイト光デバイスを扱う研究者・エンジニア・学生。バンド構造の素早い見積もりや、
パラメータ感度の検討、ナノ構造モデルの出発点として用いる。

## 成功の定義

- **精度**: 採用論文が明示する数値（バンドギャップ・SO 分裂・解析的固有値）を
  許容誤差内（ギャップで ≤ 10 meV、解析式照合で機械精度）で再現する。
- **再現性**: パラメータは出典付きで保管され、結果には実行メタデータ（コミット・日時・
  パラメータ）が付与される。同じ入力から同じ結果が再現できる。
- **計算時間**: 単一材料のバンド構造（数百 k 点、80×80 行列）が秒オーダー。
- **拡張性**: 材料・パラメータは JSON 差し替えで追加できる。

## スコープと制限

| 含む | 含まない（現時点） |
|---|---|
| 立方晶 CsBX₃ の SK-TB（13/4軌道） | 低対称相（正方/斜方） |
| 立方晶 CsPbI₃ の Jancu sp³d⁵s\* ETB | 有機カチオン (MA/FA) の明示的扱い |
| バルクバンド構造・ギャップ・SO分裂 | 表面・界面・ナノ構造、歪み |
| スピン軌道相互作用（オンサイト L·S） | 励起子・光学応答・GW/BSE、輸送 |

## 採用論文（出典）

1. R. Kashikar, M. Gupta, B. R. K. Nanda, *A Generic Slater-Koster Description of the
   Electronic Structure of Centrosymmetric Halide Perovskites*, arXiv:2101.08562 (2021).
2. M. O. Nestoklon, *Tight-binding description of inorganic lead halide perovskites in
   cubic phase*, arXiv:2012.14705 (2021).

関連する方法論の原典:
- J. C. Slater, G. F. Koster, *Simplified LCAO Method for the Periodic Potential Problem*,
  Phys. Rev. **94**, 1498 (1954).
- J.-M. Jancu, R. Scholz, F. Beltram, F. Bassani, *Empirical spds\* tight-binding
  calculation for cubic semiconductors*, Phys. Rev. B **57**, 6493 (1998).

> 収集論文の全一覧は `references/references.md`。今後たまる論文は定期的に確認し、
> 新たな TB モデル・パラメータがあれば本書とパラメータ JSON に取り込む。
