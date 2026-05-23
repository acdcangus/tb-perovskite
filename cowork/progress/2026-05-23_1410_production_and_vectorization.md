# Production 化 + shift current ベクトル化 完了 — 2026-05-23 14:10

directive 1335/1355 と PRODUCTION_RULES.md を読み、優先順に実施。

## 1. PRODUCTION_RULES.md 取り込み + 再利用ヘルパー
- `scripts/make_production_bundle.py`（再利用可）: MANIFEST.json / inputs/(cli,git_info,
  requirements,パラメータ) / outputs/{raw,figures} / convergence/ / logs / README、
  sha256・software 版・key_numbers を生成。git_dirty は production バンドル自身を除外して判定。

## 2. 既存結果の遡及 Production 化（再実行なし、コピー+索引）
- **Theme A**: `results/production/theme_A_g_factor/2026-05-23_31374dc/`（MANIFEST に
  CsPbI3/CsSnI3/CsGeI3 の g_e、g_h 乖離、TB-derived P 等）。
- **Phase 1.5 光学**: `results/production/phase_1.5_optical/2026-05-23_31374dc/`
  （ε_∞ 順序・f-sum・収束 convergence.md 同梱）。
- 両報告書 (`cowork/reports/theme_A_g_factor.md`, `theme_A5_optical.md`) に MANIFEST 参照を追記。

## 3. shift current ベクトル化（Cowork 要望; F5 前提）
- `shift_current_zzz` を行列演算化: 縮退対の Berry connection を 0 にすると virtual l-和が
  純行列積 `rz@rz`（l=v,c・Kramers 縮退を自動除外）、Lorentzian δ-和は外積。
- **ループ版と完全一致**（δ=0→0, δ=0.05/0.1/0.2 → 0.1261/0.2608/0.5375）、**~20倍高速**
  （テストスイート 92s→16s）。210 passed。

## 注記（symmetry breaker の方針確認）
- 1335 §5 は「uniaxial strain」と記載だが、これは cubic→P4/mmm（中心対称）で σ⁽²⁾=0 のまま。
  1200 F2 review・1355 F4 review で承認済みの **[001] 極性変位 (P4mm)** を採用継続（F3 実装済）。
  1335 §5 と 1355 の整合だけ確認したい（極性変位で進めて問題ないはず）。

## 次（F4, directive 1355 順）
- F4-1 length-gauge 同値性 / F4-2 Tan&Rappe MAPbI₃ 照合 / F4-3 SSH toy / F4-4 対称性テスト。
  「3 つのうち 2 つ整合で符号・prefactor 確定」方針。ベクトル化で F4 テストが現実的時間に。
- Aversa-Sipe 1995 PDF はユーザー機関アクセス取得を Cowork が依頼中（絶対符号の primary 照合用）。
- 全 push 済み（commit 870381c）。
