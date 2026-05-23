# 本番計算ルール（Production Run Rules）

**初版:** 2026-05-23
**発行:** Cowork
**対象:** Claude Code が本リポで実行する計算のうち、**論文掲載・公開・最終報告書に使うもの**

`docs/data-management.md`（既存）の方針と整合する、運用レベルの具体ルールです。

---

## 0. 計算の 2 段階モード

明示的にどちらかを宣言してから計算してください。

### モード A: Exploratory（試行錯誤・パラメータ感度確認）
- 低い k グリッド、粗い smearing、限定材料で OK
- 結果は `cowork/progress/*_log.md` に貼って良い
- データの完全保存は不要。気軽に消して良い
- 用途: 「この方針で進めるかどうかの判断材料」

### モード B: Production（論文・公開・最終報告書）
- **以下の本番ルール全てに従う**
- 結果は `results/production/<theme>/<date>_<commitHash>/` 配下に永続保存
- 同じ計算を **他人が再現できる**ことが必須
- 用途: 「論文の Figure や Table に使う数値」

**reports/ で参照する数値は必ず Production モードで出すこと**。Exploratory の数値を引用するときは「[Exploratory]」と明示。

> **5 分自律巡回の前提（2026-05-24 追加）:** Production 実行中も `scripts/cowork_5min_poll.ps1`（層 1, OS スケジューラ）が動作しており、Claude Code は最大 5 分以内に新着 directive を検知できる。**30 分以上を要する Production scan では、`scan_shift_current_9materials.py` の `_check_cowork_progress` を主ループ（k 点ループ等）に組み込み**、生存ログと新着検知の両方を担保する（層 2）。検出のみで scan 本体は止めない（Production 中断防止）。

---

## 1. 収束確認（Production 必須）

### 1.1 何を収束させるか

計算手法ごとに **収束パラメータ**を明示し、3 段階以上の解像度で結果が変わらないことを示す：

| 手法 | 収束パラメータ | 推奨ステップ |
|---|---|---|
| バンド計算 | k 経路上の点数 | 50 → 100 → 200 |
| g 因子（k·p） | 摂動次数 / バンド対 | 必要なら 2-band → 3-band → 4-band |
| 光学 ε(ω) | k グリッド (BZ 積分) | 8³ → 16³ → 24³ |
| 光学 ε(ω) | smearing η | 0.10 → 0.05 → 0.025 eV |
| 光学 ε(ω) | ω グリッド分解能 | dω = 0.05 → 0.02 → 0.01 eV |
| 光学 ε(ω) | ω カットオフ | f-sum 整合まで伸ばす |
| Shift current | k グリッド | 同上、より細かく必要かも |
| Boltzmann mobility | T グリッド・τ サンプル数 | 試験して合わせる |

### 1.2 収束判定基準

**主結果の物理量（バンドギャップ、g 因子、ピーク位置、強度比 等）が**：
- 連続する 2 ステップ間で **±1%（または ±数 meV）以内**で安定したら収束

### 1.3 収束プロット

`results/production/<theme>/<date>_<commitHash>/convergence/` に：
- `convergence_kgrid.png` — 主結果 vs k グリッド
- `convergence_eta.png` — 主結果 vs smearing
- `convergence_*.png` — 他の収束軸

これを論文の SI に載せられるクオリティで作成。

---

## 2. データ保存ルール（Production 必須）

### 2.1 ディレクトリ構造

```
results/production/<theme>/<date>_<commitHash>/
├── MANIFEST.json              # 全入出力の索引（後述）
├── inputs/                    # 入力ファイル一式（後述 §3）
│   ├── config.json
│   ├── parameters.json
│   ├── ...
├── outputs/                   # 計算結果（生データ）
│   ├── raw/                   # CSV、numpy.npz、HDF5 等の生数値
│   ├── derived/               # 加工済み（プロット用に整形した CSV 等）
│   └── figures/               # プロット PNG/SVG
├── convergence/               # §1.3 収束プロット
├── logs/                      # 標準出力・エラー出力
│   └── run.log
└── README.md                  # この実行で何をしたか、150 字程度
```

