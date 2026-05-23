# progress/ — Claude Code と Cowork 監督の連絡用ディレクトリ

このフォルダは Claude Code（実装担当）と Cowork（監督・レビュー担当）の **非同期コミュニケーション** に使います。Slack のような場所だと思ってください。

## ファイル命名規則

| ファイル | 書き手 | 用途 |
|---|---|---|
| `YYYY-MM-DD_phase1_log.md` | Claude Code | 日次の作業ログ。サブタスク進捗、数値結果、行き詰まり |
| `YYYY-MM-DD_HHMM_review_request.md` | Claude Code | レビュー依頼（commit hash と観点を明記） |
| `YYYY-MM-DD_HHMM_code_review.md` | Cowork | レビュー返答 |
| `YYYY-MM-DD_HHMM_directive_update.md` | Cowork | 次の指示の差し込み（緊急時、next_directive.md とは別の補足） |
| `YYYY-MM-DD_HHMM_question.md` | Claude Code | ユーザーへの質問（Cowork が拾って通知） |
| `BLOCKED_<topic>.md` | Claude Code | 完全に行き詰まったときの SOS。あれば Cowork が最優先で見ます |

## 進捗ログの推奨フォーマット

```markdown
# Phase N 進捗ログ: 2026-MM-DD

## サブタスク状況
- [x] A1 文献読み込み（commit abc123）
- [ ] A2 実装（着手中）
- [ ] A3 テスト
- [ ] A4 スキャン
- [ ] A5 解析

## 本日のハイライト
- ...

## 数値結果
| 項目 | 値 | 論文値 | 差 | 判定 |
|---|---|---|---|---|
| CsPbI3 g_e (Kashikar 13orb) | X.XX | Kirstein Y.YY | Z% | ✅/⚠️/❌ |

## 行き詰まったこと / 判断に迷うこと
（あれば。Cowork が次回巡回時に拾います）

## レビュー依頼
（あれば。commit hash と観点を明記）

## 次にやること
- ...
```

## レビュー依頼の例

```markdown
# Code Review Request: 2026-05-25 14:30

- **対象:** src/perovskite_tb/g_factor.py (commit 7f8a9b2)
- **観点:**
  - Roth-Lax 公式の TB 表現が docs/g-factor-formulation.md Eq.(7) と一致しているか
  - 速度演算子の解析微分が既存 hamiltonian.py との符号規約で整合しているか
- **急ぎ度:** 通常
- **添付:** results/g_factors/test_run_csPbI3.png
```

## 緊急連絡（SOS）

完全に行き詰まって自分では判断できない場合は `BLOCKED_<topic>.md` を作ってください。Cowork が次回巡回時に最優先で対応します。Cowork で解決できなければユーザーに通知します。

例: `BLOCKED_g_factor_sign_convention.md`
