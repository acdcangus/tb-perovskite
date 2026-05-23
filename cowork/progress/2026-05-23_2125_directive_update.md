# Directive update — 2026-05-23 21:25 JST (18:22 UTC) — soft nudge

**発行元:** Cowork supervisor (patrol 2125)
**宛先:** Claude Code
**性質:** 🟢 **強制ではなく推奨**。すでに自走中であれば現在の作業を継続して構いません。

---

## 状況認識

- 直近コミット `4b33104` から **45 分間** git/progress いずれも更新なし
- Theme F closeout + Production 3 bundle + recipe docs 化はすべて完了
- `next_directive.md` 優先 1-7 はほぼ消化済み。残タスクは `PI_summary_2026-05-24.md` と優先 8 (future_themes)

`next_directive.md` の自律判断ルール:
> 30 分以上行き詰まったら BLOCKED に書いて次の優先タスクへ進む

→ 現在 BLOCKED もなく沈黙が続いているため、待機状態と推測。PI 起床（JST 朝、約 5-7 時間後）まで余裕あり、進められるタスクは進めて問題ありません。

## 推奨アクション（2 択、Claude Code が選択してください）

### Option A: `PI_summary_2026-05-24.md` を着手（最優先候補）

`next_directive.md` §「PI が朝起きた時に見たいもの」の **6 項目中 5 は達成、PI_summary だけ未達**。これを書くのが最も価値が高い。

**配置:** `cowork/progress/2026-05-24_PI_summary.md`（または `cowork/PI_summary_2026-05-24.md`、どちらでも可）

**内容構成案:**
1. **TL;DR**（3-5 行）: PI 不在中の最大の発見
2. **何をやったか**（時系列、5-10 件）: コミット履歴 `4b33104` 以前のハイライト
3. **Production bundle 3 本の要約**: phase_1.5_optical / theme_A_g_factor / theme_F_shift_current の key_numbers
4. **新規性の確信度**: Sn/Ge halide で σ_BPVE 最大 / g_h 普遍関係破れの 2 大 finding
5. **未解決・要 PI 判断**: 絶対値較正の Hughes-Sipe prefactor pass、Kane 1957 等の D ドライブ古典原典コピー、優先 8 のテーマ選択
6. **次のおすすめテーマ**: Theme I (Wannier-Mott 励起子) が軽量で即実装可能

PI が朝に `RESULTS.md` と `PI_summary_2026-05-24.md` の 2 本だけ読めば全体把握できる構成を目指す。

### Option B: 優先 8 の Theme I (Wannier-Mott 励起子結合エネルギー) を軽量着手

`cowork/future_themes.md` Theme I 節（line 42-73）参照。

- 100-150 行の軽量実装
- 既存 effective mass 計算（Theme A の P-parameter 抽出と同枠組み）+ ε_∞（Phase 1.5 既存出力）を流用
- 公式: `E_b = (μ/m₀) / ε_∞² × 13.6 eV`、`1/μ = 1/m_e + 1/m_h`
- 文献: Yang et al. 2017 PRB 96, 035301 / Tanaka et al. 2003 / `references/pdfs/arxiv_1908.09436.pdf` (Cho 2019 GW-BSE)
- Production モード（収束確認: k グリッド・有限差分間隔の 3 段階）+ MANIFEST.json
- 出力: `results/production/theme_I_exciton/2026-05-23_<hash>/`
- 報告書: `cowork/reports/theme_I_exciton_binding.md`

## どちらを選ぶかの判断指針

- **PI 起床まで残 5-7 時間**: 両方こなせる可能性あり。Option A を先に短時間で書き上げ、その後 Option B に着手するのが理想
- **Option A のみで十分**: PI レビュー用サマリは性質上、フレッシュなうちに書くほうが質が高い
- **Option B 優先**: 軽量とはいえ Production 化まで含めると 2-3 時間。深夜帯の集中作業に向く

→ **推奨は Option A を先に 30-60 分で書き、その後 Option B に着手**。ただし Claude Code の判断で順序逆転 OK。

## すでに自走中の場合

もし PI_summary をすでに書いている最中だった場合は、本 nudge は無視して構いません。コミット時に `2026-05-23_2140_<topic>.md` 等で「nudge 受信時点で既に X 作業中だった」と一言追記いただければ、こちら（supervisor）の混乱防止に役立ちます。

## 引き続きの自律判断ルール

`next_directive.md` の以下は今も有効です:

- 行き詰まったら `BLOCKED_<topic>.md` で報告して次へ
- 物理判断に迷ったら根拠を `progress/` に書いて自分で判断
- 新しい論文・データが必要なら `need_paper_<topic>.md` で Cowork に依頼
- テスト失敗は修正せず原因を `test_failure_<file>.md` に記録

## 出典・参照

- `cowork/next_directive.md` 優先 8 + 「PI 不在中の自律判断の原則」
- `cowork/future_themes.md` line 42-73 (Theme I 詳細)
- `cowork/progress/2026-05-23_2110_supervisor_patrol.md` §7 (本 nudge の発行条件と内容を予告)
- `cowork/PRODUCTION_RULES.md` §1-8 (Production モード必須)

---

**判断: Cowork supervisor は強い指示は出しません**。Claude Code の自律判断を尊重します。本メモは「45 分沈黙の合図」として参考にしてください。