### 2.2 保存対象（**全て残す**）

- **入力ファイル**: config, parameters JSON、コマンドライン引数、環境変数
- **乱数シード**: 全てのシードを `MANIFEST.json` に明示
- **生出力**: ε(ω), g 値, band 配列、Berry curvature 等の **数値配列そのまま**（プロットだけでなく）
- **収束データ**: 試した各解像度の結果
- **ログ**: stdout/stderr、警告、計算時間
- **ソフトウェアバージョン**: Python, numpy, scipy, matplotlib のバージョン
- **コミットハッシュ**: 実装版の git commit hash
- **計算機環境**: CPU、RAM、OS（任意だが推奨）

### 2.3 圧縮・大容量データ

- 100MB 以上は **gzip/zstd 圧縮**して保存（小さい数値配列でも npz は圧縮形式 `np.savez_compressed`）
- Git 管理: 1MB 以上は **Git LFS** または **`.gitignore` で除外 + `MANIFEST.json` にハッシュ記録**
- 大容量は外部ストレージ（DVC, Zenodo, OSF 等）への参照を `MANIFEST.json` に記録

### 2.4 削除禁止

**Production 結果は手動で削除しないこと。** 古い結果は `results/production/<theme>/_archived/` に移動するだけ。後で別の主張をするときの参照になります。

---

## 3. 入力ファイルの保存（再現性）

### 3.1 必須項目

すべての Production 実行で、`inputs/` 配下に以下を保存：

```
inputs/
├── config.json              # 計算条件（材料、k 経路、収束パラメータ）
├── parameters.json          # TB / k·p パラメータ（出典 DOI 込み）
├── cli.txt                  # 実行コマンド（PYTHONPATH=src python ... の完全形）
├── env.yml                  # conda 環境 or requirements.txt スナップショット
├── git_info.txt             # コミットハッシュ・ブランチ・修正ファイル一覧
└── seeds.json               # 乱数シード（あれば）
```

### 3.2 `env.yml` の作り方

```bash
# conda 環境を使っている場合
conda env export --no-builds > inputs/env.yml

# venv + pip の場合
pip freeze > inputs/requirements.txt
```

### 3.3 `git_info.txt` の作り方

```bash
{
  echo "## Git info"
  git log -1 --pretty=fuller
  echo ""
  echo "## Branch"
  git branch --show-current
  echo ""
  echo "## Modified (uncommitted) files (must be clean for production!)"
  git status --short
} > inputs/git_info.txt
```

**Production 実行時に uncommitted modification があってはならない**（再現できなくなる）。`git status --short` が空であることを確認してから走らせる。

### 3.4 再現コマンド

`README.md` の末尾に、コピペで再実行できるコマンドを書く：

```bash
# Reproduction (cloning at the recorded commit)
git checkout <commit_hash>
conda env create -f inputs/env.yml -n repro
conda activate repro
cd <project_root>
$(cat inputs/cli.txt)
```

---

## 4. MANIFEST.json（中心索引）

各 Production 実行の根本に置く。Cowork や他の人がすぐに状況を把握できる索引。

