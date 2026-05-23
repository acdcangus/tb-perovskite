# 技術仕様書 (architecture)

## テクノロジースタック

- **言語**: Python (>= 3.10)。Python 3.14 でも動作確認。
- **主要ライブラリ**:
  - `numpy`（配列・線形代数 `linalg.eigvalsh`。**唯一の機能的依存**）
  - `matplotlib`（バンド図, 非対話 Agg バックエンド）
  - `scipy`（宣言済み依存だが現状は機能的に未使用。`_meta.py` がバージョン記録のために
    任意 import するのみ。将来の数値拡張用に保持）
  - `pytest`（検証・V&V テスト）
  - `pymupdf`（参照論文 PDF からのテキスト抽出; 開発時のみ）
- **数値精度**: 倍精度（float64 / complex128）。
- **計算環境**: 単一 CPU、ノート PC で十分（行列サイズ 8〜80、k 点数 数百）。
  GPU/MPI/HPC は不要。並列化も現時点では不要。

## モジュール構成（`src/perovskite_tb/`）

| モジュール | 役割 |
|---|---|
| `slater_koster.py` | 一般 Slater-Koster 二中心積分（s/p/d/s\*, 任意方向） |
| `_soc.py` | p 軌道スピン軌道 L·S（Δ/3 規約 = 3λ 分裂） |
| `models_kashikar.py` | Kashikar 13/4軌道ハミルトニアン + Eq.9 解析式 |
| `models_nestoklon.py` | Nestoklon sp³/sp³d⁵s\*（SK + 八面体ジオメトリ + 両副格子 SOC） |
| `models.py` | モデルレジストリ（`model_kind` → builder, `n_filled`） |
| `kpath.py` | 立方 BZ 高対称点・k 経路サンプリング |
| `io_params.py` | パラメータ JSON ロード・材料/パラメータセット選択 |
| `bandstructure.py` | 対角化・バンド構造・ギャップ算出 |
| `plotting.py` | バンド図（Agg） |
| `cli.py` / `__main__.py` | CLI（`band` / `gap` サブコマンド） |
| `_meta.py` | 再現性メタデータ（git コミット・版・入力） |

## データフロー

```mermaid
graph LR
  J[data/parameters/*.json] --> IO[io_params]
  C[configs/*.json k経路] --> KP[kpath]
  IO --> M[models: builder + n_filled]
  M --> BS[bandstructure: H(k) 対角化]
  KP --> BS
  BS --> GAP[ギャップ算出]
  BS --> PLT[plotting]
  PLT --> PNG[results/*.png]
  GAP --> META[_meta]
  META --> JSON[results/*.json 再現性メタデータ]
```

## ハミルトニアン構築の流れ

1. `io_params.get_material` が JSON から材料/パラメータセットを選び、フラットな
   数値辞書 + 格子定数 `a` + 基底を返す。
2. `models.build_model` が `model_kind` に応じて builder（`H(kvec)`）と `n_filled` を生成。
3. `bandstructure.compute_band_structure` が k 経路の各点で `H(k)` を対角化。
4. `cli` が図と再現性メタデータ JSON を `results/` に出力。

## インタフェース規約

- builder は純関数 `H(kvec_cart: ndarray(3,)) -> ndarray(N,N) complex`（Hermite）。
- 行列の基底順序は spin-major（全軌道↑→↓）。各モデルのオンサイト/軌道順序は
  各モジュール docstring に明記。
- パラメータ JSON は `model_id`, `model_kind` を必須とし、出典メタデータを保持する
  （[data-management.md](data-management.md)）。

## パフォーマンス

- 1 材料のバンド構造（~600 k 点 × 80×80 対角化）: 秒オーダー。
- スケーリング: k 点数に線形、行列サイズに `O(N³)`。
- 現状の問題規模では最適化不要。将来 2D/超格子で N が増える場合は、
  k 並列化（`multiprocessing` / ベクトル化）を検討。
