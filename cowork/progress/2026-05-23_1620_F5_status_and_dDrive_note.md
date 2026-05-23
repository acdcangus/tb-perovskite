# F5 ステータス + D ドライブ件 — 2026-05-23 16:20

## F5 ステータス（1840 code review §3 への対応 = 完了、Production 実行中）

1840 code review の §3（バンドル化必須）・§4（minor）すべて反映済み。commit `bde96e7`:
- `--production` モード追加: git-clean チェック → convergence + 9 材料 scan → `build_bundle` で
  `results/production/theme_F_shift_current/<date>_<hash>/`（MANIFEST.json, inputs/, outputs/{raw,figures}/,
  convergence/, logs/, README.md）を生成。bundle 組み立ては dummy ファイルで smoke-test 済み。
- §3.2 MANIFEST: theme/git_*/physics_method/convergence/inputs/outputs/key_numbers/checksums/software/references/notes 完備。
  references に Fregoso2017 + Tan&Rappe2016 + Young&Rappe2012 + **Kashikar2021** を明記。
- §3.3 inputs/: scan_config.json, kashikar13_params_9materials.json, materials.json, seeds.json, cli.txt, git_info.txt, requirements.txt。
- §3.4 git-dirty チェック（`--allow-dirty` 例外）。§3.5 convergence/ を同一 commit で同梱。§3.6 README.md。
- §4: `models_kashikar` 冒頭 import、`gap_at_R_eV` rename、`peak_omega_*_eV` suffix、flush print、
  key_numbers に **ω 積分 [Eg,2Eg]**（§6 の主問い用）+ δ=0 null + runtime_seconds。
- Q3（絶対値）: **相対単位を一次成果**として実行。絶対 μA/V² は Blount 限界のため notes に formula のみ記載し deferred
  （規約敏感な SI 換算でハルシネーションを避ける方針。必要なら参照アンカー付きで後日較正）。

**Production run 実行中**（single-thread BLAS, n_kpts=48/η=0.10、9 材料 × δ∈{0.10,0.15,0.20} + 3 段収束、~16–20 分見込み）。
完了後 `F5_production_done.md` + F6 報告書（`cowork/reports/theme_F_shift_current.md`）に進みます。

## 性能の重要メモ（既報の確定版）

batched eigh は **multithreaded BLAS だと微小行列(26×26)で病的に遅い**（~24ms/行列）。
`OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1` を numpy import 前にシェルで設定すると
n_kpts=24 σ が **281s→5.9s（~48×）**。script 冒頭の `os.environ.setdefault` だけでは不完全（BLAS 初期化タイミング）なので、
**実行はシェル env 付き**で行う（cli.txt にもその形で記録）。

## 1410 directive（D ドライブ classic 15 件）について — ★ 実行不可の申し送り

本コンテナ（Linux/WSL, `/workspace`）から **D ドライブにアクセスできません**（`/mnt/` は空、`/mnt/d` 無し）。
classic 原典（Kane/Vogl/Luttinger 等）は**ユーザー側 Windows の D: にあり、私の実行環境にはマウントされていない**ため、
私からはコピーできません。対応案:
- (a) ユーザー or Cowork 側（D: にアクセス可能な環境）が `references/pdfs/classic_*.pdf` に配置、
- (b) arXiv 等で入手可能な範囲を私が WebFetch で取得（古典原典の多くは arXiv 以前なので限定的）、
- (c) Theme A/F 論文化の引用は **書誌情報（著者・誌・年・式番号）の明記**で代替（PDF 本体は無くても引用は可能）。

→ 7 連続リマインドされていますが**環境制約で私が実行できない**タスクです。(a) を推奨。私は F5→F6 を継続します。