```json
{
  "manifest_version": "1.0",
  "theme": "theme_A_g_factor",
  "subtask": "A4 9-material scan",
  "date_utc": "2026-05-23T10:30:00Z",
  "git_commit": "a0c3775abc1234",
  "git_branch": "main",
  "git_dirty": false,
  "executor": "Claude Code (Sonnet 4.5 via CLI)",
  "mode": "Production",
  "physics_method": "k.p universal formula with TB-derived Δ, P_universal=6.8 eV·Å",
  "convergence": {
    "k_grid": "Not applicable (R-point evaluation)",
    "eta_eV": "Not applicable"
  },
  "inputs": {
    "config": "inputs/config.json",
    "parameters": "inputs/parameters.json",
    "cli": "inputs/cli.txt",
    "env": "inputs/env.yml",
    "git_info": "inputs/git_info.txt"
  },
  "outputs": {
    "csv": "outputs/raw/g_factor_9material.csv",
    "plots": [
      "outputs/figures/kirstein_universal_plot.png",
      "outputs/figures/material_grid.png"
    ],
    "logs": "logs/run.log"
  },
  "key_numbers": {
    "CsPbI3_g_e": 3.01,
    "CsSnI3_g_e": 4.557,
    "CsGeI3_g_e": 3.39
  },
  "checksums_sha256": {
    "outputs/raw/g_factor_9material.csv": "abc...",
    "outputs/figures/kirstein_universal_plot.png": "def..."
  },
  "data_size_total_bytes": 12345678,
  "runtime_seconds": 123.4,
  "software": {
    "python": "3.11.5",
    "numpy": "1.26.0",
    "scipy": "1.11.3",
    "matplotlib": "3.8.0"
  },
  "machine": {
    "os": "Windows 11 / WSL2 Ubuntu 22.04",
    "cpu": "Intel i7-1185G7",
    "ram_gb": 32
  },
  "notes": "Δ for Sn/Ge from Kashikar 3λ (±20%), Pb from Nestoklon Table S2",
  "references": [
    "Kirstein 2021 arXiv:2112.15384 Eq.5,6",
    "Nestoklon 2023 arXiv:2305.10586 SI Eq.S3,S7",
    "Kashikar 2021 arXiv:2101.08562 Eq.9"
  ]
}
```

---

## 5. テスト・検証（Production 必須）

Production 実行前に：

1. ✅ **既存テスト**が全通過していること（破壊変更なし）
2. ✅ **対称性チェック**が通る（立方等方、Kramers 縮退 等）
3. ✅ **解析極限**（SOC→0、E_g→∞ 等）が論文値と一致
4. ✅ **論文値再現アンカー**（Nestoklon Table S2 等）が許容範囲内

これらの確認結果も `outputs/validation_checks.txt` に保存。

---

## 6. 報告書（reports/）との連携

`cowork/reports/theme_X_*.md` で Production 結果を引用する際：

- 数値表のキャプションに `MANIFEST.json` のパスを記載
- 「§8 再現コマンド」に正確な実行コマンドを書く
- 数値が変わったら **古い数値は残す**（取り消し線などで）+ MANIFEST 番号で履歴を辿れる

例：
> Table 1 の数値は `results/production/theme_A_g_factor/2026-05-23_a0c3775/MANIFEST.json` の `key_numbers` から取得。

---

## 7. Exploratory → Production への昇格

試行錯誤で「これが論文の主張になる」と確信できたら：

1. **収束確認**を 3 段階以上で実施
2. uncommitted な修正があれば全てコミット
3. `results/production/<theme>/<date>_<commitHash>/` を新規作成
4. 上記ルールに従って全データ保存
5. `MANIFEST.json` 作成
6. 報告書を更新して MANIFEST へのリンク追加
7. `cowork/progress/.../production_run_complete.md` で Cowork に通知

---

## 8. 違反の自動検出（Cowork 側でチェック）

Cowork supervisor は巡回時に以下を自動チェック：

- `reports/` 内の数値が `results/production/.../MANIFEST.json` から引用されているか
- `MANIFEST.json` が完備か（必須フィールド欠落なし）
- `git_dirty: true` で commit されている Production がないか
- 収束プロットが存在するか

違反があれば `cowork/progress/.../production_violation.md` で警告。

---

## 9. 既存結果の遡及対応

すでに存在する Theme A の結果 (`results/g_factors/`) などは、**遡及的に MANIFEST.json を作って Production 化**するのが望ましい。優先度低いが、論文化前に必須。

Phase 1.5 (光学) の結果も同様。次の自然な作業区切りで実施。

---

## まとめ（一言で）

> **Production = 全データ保存 + 入力一式保存 + 収束確認 + MANIFEST.json で索引。Exploratory はラフで OK。両者を明示的に分ける。**
