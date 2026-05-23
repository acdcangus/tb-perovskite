# Cowork 研究フォルダ案内（プロジェクトルートに置く目印）

**作成:** 2026-05-23
**目的:** Cowork（Claude Cowork app）駆動の研究関連ファイルがどこにあるかを Claude Code 等に明示する。

## ファイル配置

- **`cowork/next_directive.md`** — Cowork から Claude Code への現行指示書
- **`cowork/research_ideas.md`** — 研究テーマ全体像（5本のテーマ案、優先度付き）
- **`cowork/novelty_assessment.md`** — 各テーマの新規性判定（週 2 回更新）
- **`cowork/progress/`** — Cowork ↔ Claude Code 非同期通信
  - `YYYY-MM-DD_HHMM_code_review.md` — Cowork からのコードレビュー応答
  - `YYYY-MM-DD_HHMM_directive_update.md` — 補足指示
  - `YYYY-MM-DD_HHMM_*_log.md` — Claude Code の進捗ログ
  - `YYYY-MM-DD_HHMM_*_review_request.md` — Claude Code からのレビュー依頼
  - `BLOCKED_*.md` — Claude Code の SOS
- **`cowork/reports/`** — テーマごとの公開向け報告書
  - `theme_A_g_factor.md` 等

## Claude Code 起動時の推奨アクション

セッション開始時、もしくは作業区切り（commit ごと）に以下を確認してください：

1. `cowork/progress/` の **過去 30 分以内に更新されたファイル**を `ls -lat` で確認
2. 新着の `*_code_review.md` や `*_directive_update.md` があれば Read
3. `cowork/next_directive.md` も最新版を Read
4. 未完の作業を続けるか、新しい指示に従う

## 自動巡回スケジュール（Cowork 側）

- **supervisor**: 15 分ごと（progress/ 巡回、レビュー作成）
- **novelty-watch**: 月・木 9:00（新規性監視）

## 開発プロジェクト本体との分離

`cowork/` は **科学的な研究管理用**のサブフォルダで、以下の本体プロジェクト構造とは独立です：

- `src/perovskite_tb/` — TB 計算エンジン実装
- `tests/` — pytest テスト
- `data/parameters/` — 論文出典付きパラメータ JSON
- `configs/` — k 経路設定など
- `results/` — 計算結果（バンド図、g 因子 CSV、光学スペクトル）
- `scripts/` — 実行スクリプト
- `notebooks/` — 試行錯誤・可視化
- `docs/` — 永続ドキュメント（科学的記述）
- `.steering/` — 作業単位ドキュメント
- `references/` — 49 本の文献コレクション

`cowork/` 配下のドキュメントは「研究方針」「指示」「巡回ログ」が中心で、上記の科学コンテンツとは性質が違います。

## 移動日付

2026-05-23 — Cowork（Claude Cowork app）で以下を `cowork/` に移動：
- `next_directive.md`
- `research_ideas.md`
- `novelty_assessment.md`
- `progress/`
- `reports/`
