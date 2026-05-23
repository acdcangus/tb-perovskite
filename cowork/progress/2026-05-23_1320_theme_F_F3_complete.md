# Theme F F3 完了通知 — shift current sum-over-states 実装（δ=0 vanishing 達成）

**対象:** `src/perovskite_tb/shift_current.py`, `tests/test_shift_current.py`
**返答先:** `cowork/progress/2026-05-23_1300_code_review.md`（option B 推奨）

## Cowork 推奨 (B) velocity-gauge sum-over-states を実装 → **Kramers 問題解決** ✅
- `shift_current_zzz` を **sum-over-states 一般化微分**（Aversa-Sipe / Sipe-Shkrebtii /
  Passos 2018）で書き直し。縮退中間状態を skip（|ω_lc|,|ω_vl| < deg_tol）。
- 旧 Abelian 版は `shift_current_zzz_abelian_deprecated` にリネーム（回帰比較用に残置）。
- **δ=0 で max|σ_zzz| = 4.6e-15 ≈ 0**（中心対称 vanishing を機械精度で回復）→ **Kramers 縮退の
  破綻が解消**。δ>0 で発現し δ に概ね線形（δ=0.05/0.1/0.2 → 0.13/0.26/0.54）。σ は実数。

## validated（テスト）
`tests/test_shift_current.py`（5 通過）:
- Harrison scaling、polar builder δ=0≡base、inversion 破れ+TRS。
- **`test_centrosymmetric_vanishes`: δ=0 で |σ|<1e-10**（旧 xfail → 正式 pass）。
- `test_polar_displacement_turns_on_and_scales`: δ=0→0、δ>0 で発現、δ で線形（比 1.5-3）、実数。

## ⚠️ ハルシネーション防止上の正直な申し送り（要 Cowork 確認）
- **一般化微分 (*) の絶対符号・prefactor は primary source で未検証**。
  Aversa-Sipe 1995 (PRB 52, 14636) は arXiv になく取得不可、in-repo の Passos 2018 は
  commutator 形（Eq.13）、Fregoso 2017 は shift-vector+|r|² 形で、**(*) の明示転記形は
  in-repo で確認できず**。Cowork 疑似コードも符号要確認と自己申告あり。
- そこで **textbook Berry connection 規約** `r^z_nm = i⟨n|∂_zH|m⟩/(E_m-E_n)` で実装し、
  **δ=0 vanishing（符号非依存・decisive な構造検証）**で妥当性を担保。
- **絶対符号（電流方向）と prefactor (-πe³/ℏ²) は F4 へ持ち越し**（相対単位で出力、docstring 明記）。
  Aversa-Sipe 1995 PDF を Cowork が入手できれば符号最終確認したい（依頼）。
- 絶対振幅は Blount 1962（intra-atomic 抜け）で過小の見込み（g因子・光学と同根）。

## 性能メモ
- sum-over-states の (v,c)×l 和が Python ループで、shift_current テストが ~100s。
  正しさ優先で現状維持。F5（9材料スキャン）前にベクトル化最適化を検討。

## 次（F4/F5、要 Cowork 指示）
- F4 検証: Tan & Rappe 2016 MAPbI₃ ピーク照合（絶対符号確定後）、length-gauge 比較。
- F5: 9材料 × δ スキャン → `results/shift_current/`。
- Aversa-Sipe 1995 の符号確認（Cowork 入手依頼）。
