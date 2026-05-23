# F5 設計書（9 材料 × δ shift-current スキャン, Production）— レビュー依頼 — 2026-05-23 16:10

patrol 1725 §6 の事前確認 6 点に沿った F5 design です。**実行前にレビューをお願いします。**
収束プローブは実施済み（§4）。

---

## 1. 目的・主問い

- 立方 CsBX₃（B=Ge/Sn/Pb, X=Cl/Br/I, 計 9）に [001] 極性変位 δ（P4mm）を入れ、
  shift-current σ_zzz(ω) を計算。
- **主問い: 鉛フリー（Sn/Ge）で σ が大きい組成があるか**（毒性 Pb の代替の光起電力ポテンシャル）。
- モデル: **Kashikar-13 経験 TB**（`make_polar_kashikar13_builders`, n_occ=20 = Pb-s² + 3×X-p⁶）。
  shift current の起源（s↔p spσ 符号交替, Tan&Rappe Eq.14）を陽に持つため 13 軌道を採用（4 軌道は X-p を畳み込むため不適）。

## 2. 手法（確定済み・検証済み）

- 一般化微分: **Fregoso 2017 Eq.(C2) TB 形（w 項込み）**。F4-3 で Rice-Mele 閉形式 Eq.(D15)/(D16) と
  機械精度一致（符号・prefactor 確定）、F4-2 で多バンド対称則（Tan&Rappe Eq.14）一致。
- symmetry breaker: [001] Pb 極性変位（Harrison η=2.0 で B-X_z 結合非対称化）。δ=0 で σ=0（機械精度）を検証済み。
- **`d2Hdk_fn` を必ず渡す**（patrol 1725 §6-1; `allow_continuum_form` は使わない。defensive guard 通過）。

## 3. 絶対値 vs 相対値（patrol 1725 §6-6）

- **一次成果 = 相対比較**（9 材料すべて同一 prefactor・同一 (δ, n_kpts, η, ω) → cross-material 比較は頑健）。
- **絶対 μA/V² 較正**: Young & Rappe 2012 Eq.(1)（in-repo arxiv_1202.3168）より
  `σ_rsq = πe ∫dk (f) [e/(mℏω)]² ⟨P_r⟩⟨P_s⟩ R_q δ(ω_cv−ω)`。
  運動量 `P=(m/ℏ)∂H/∂k` を代入すると prefactor は `π e³/ℏ⁴`、BZ 測度は `∫d³k/(2π)³ = (1/V_cell)·⟨·⟩`。
  本実装の σ（積分核の自然単位 ÷N_k）に `π e³/(ℏ⁴ V_cell)` ＋ 周波数↔エネルギー単位換算を掛けて A/V² 化する。
  **ただし** (a) 換算は規約敏感、(b) Blount 1962 の TB intra-atomic 欠落で絶対値は系統的過小（g因子・光学 f-sum と同根）。
  → MANIFEST.notes に明記し、**論文の主張は相対比較で行う**。絶対値は「桁・符号の目安」として併記。

## 4. 収束（patrol 1725 §6-5; プローブ実施済み）

CsPbI₃, δ=0.15, ω∈[0.3,4.0] で実測（**single-thread BLAS 必須**, 下記 §6）:

| η | n_kpts=16 | 24 | 32 | 48 | L2rel(32→48) |
|---|---|---|---|---|---|
| 0.05 | （peak が 16↔24 で符号反転 → **η 小さすぎ・k 未収束**）|||||
| 0.08 | peak +1.06@4.0 | +1.05 | +1.05 | +1.03 | **0.019** |
| 0.15 | +0.86 | +0.85 | +0.84 | +0.83 | **0.009** |

- **結論: η=0.05 は鋭すぎて k 収束不良。η≥0.08 で n_kpts=48 が L2rel≤2% に収束。**
- Production 設定（案）: **n_kpts=48（仕上げ）, η=0.10, ω∈[0.3, 5.0] eV（ピークが ~4 eV 付近のため窓を 5 eV まで拡張）**。
- **3 段階収束（PRODUCTION_RULES）**: k=24/32/48（L2rel 単調減）, η=0.05/0.08/0.15, ω 分解能 150/300/600。
  → `convergence/sigma_vs_nkpts.png`, `convergence/sigma_vs_eta.png`, `convergence/sigma_vs_omega_res.png`（patrol 1725 §6-3）。

## 5. 出力（PRODUCTION_RULES §4 準拠）

`results/production/theme_F_shift_current/2026-05-23_<hash>/`:
- `sigma_zzz_9materials.csv`（ω × 9材料 × δ∈{0.10,0.15,0.20}, 相対単位 + 絶対 μA/V² 換算列）
- `sigma_zzz_9materials.png`（材料比較プロット）
- `convergence/`（上記 3 プロット + 数表）
- `inputs/`（patrol 1725 §6-4）: `kashikar13_params_9materials.json`（SK パラメータ）, `scan_config.json`
  （δ 値・n_kpts・η・ω・n_occ）, `materials.json`（9 種一覧）, `git_info.txt`, `cli.txt`, `env.yml`, `seeds.json`（乱数なしを明記）
- `MANIFEST.json`: key_numbers に 9 材料の σ_zzz ピーク値・位置（δ=0.15）、
  **references に Fregoso 2017 PRB 96 075421（Eq. C2/D12/D15）+ Tan & Rappe 2016 npj CM 2:16026 + Young&Rappe 2012 PRL 109 116601** を明記（patrol 1725 §6-2）。notes に Blount 限界・相対/絶対の方針。
- uncommitted modification なしで実行、`git_dirty:false`。

## 6. 性能（重要な実装メモ）

- **batched eigh は multithreaded BLAS だと微小行列で病的に遅い**（26×26 で ~24ms/行列）。
  **`OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1` を numpy import 前に設定**すると
  n_kpts=24 の σ が 281s→5.9s（~48×）。Production スクリプト冒頭で `os.environ` に設定する。
- Kashikar polar builder は k 方向ベクトル化済み（`_batched`）。n_kpts=48 ≈ 35s/call。
  → 9 材料 × 3 δ ≈ 27 call ≈ **~16 分**（収束スタディ込みでも ~30 分）。

## 7. 確認したい点（Cowork へ）

1. Production 設定 **n_kpts=48 / η=0.10 / ω≤5 eV** で OK か（η=0.10 は 0.08 と 0.15 の中間、収束と分解能のバランス）。
2. δ ∈ {0.10, 0.15, 0.20} Å の 3 点で十分か（線形性は F4 で確認済み、絶対スケール用に複数点）。
3. 絶対 μA/V² 換算を入れるか、相対のみで報告するか（§3 の方針＝相対主・絶対併記caveat で進める想定）。

問題なければ収束スタディ（plots 保存）→ 9 材料スキャン → MANIFEST → F6 報告書、と進めます。
