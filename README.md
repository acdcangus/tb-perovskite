# perovskite-tb — ペロブスカイトのタイトバインディング バンド構造計算

立方晶ハライドペロブスカイト `CsBX₃` (B = Ge, Sn, Pb; X = Cl, Br, I) および
鉛ハライドペロブスカイトの電子バンド構造を、**経験的タイトバインディング (ETB) /
Slater-Koster 法**で計算する Python パッケージです。

> **設計原則: 論文の値を厳密に再現する。ハルシネーション禁止。**
> すべてのモデル方程式・パラメータは査読論文（または arXiv プレプリント）に出典を持ち、
> `data/parameters/*.json` に出典メタデータ付きで保管されます。実装は論文が明示する
> 解析式・数値（バンドギャップ等）に対して自動テストで検証されます（`tests/`）。

## 実装しているモデル（すべて出典付き）

| モデル | 軌道基底 | 対象材料 | 出典 | 検証アンカー |
|---|---|---|---|---|
| Kashikar 13軌道 | B-{s,p} + X-p (13) + SOC | CsBX₃ 全9種 (cubic) | Kashikar, Gupta & Nanda, arXiv:2101.08562 | R点固有値 解析式 (Eq.9) |
| Kashikar 4軌道 最小 | B-{s,p} (4) + SOC | CsBX₃ 全9種 (cubic) | 同上 (Table IV) | バンドギャップ閉形式 |
| Nestoklon sp³ | (s,p)×(Pb,I) + SOC | CsPbI₃ (cubic) | Nestoklon, arXiv:2012.14705 | R点ギャップ ≈ DFT 1.017 eV |
| Nestoklon sp³d⁵s\* | (s,p,d,s\*)×(Pb,I) + SOC | CsPbI₃ (cubic) | 同上 (Table I) | R点ギャップ / SO分裂 1.48 eV |

材料・パラメータ・k 経路はすべて **JSON で入力**します。

## クイックスタート

```bash
pip install -r requirements.txt          # numpy, scipy, matplotlib, pytest
pip install -e .                          # パッケージをインストール

# バンド構造を計算してプロット
python -m perovskite_tb band \
    --params data/parameters/kashikar2021_cubic_13orb.json \
    --material CsPbI3 \
    --config configs/cubic_MRXGM.json \
    --out results/CsPbI3_kashikar13.png

# 検証テスト（論文の値を再現できているか）
pytest -q
```

## ディレクトリ構成（CLAUDE.md 準拠）

```
src/perovskite_tb/   実装本体
data/parameters/     論文から抽出したパラメータ (JSON + 出典)
configs/             実行設定 (材料・モデル・k経路)
tests/               単体テスト・V&V テスト（論文値の再現確認）
docs/                永続ドキュメント（理論・数値解法・V&V 計画 等）
.steering/           作業単位ドキュメント
results/             計算結果（バンド図・数値）
references/          収集論文と文献リスト (references.md)
RESULTS.md           ★ 現在の進捗と再現結果のサマリ（ここを見れば状況が分かる）
```

## ステータス

進捗・再現結果の最新サマリは **[RESULTS.md](RESULTS.md)** を参照してください。
