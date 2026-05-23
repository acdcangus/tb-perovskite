# フォルダ移動の取り込み + Theme A Fig.2 polish — 2026-05-23 12:45

## フォルダ構造変更を取り込み
- `COWORK_README.md` と `cowork/next_directive.md` を読了。**以後 `cowork/` プレフィックス**で
  Cowork 関連ファイル（progress/reports/directive/research_ideas/novelty_assessment）にアクセスします。
- Cowork による移動はファイルシステム上のみで未コミットだったため、**git に反映（29 renames 検出）して
  commit/push**（5293215）。リポジトリが新構造と一致。
- `cowork/next_directive.md` は内容的に v2 のまま（変更はフォルダ告知のみ）。新規研究指示なし。

## Theme A Fig.2 polish (c) 完了
- `scripts/plot_gh_delta_dependence.py` → `results/g_factors/gh_delta_dependence.png`（commit ddf5154）。
- **Δg_h vs Δ**: Pb（Δ~1.3-1.5）は乖離≈0、Sn（Δ~0.45）+0.6〜1.8、Ge（Δ~0.21）+0.6〜1.9。
  ±20% Δ バンド付き。鉛フリーの g_h 普遍関係破れを Δ 依存として直接可視化（論文 Fig.2 候補）。
- `cowork/reports/theme_A_g_factor.md` の図リスト更新。

## Theme F F3 ステータス（変わらず blocked）
- `cowork/progress/2026-05-23_1230_shift_current_kramers_escalation.md` 参照。
- **builder（δ=0 で base と一致）/ Harrison / intensity は validated**。
- **Abelian shift vector が Kramers 2重縮退（SOC）で破綻**（δ=0 で σ_zzz≠0）。
  非アーベル化（縮退部分空間トレース）or velocity-gauge sum-over-states（Passos 2018）の
  正しい離散表式を **Cowork の式検証待ち**（推測実装しない）。δ=0 テストは xfail(strict)。

## 検証
208 passed + 1 xfailed（既存 205 維持）。全 push 済み。

## 次（Cowork 待ち / 並行可）
- F3 完遂は縮退バンド shift vector の式確定待ち。
- 並行で可能な残作業: Theme A Fig.1 の残り polish（残差パネル等）、または
  Cowork の F3 式回答が来たら即実装（builder/intensity は検証済み）。
