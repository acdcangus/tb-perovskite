# Next Directive — Claude Code 向け作業指示（v4 — PI 判断 3 件反映版）

**発行日:** 2026-05-24 11:45 JST
**発行元:** Cowork（監督役）
**前 directive:** `cowork/progress/2026-05-24_0930_directive_theme_I_MP_and_PI_reports.md` ✅ 完全完了 (HEAD `2228a4a`)
**本 directive 実体:** `cowork/progress/2026-05-24_1145_directive_PI_decisions.md`

---

## 📌 v4 で何が変わったか

PI から 2026-05-24 11:40 に 3 件の方針判断を受領し、それを反映した directive を発行:

1. **Theme I 論文化方針** = option C' を主結果、option D' を校正点として併記
2. **自律 5 分巡回ループ** = 停止（Cowork 15 分巡回で代替）
3. **LICENSE** = MIT を適用

加えて PI 追加指示「**プログラムに手を入れているなら CLAUDE.md に従って各種ドキュメント整備もちゃんとやって**」を受領。
本 directive では `src/` / `scripts/` / `docs/` を変更する Part に対して **`.steering/` ディレクトリ作成と永続 `docs/` 更新を必須化**。

---

## §-2. ★ Standing rule: 全レポート二者並行レビュー（3 ラウンド連続 0 指摘 + 文献照合必須）— 2026-05-24 12:00 PI 直接指示

PI 指示原文（2026-05-24 11:55 JST）:
> 「すべてのレポート類は、claude code およびあなたそれぞれで批判的にレビューして、3 回指摘がなくなるまで何度もレビューしなおしてね。特に、ハルシネーションは絶対ダメ。記憶じゃなくて、文献など事実に基づいて確認は必須。」

**実体 directive:** `cowork/progress/2026-05-24_1200_PI_review_protocol_standing_rule.md`

### 中核ルール

1. **二者並行**: Claude Code と Cowork supervisor がそれぞれ独立に批判的レビュー
2. **3 ラウンド連続 0 指摘で合格**: 1 件でも指摘が出たらカウンタリセット
3. **ハルシネーション禁止**: すべての記述は手元 PDF (`references/pdfs/`) または `results/production/*/MANIFEST.json` に遡れること。記憶ベース記述は無条件アウト
4. **文献照合は必須**: `pdftotext -layout references/pdfs/arxiv_XXXX.YYYYY.pdf` で原典確認

### 対象（17 ターゲット）

`cowork/reports/*.md` × 11 + `results/production/*/MANIFEST.json` の `key_numbers` × 6

### 優先度

最高（standing rule）だが緊急性は低い。v4 Part 2/Part 3 と **並行実施可**。
新規レポート追加時は本 protocol を起動。

---

## §-1. 自律 5 分巡回ループ — **停止中（2026-05-24 PI 判断）**

旧 v3 では `scripts/cowork_5min_poll.ps1`（OS スケジューラ層）が 5 分ごとに巡回プロンプトを流し込む前提だったが、
PI 判断により停止。**Cowork supervisor の 15 分巡回（Cowork 側 scheduled task）が監視を担う**。

→ Claude Code 側は **イベント駆動**（PI からの直接 chat / Cowork の `cowork/progress/` ファイル更新）で動く。
→ 沈黙再発検知は Cowork 側で「新規 commit ゼロが 4 サイクル（1h）連続 → PI 通知」ロジックを追加（本 directive 外）。

詳細は `cowork/progress/2026-05-24_1145_directive_PI_decisions.md` Part 2。

---

## §0. 最優先タスク（本 directive で実施するもの）

すべて緊急性は低い（Production 数値・物理結果に影響しない方針確定）が、**面倒くさがらず CLAUDE.md 準拠で実施**。

| Part | 内容 | `.steering/` | `docs/` 更新 | コミット |
|---|---|---|---|---|
| Part 1 | Theme I 報告書を C' 主・D' 併記に再構成 + 論文骨子初稿 | 不要 | 不要 | 1 commit |
| Part 2 | 自律 polling 停止（DEPRECATED 化、解除手順書化） | `.steering/20260524-deprecate-polling/` | `docs/repository-structure.md` | 1 commit |
| Part 3 | MIT LICENSE 適用（LICENSE ファイル / SPDX / README / dev-guidelines） | `.steering/20260524-add-mit-license/` | `docs/development-guidelines.md` + `docs/repository-structure.md` | 1 commit |

