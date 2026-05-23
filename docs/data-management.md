# データ管理規程 (data-management)

## 入力データ

### パラメータ（物性値）
- 配置: `data/parameters/*.json`。出典は各 JSON 内の `source` と `data/parameters/SOURCES.md`。
- 形式: `model_id`, `model_kind`, `source`（著者・タイトル・arXiv・表番号・単位・DFT 基準）、
  `parameter_keys`（各キーの物理的意味）、材料/パラメータセット別の数値。
- **方針**: 論文記載値を**改変せず転記**。誤植が疑われても値は変えず `anomaly` に注記。
  これにより「使った物性値はいつでも再現できる」ことを保証する（ハルシネーション防止）。

### k 経路設定
- 配置: `configs/*.json`（高対称点列・サンプル数）。

### 参照論文
- 配置: `references/pdfs/arxiv_<id>.pdf`（自動収集、計 245 MB / 49 本）。一覧 `references/references.md`。
- **大容量のため Git 本体にはコミットしない**（`.gitignore`）。来歴は arXiv ID で保持し、
  `arxiv.org/pdf/<id>.pdf` から再取得可能。

## 出力データ

- 配置: `results/<model>/<material>.png` と同名 `.json`（再現性メタデータ）。
- 命名: モデル・材料・パラメータセットが分かる名前（例 `CsPbI3_sp3d5sstar.png`）。
- 大容量の生バンドデータ（`.npz/.npy`）は Git 管理外（`.gitignore`）。図 (PNG)・
  メタデータ (JSON) は軽量なので必要に応じてコミット可。

## 再現性メタデータ（必須）

各結果 JSON（`src/perovskite_tb/_meta.py`）に以下を付与:
- `timestamp_utc`, `git_commit`（dirty 判定付き）, `package_version`,
  `python` / `numpy` / `scipy` バージョン, `platform`,
- `model_id`, `model_kind`, `material`, `parameter_set`, `lattice_constant_a`,
  使用した **`params`（全数値）**, `kpath_segments`, `n_filled`, `fundamental_gap`。

→ 結果ファイル単体から、どのコミット・どのパラメータ・どの環境で計算したかが分かる。

## 計算環境のスナップショット

- 依存は `requirements.txt` / `pyproject.toml` に記載。
- 結果メタデータに numpy/scipy/python の実バージョンを記録。
- 厳密固定が必要な場合は `pip freeze > results/<run>/pip-freeze.txt` を併用（任意）。

## 乱数シードの管理

- 本手法は決定論的（固有値問題）で乱数を使わない。テスト内で乱数を使う箇所
  （SK パリティ検証）は `np.random.default_rng(0)` でシード固定し再現性を担保。

## データの来歴 (provenance)

- パラメータ → 論文（arXiv ID・表番号）→ `references/references.md` → PDF。
- 結果 → メタデータ JSON（コミット・パラメータ）→ パラメータ JSON → 論文。
  この鎖により任意の図・数値を出典までたどれる。

## バージョニング

- コード・パラメータ・ドキュメントは Git で管理。大容量データは対象外（上記）。
- 将来データが増える場合は Git LFS / DVC を検討（現状は不要）。
