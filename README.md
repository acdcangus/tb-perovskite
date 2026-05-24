# perovskite-tb — ペロブスカイトのタイトバインディング バンド構造計算

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

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

## 計算できる物性（共有 `velocity.py` の上に構築）

| カテゴリ | モジュール | 物理量 |
|---|---|---|
| g 因子 / 光学 | `g_factor.py`, `optical.py` | Landé g 因子、複素誘電関数 ε(ω) |
| 非線形・光電流 | `shift_current.py`, `cpge.py` | シフト電流 / BPVE、円偏光光起電力 (CPGE) |
| Berry 位相・トポロジー | `berry.py`, `topology.py`, `polarization.py` | Berry 曲率・AHC・SHC・離散 Chern、Wilson ループ / WCC、KSV 分極 |
| スピン軌道輸送 | `rashba.py`, `edelstein.py` | Rashba 分裂 α_R、Edelstein 電流誘起スピン分極 |
| 輸送・電子格子 | `thermo.py`, `polaron.py` | Boltzmann 熱電 (S/σ/κ_e)、Fröhlich ポーラロン結合 |
| 励起子・構造 | `exciton.py`, `bandengr.py`, `slab.py` | Wannier-Mott 励起子、歪みバンド工学、2D RP スラブ / 超格子 / Stark |

各物性の式・出典・V&V は [docs/numerical-methods.md](docs/numerical-methods.md)（§9–§18）と
[extention/08_tb-perovskite_implementation_report.md](extention/08_tb-perovskite_implementation_report.md) を参照。
**追加機能の物理・検証・定量結果・コアTB結合 end-to-end テスト**をわかりやすくまとめた解説レポート →
[extention/10_additional_features_report.md](extention/10_additional_features_report.md)。

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

## License

This project is licensed under the MIT License — see [LICENSE](LICENSE) for details.
新規ソースファイルには冒頭に `# SPDX-License-Identifier: MIT` を付与します（[docs/development-guidelines.md](docs/development-guidelines.md) 参照）。