**詳細・受け入れ条件・タスク分解は `cowork/progress/2026-05-24_1145_directive_PI_decisions.md` を必読**。

---

## §1. 完了タスク（履歴）

### 2026-05-24 11:30 — Directive 0930 完全完了
- Part 1: Theme I C' (MP DFPT bare ε∞ 8 材料 E_b マップ) — bundle `theme_I_exciton_MP_DFPT/2026-05-24_118b3ce`
- Part 2: PI 向け解説報告書 4 本（A / Phase 1.5 / F / I）, 計 470 行, MANIFEST 引用厳守, 捏造ゼロ

### 完了テーマ（Production + 技術報告書 + PI 解説の 3 点セット完備）
- Theme A: Landé g 因子 9 材料マップ
- Phase 1.5 (A5): 光学応答 ε(ω)
- Theme F: shift current / BPVE
- Theme I: 有効質量 + 励起子 E_b（option C' + D'）

### Production bundle（6 本、すべて git_dirty:false, 必須 8 フィールド完備）
- `phase_1.5_optical/2026-05-23_31374dc/`
- `theme_A_g_factor/2026-05-23_31374dc/`
- `theme_F_shift_current/2026-05-23_ef575e3/`
- `theme_I_effective_mass/2026-05-23_1e9c65c/`
- `theme_I_exciton/2026-05-23_f66690c/` (D')
- `theme_I_exciton_MP_DFPT/2026-05-24_118b3ce/` (C')

---

## §2. ワークフロー指針

### 通常モード
1. PI からの chat or Cowork から新規 directive (`cowork/progress/*_directive_*.md`) を受領
2. 該当 directive を読み、必要なら `cowork/progress/YYYY-MM-DD_HHMM_directive_received.md` で受領確認
3. 既存規律（`CLAUDE.md` / `cowork/PRODUCTION_RULES.md` / `cowork/COWORK_CLAUDECODE_PATTERN.md`）に従い実装
4. `src/` / `docs/` 変更がある場合は **必ず `.steering/[YYYYMMDD]-[title]/` を作成**（CLAUDE.md 「機能追加・修正時の手順」）
5. 完了時に `cowork/progress/YYYY-MM-DD_HHMM_*_complete.md` で報告 + 必要なら code review request

### 質問・blocker
- `cowork/progress/YYYY-MM-DD_HHMM_question.md` または `BLOCKED_*.md`
- Cowork は 15 分巡回で対応

### 待機モード
- PI 判断待ち / 次指示待ち の場合は無理に commit しない（保守的態度を維持）
- Cowork 巡回で待機状態を確認、必要なら PI 通知

---

## §3. 重要参照ファイル

| ファイル | 内容 |
|---|---|
| `C:\Users\kteru\tb-perovskite\CLAUDE.md` | プロジェクト全体ルール（規律・docs/ 構造） |
| `C:\Users\kteru\tb-perovskite\references\CLAUDE.md` | references/ 文献コレクションのルール（ハルシネーション防止含む） |
| `cowork/PRODUCTION_RULES.md` | 本番計算ルール（MANIFEST 必須 8 フィールド等） |
| `cowork/COWORK_CLAUDECODE_PATTERN.md` | Cowork↔Claude Code 運用パターン |
| `cowork/research_ideas.md` | 研究テーマ全体像 |
| `cowork/novelty_assessment.md` | 新規性判定 |

---

## §4. v3 履歴（参照のため保持）

v3 (2026-05-23 14:40) は「PI 不在中の長時間タスクキュー」を含み、Theme F F4 ベンチマーク / Theme I 実装 / Phase 1.5 などを 10+ 時間自走で消化させる設計だった。
これら全タスクは 2026-05-24 までに完全消化済み（§1 参照）。
v3 本文の詳細は git 履歴（`git log -- cowork/next_directive.md`）から復元可能。

---

**Cowork 署名:** supervisor patrol 2026-05-24 11:45 JST (v4)
