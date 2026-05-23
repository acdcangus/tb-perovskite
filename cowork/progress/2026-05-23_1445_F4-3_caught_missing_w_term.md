# F4-3 (Rice-Mele 閉形式) が F3 のバグを検出 — 一般化微分の w 項欠落 — 2026-05-23 14:45

**重要:** F4-3（Fregoso 2017 Appendix D の Rice-Mele 解析解との照合）で、**F3 の shift current
実装が不完全**であることが判明。decisive な検証が機能した好例。

## 検出内容
- Fregoso 2017 D15: `Im[r^z_cv r^z_vc;z] = a³ t δ Δ /(32 E³)`（2-band RM の per-k 積分核, 解析閉形式）。
- 私の現 `shift_current_zzz`（sum-over-states (*) 形）を 2-band RM に適用 → 積分核が **~1e-19（≈0）**、
  D15 は ~5e-3。**不一致**。
- 原因: 2-band では virtual sum が空、かつ第1項 `2 r Δ/ω` は Im[実数]=0 になる。
  → **Fregoso C2 の第2微分項 `w^{ab}_nm = ⟨n|∂²H/∂k_a∂k_b|m⟩` が私の (*) 形に欠落**していた
  （Cowork 1300 の擬似コード (*) も w 項なし）。δ=0 vanishing は対称性(0=0)で通っていただけ。
- **含意:** F3 の CsPbI₃ σ_zzz（多バンドで virtual sum は非ゼロ）も **w 項の寄与を取りこぼし＝不完全**。

## 修正（検証済み）
- Fregoso C2（velocity 形, w 項込み）を実装し、2-band RM で **D15 と完全一致（比 magnitude=1.0、
  全 k）**。符号も Fregoso σ（D14: σ∝−Im_Fregoso）と私の σ(=+∫Im_mine, Im_mine=−Im_Fregoso)が
  一致 → **符号・prefactor が Fregoso 閉形式で確定**（F4-3 の主目的達成、in-repo 一次照合）。
- C2: `r^a_{nm;b} = -(1/(iω_nm))[ (v^a_nm Δ^b + v^b_nm Δ^a)/ω_nm − w^{ab}_nm
  + Σ_{p≠n,m}(v^a_np v^b_pm/ω_pm − v^b_np v^a_pm/ω_np) ]`、出典 Fregoso 2017 (arXiv:1701.00172) Eq.(C2)。

## 次（実装中）
1. `shift_current_zzz` を C2（w 項込み）で書き直し、builder に `d2Hdk_fn`(∂²H/∂k²) を追加。
2. RM テスト（D15/D16 照合）を `tests/` に追加（符号・prefactor 確定の根拠）。
3. δ=0 vanishing 再確認、Nestoklon σ_zzz を w 項込みで再計算。
4. これにより F4-3 で符号確定 → F4-2（Tan&Rappe）は補助確認に格下げ可。

commit/push 進行中。no-hallucination: Fregoso 閉形式という一次照合で確定するので堅い。
