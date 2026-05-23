# F5 Production 完了 + F6 報告書更新 — 2026-05-23 20:30

**status check（1940/2010/2025）への応答が遅れてすみません。** 88 分の長時間 run を監視していました（中断・失敗ではなく、完走）。

## 結論

- **F5 Production 完了。** bundle: `results/production/theme_F_shift_current/2026-05-23_ef575e3/`（commit `8231bf4`）。
  **git_dirty:false**, MANIFEST + inputs(7) + outputs(3) + convergence(4) + logs + README 完備、checksums 付き。
- **F6 報告書更新済み**: `cowork/reports/theme_F_shift_current.md` §3（確定値表）/§6（考察）。

## ★ 主結果（n_kpts=48, η=0.10, δ=0.15, 相対単位）

**鉛フリー Sn/Ge ハライド（特にヨウ化物）が Pb 系より大きい shift current** → 主問いの答えは **YES**。

| | ピーク |σ_zzz| 順位 |
|---|---|
| 1–2 | **CsSnI₃ (3.43), CsGeI₃ (2.67)** ← 最大 |
| 3–4 | CsSnBr₃ (1.31), CsGeBr₃ (1.30) |
| 5 | CsPbI₃ (0.97) |
| 6–9 | CsGeCl₃ 0.66, CsSnCl₃ 0.44, CsPbBr₃ 0.31, CsPbCl₃ 0.11 |

- σ は **gap と逆相関**（小 gap→大 σ、1/E_cv² 由来）。Sn/Ge は gap が小さく大 σ。
- δ=0 で σ=6.9e-15（中心対称消失）。n_kpts=24↔48 で順位不変（頑健）。
- **メトリクス注意**: [Eg,2Eg] ω 積分は極小 gap 材料（CsSnI₃ 0.175 eV）を過小評価（主ピークが 2Eg 上）。
  → 小 gap 材料はピーク強度が適切な指標（報告書 §3 に明記）。

## 88 分かかった件（1940 status check §3 への回答）

- **シェル env は正しく設定**して実行（`OMP_NUM_THREADS=1 ...` 付き、cli.txt にも記録）。BLAS multithread 病的遅延ではありません。
- 遅延原因は **収束デバッグ期に私が多数の background timing プロセスを並行起動**し、本番 run と CPU を取り合ったため
  （single-thread だが他プロセスと競合）。run 自体は正しく完走（runtime 5278s, logs/run.log）。
- 教訓: Production run 中は他の重い background ジョブを走らせない。次回 G テーマで徹底します。

## 残（任意）

- 絶対 μA/V² 較正は Blount 限界 + 規約敏感のため deferred（formula は MANIFEST.notes / report §5）。必要なら参照アンカーで後日。
- F-D8（SOC on/off 比較）は report §6 に今後の論点として記載。

Theme F（F1–F6）完了とします。次の指示（G テーマ等）あれば `next_directive.md` で。レビューよろしくお願いします。
