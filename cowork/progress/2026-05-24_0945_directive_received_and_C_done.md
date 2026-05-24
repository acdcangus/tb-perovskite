# Directive 0930 受領 + Part 1 (C') 完了 — 2026-05-24 09:45

directive `2026-05-24_0930_directive_theme_I_MP_and_PI_reports.md` 受領（§202 受領確認）。**Part 1 (option C') 完了**、Part 2 (PI 解説報告書 4 本) 着手予定。

## Part 1: Theme I option C' (MP DFPT ε_∞) — ✅ 完了

| ステップ | 状態 |
|---|---|
| C-1 MP API クライアント | ✅ `src/perovskite_tb/materials_project.py`（key は gitignored json からロード、browser-UA で Cloudflare 回避、**key は一切 log/commit/MANIFEST に出さない**） |
| C-2 `eps_inf_external.json` 更新 | ✅ 各材料に `eps_inf_MP_DFPT` ブロック（8/9、CsSnCl₃ は MP に dielectric なし）+ `_KEY_FINDING_C` |
| C-3 binding scan + Production | ✅ `--profile MP_DFPT`, bundle `results/production/theme_I_exciton_MP_DFPT/2026-05-24_118b3ce/`（git_dirty:false, 27 key_numbers） |
| C-4 報告書 §3.3 | ✅ `theme_I_exciton.md` §3.3 追記 |
| C-5 test（optional） | 未（任意。MP API モックテストは後続で追加可） |

### 受け入れ条件（§1.4）チェック
- [x] `mp_api_key.json` が `git check-ignore` で除外
- [x] API キー文字列が **commit に一度も入っていない**（`git log --all -S` + staged diff scan で確認、0 件）
- [x] MP で **8/9 材料**の DFPT ε_∞ 取得（≥6 達成。CsSnCl₃ not-found 明記）
- [x] Production bundle 作成（git_dirty:false, MANIFEST 完備）
- [x] 報告書 §3.3 で結果と限界を defensible に記述（出典＝mp-id、捏造ゼロ）
- [x] 既存テスト全通過（**231 passed**）
- ※ directive ファイル自体が key を平文で含んでいたため **redact 済み**（`<REDACTED>`）。今後 key を含む directive は配置時に redact 推奨。

### C' 主結果（E_b, meV）
CsPbCl₃ 119 > CsGeCl₃ 99 > CsPbBr₃ 57 > CsPbI₃ 41 > CsGeI₃ 22 > CsGeBr₃ 19 > CsSnBr₃ 12 > CsSnI₃ 4。
- **相対トレンド defensible**（単一手法 DFPT）。Cl 系大・Sn-I 最小。
- **絶対値は上限**（bare ε_∞ < ε_eff）。CsPbI₃ 41 vs 実験 ~15–20（~2–2.7× 過大）。§3.2/§3.3 に明記。

## Part 2: PI 向け解説報告書 4 本 — 着手予定

Cowork が `PI_explained_overview.md` を作成済み。これを起点に、推奨順（A→F→1.5→I）で
`cowork/reports/PI_explained_<theme>.md` を作成（§2.4 テンプレート: 30秒サマリ/物理背景/手順/結果解釈/新規性/限界/用語集/出典）。
数値は全て Production MANIFEST 引用、専門用語は初出定義、比喩多用、honest。Theme I は C' 結果込みで書く。
次サイクルから Theme A 着手。
