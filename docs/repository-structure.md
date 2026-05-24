# リポジトリ構造定義書 (repository-structure)

```
.
├── CLAUDE.md                  プロジェクトメモリ（標準ルール）
├── README.md                  概要・クイックスタート
├── RESULTS.md                 ★ 進捗と論文値の再現結果サマリ（携帯確認用）
├── pyproject.toml             パッケージ定義（src レイアウト, pytest 設定）
├── requirements.txt           依存関係
├── .gitignore                 PDF・生成大容量データ・キャッシュを除外
│
├── src/perovskite_tb/         ソースコード（実装本体）
│   ├── slater_koster.py / _soc.py / _constants.py
│   ├── models_kashikar.py / models_nestoklon.py / models.py
│   ├── kpath.py / io_params.py / bandstructure.py / plotting.py
│   ├── velocity.py            速度演算子 dH/dk（物性モジュールの共有基盤）
│   ├── g_factor.py            Landé g 因子（Theme A）
│   ├── optical.py             誘電関数 ε(ω)（Phase 1.5）
│   ├── shift_current.py       シフト電流 / BPVE（Theme F）
│   ├── exciton.py             Wannier-Mott 励起子（Theme I）
│   ├── berry.py               Berry 曲率 → AHC / SHC / 離散 Chern（spec F1 / Theme H）
│   ├── topology.py            Wilson ループ / Wannier 電荷中心 / Chern（spec F2 部分）
│   ├── thermo.py              Boltzmann 熱電輸送 S/σ/κ_e（spec F9, CRTA）
│   ├── rashba.py              Rashba スピン分裂 α_R / spin texture（spec F4）
│   ├── edelstein.py           Edelstein 電流誘起スピン分極 χ（spec F11, CRTA）
│   ├── cpge.py                円偏光光起電力 CPGE / injection current（spec F7）
│   ├── polaron.py             Fröhlich ポーラロン結合 α / 弱結合質量（spec F6）
│   ├── bandengr.py            歪みバンド工学 E_g(ε) / 変形ポテンシャル（spec F12）
│   ├── materials_project.py   MP DFPT ε∞ 取得（Theme I, option C'）
│   ├── cli.py / __main__.py / _meta.py / __init__.py
│
├── tests/                     単体テスト・V&V テスト
│   ├── test_soc.py            SOC L·S 固有値・規約
│   ├── test_slater_koster.py  SK 二中心積分（軸方向手計算・パリティ）
│   ├── test_kashikar.py       Eq.9 / SO分裂=3λ / 4軌道ギャップ
│   └── test_nestoklon.py      R点 1.017 / 実験 1.65・2.75 / SO分裂 1.48 eV
│
├── data/                      入力データ
│   └── parameters/            論文から抽出したパラメータ（JSON）
│       ├── kashikar2021_cubic_13orb.json
│       ├── kashikar2021_cubic_4orb.json
│       ├── nestoklon2021_CsPbI3.json
│       └── SOURCES.md         出典・検証アンカー・誤植注記
│
├── configs/                   実行設定（k 経路）
│   ├── cubic_MRGXM.json
│   └── cubic_GXMGR.json
│
├── results/                   計算結果（バンド図 + 再現性メタデータ JSON）
│   ├── kashikar13/  kashikar4/  nestoklon/
│
├── notebooks/                 試行錯誤・可視化用（任意）
├── scripts/                   実行・バッチスクリプト（任意）
│
├── docs/                      永続的ドキュメント（本フォルダ）
│   ├── research-objectives.md / theoretical-model.md / numerical-methods.md
│   ├── architecture.md / repository-structure.md / development-guidelines.md
│   ├── verification-validation.md / data-management.md / glossary.md
│
├── .steering/                 作業単位ドキュメント
│   └── 20260523-initial-implementation/  (requirements/design/tasklist)
│
└── references/                収集論文
    ├── references.md          文献リスト（arXiv ID 付き = 再取得可能）
    └── pdfs/                   PDF 群（Git 管理外, .gitignore）
```

## ディレクトリの役割とファイル配置ルール

- `src/`: 実装。物理量・軌道順序・ゲージ規約は各モジュール docstring に明記。
- `data/parameters/`: **論文記載値の転記のみ**。改変禁止、誤植は注記。出典必須。
- `configs/`: 計算条件（材料・モデルではなく k 経路など）。
- `results/`: 図と**再現性メタデータ JSON**を対で配置。大容量 `.npz/.npy` は Git 管理外。
- `tests/`: V&V を含む。論文の数値・解析式を再現することを assert する。
- `docs/`: 恒久ドキュメント。理論・数値・V&V の変更時に更新。
- `.steering/`: 作業ごとに `YYYYMMDD-タイトル` で新規作成（履歴=実験ノート）。

## ルート直下ファイル
- `LICENSE` — MIT License 全文（2026-05-24 追加。詳細は [development-guidelines.md](development-guidelines.md) 「ライセンスと SPDX 表記」）。

## scripts/ の deprecated 項目
- `cowork_5min_poll.ps1` — **2026-05-24 deprecate**（PI 判断による自律 5 分巡回停止）。削除せず履歴保持。
- `cowork_5min_poll_README.md` — 同上。停止/再開手順を同 README に記載。
- 監視は Cowork supervisor の 15 分巡回が代替。経緯: `cowork/progress/2026-05-24_1145_directive_PI_decisions.md`。

## 大容量データの取り扱い

- 参照 PDF（計 245 MB, 49 本）は Git 本体にコミットしない（`.gitignore`）。
  来歴は `references/references.md` の arXiv ID で保持（再取得可能）。
- 生成バンドデータ（`.npz/.npy`）は Git 管理外。図 (PNG) とメタデータ (JSON) は
  軽量なため必要に応じてコミット可。詳細は [data-management.md](data-management.md)。
