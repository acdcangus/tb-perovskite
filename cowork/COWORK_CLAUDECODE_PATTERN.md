# Cowork × Claude Code 継続的協調パターン（汎用ガイド）

**初版:** 2026-05-23（tb-perovskite プロジェクトでの実証から抽出）
**対象:** Cowork デスクトップアプリのユーザーで、Claude Code（CLI）と組み合わせて研究・開発を進めたい人
**読み方:** 上から順に。テンプレートはそのままコピペ可

---

## このパターンが解く問題

Cowork（GUI）と Claude Code（CLI）はそれぞれ独立したセッションを持ち、**直接の通信路がない**。ユーザーが両者の間で「メッセンジャー」をやるのは大変。

**このパターンでは:**
- Cowork が「監督役」となり、Claude Code の作業を **ファイル経由で非同期にレビュー・指示**
- Cowork の scheduled task が定期巡回（15分ごと等）して自動で動く
- 物理的な実装・計算は全て Claude Code、研究方針・新規性検証は Cowork
- ユーザーは大局判断と方向転換だけに集中できる

実証：1日で論文値再現済み TB エンジン → g因子計算モジュール → 9材料スキャン → 報告書 draft → 光学物性計算 → 9材料光学スキャン まで完了

---

## 役割分担

### Cowork（GUI、監督役）が担う
- 文献検索・新規性検証（WebSearch、ChromeMCP、scheduled task）
- 研究テーマの提案・優先順位付け
- Claude Code のコードレビュー（物理的妥当性、出典確認）
- ハルシネーション検出（自分自身も含む！）
- ユーザーへの重要判断のエスカレーション
- 文献 PDF の追加収集
- 進捗の定期巡回

### Claude Code（CLI、実装役）が担う
- ソースコード実装
- 数値計算実行
- テスト作成・実行
- 論文値の数値再現
- 報告書ドラフト
- git commit / コミット履歴管理
- 行き詰まり時の SOS 発信

### ユーザーが担う
- 全体方針の決定（テーマ選択、優先度変更）
- 物理的判断（モデル選択、近似の妥当性）
- 大局的なレビュー（Cowork が出した結果の検査）
- Claude Code への kick（「続けて」と言う、または特定の指示）

---

## フォルダ構造テンプレート

プロジェクトのルートに `cowork/` サブフォルダを作る：

```
<project_root>/
├── CLAUDE.md                  # 既存：プロジェクトの開発標準（触らない）
├── README.md, RESULTS.md, ... # 既存：プロジェクトドキュメント
├── COWORK_README.md           # ★新規：cowork/ への案内（目印）
├── src/, tests/, ...          # 既存：実装本体（触らない）
└── cowork/                    # ★新規：Cowork 駆動の研究管理
    ├── next_directive.md      # 現行指示書（Cowork が更新）
    ├── research_ideas.md      # テーマ全体像（テンプレ後述）
    ├── novelty_assessment.md  # 新規性判定（週次更新）
    ├── progress/              # 非同期通信ログ
    │   ├── YYYY-MM-DD_HHMM_code_review.md       # Cowork → Claude Code
    │   ├── YYYY-MM-DD_HHMM_directive_update.md  # Cowork → Claude Code
    │   ├── YYYY-MM-DD_HHMM_*_log.md             # Claude Code の作業ログ
    │   ├── YYYY-MM-DD_HHMM_*_review_request.md  # Claude Code → Cowork
    │   ├── YYYY-MM-DD_HHMM_*_complete.md        # Claude Code 完了通知
    │   └── BLOCKED_*.md                         # Claude Code の SOS
    └── reports/               # テーマ別公開向け報告書
        ├── theme_A_xxx.md
        └── theme_B_yyy.md
```

**重要:** 既存の `CLAUDE.md`（プロジェクト開発標準）と `cowork/next_directive.md`（Cowork 指示）は **役割が違うので分けて運用**。CLAUDE.md は触らない。

---

## ファイル種別と命名規則

### `cowork/progress/` 内ファイル

| ファイル名 | 書き手 | 役割 |
|---|---|---|
| `YYYY-MM-DD_phase{N}_log.md` | Claude Code | 日次の作業ログ。サブタスク進捗・数値結果・行き詰まり |
| `YYYY-MM-DD_HHMM_review_request.md` | Claude Code | レビュー依頼（commit hash + 観点を明記） |
| `YYYY-MM-DD_HHMM_*_complete.md` | Claude Code | フェーズ完了通知 |
| `YYYY-MM-DD_HHMM_question.md` | Claude Code | ユーザーへの質問（Cowork が拾って通知） |
| `BLOCKED_<topic>.md` | Claude Code | 完全に行き詰まったときの SOS |
| `YYYY-MM-DD_HHMM_code_review.md` | **Cowork** | レビュー応答 |
| `YYYY-MM-DD_HHMM_directive_update.md` | **Cowork** | 補足指示 |
| `YYYY-MM-DD_HHMM_directive_correction.md` | **Cowork** | 自己訂正（ハルシネーション発見時） |
| `YYYY-MM-DD_HHMM_novelty_check.md` | **Cowork** | 新規性監視の結果 |

### `cowork/reports/` 内ファイル

| ファイル名 | 役割 |
|---|---|
| `theme_<X>_<short_name>.md` | テーマごとの公開向け報告書（成功/失敗問わず作成） |

---

## スケジュールタスクの設計

Cowork の `mcp__scheduled-tasks__create_scheduled_task` で 2 つ作る。

### Task 1: supervisor（15 分ごと）

```
cronExpression: */15 * * * *
notifyOnCompletion: false  （頻繁すぎる通知を避ける）
```

**プロンプトテンプレート:**

```
あなたは <PROJECT_NAME> プロジェクトの監督エージェントです。
Claude Code が <PROJECT_ROOT> で進めている作業の進捗を 15 分ごとに確認します。

## やること

1. <PROJECT_ROOT>/cowork/progress/ の過去 30 分以内に更新されたファイルを全て読む
   - 特に BLOCKED_*.md、*_review_request.md、*_question.md を最優先
2. bash で git log --oneline -10、git show HEAD --stat を確認
3. レビュー依頼があれば cowork/progress/YYYY-MM-DD_HHMM_code_review.md で返答
4. BLOCKED があれば cowork/progress/YYYY-MM-DD_HHMM_directive_update.md で補足指示
5. 重要判断が必要ならこのセッションで報告（ユーザーへの通知）

## レビューの観点

- 物理的正しさ（出典との一致）
- 検証の十分性
- 既存テストを壊していないか
- ハルシネーション防止：docstring に出典が明記されているか

## 出力サマリ

最後に以下を出してください:
## 巡回結果 (YYYY-MM-DD HH:MM)
- 確認したファイル数: N
- レビュー依頼: あり/なし
- BLOCKED: あり/なし
- 最新コミット: <hash>
- 進捗判定: 順調 / 要注意 / 行き詰まり
```

### Task 2: novelty-watch（週 1〜2 回）

```
cronExpression: 0 9 * * 1,4   （月・木 9:00）
notifyOnCompletion: true  （重大発見時の通知用）
```

**プロンプトテンプレート:**

```
あなたは <PROJECT_NAME> プロジェクトの新規性監視エージェントです。
進行中の研究テーマが本当に新規であり続けているか厳密に検証します。

## 監視対象

<PROJECT_ROOT>/cowork/novelty_assessment.md を読み、現在進行中のテーマをリストアップ。

## 検索プロトコル（各テーマ）

1. arXiv 新着スキャン: WebFetch で cond-mat.mtrl-sci/recent 等
2. WebSearch でテーマ別深掘り（最低 4 つのクエリ、表記揺れも全て試す）
3. 既収集論文との重複チェック（references.md を Grep）

## 判定

- ✅ 新規性堅持
- 🟡 要注意（部分重複）
- ⚠️ 危険信号（即時ユーザー通知）
- ❌ scooped（テーマ変更必須）

## 出力

1. cowork/progress/YYYY-MM-DD_HHMM_novelty_check.md（必ず作成）
2. cowork/novelty_assessment.md の更新履歴に追記（変更あれば）
3. ⚠️ または ❌ ならユーザー通知
```

---

## 進捗ログのフォーマット（Claude Code 用）

```markdown
# Phase N 進捗ログ: YYYY-MM-DD

## サブタスク状況
- [x] A1 文献読み込み（commit abc123）
- [ ] A2 実装（着手中）

## 本日のハイライト
- ...

## 数値結果
| 項目 | 値 | 論文値 | 差 | 判定 |
|---|---|---|---|---|
| CsPbI3 g_e | X.XX | Y.YY | Z% | ✅ |

## 行き詰まったこと / 判断に迷うこと（Cowork へ）
（あれば。Cowork が次回巡回時に拾う）

## レビュー依頼
（あれば。commit hash と観点を明記）

## 次にやること
- ...
```

---

## 報告書のフォーマット（reports/ 用）

```markdown
# Theme X: <タイトル>

**ステータス:** 完了 / 部分完了 / 失敗（理由）
**実施期間:** YYYY-MM-DD 〜 YYYY-MM-DD
**コミット範囲:** abc123..def456

## 1. 動機と仮説
## 2. 方法（出典必須）
## 3. 主要結果（数値・図）
## 4. 論文値との比較・整合性
## 5. 物理的考察
## 6. 学会・論文化の見通し
## 7. 限界・残課題
## 8. 再現コマンド
## 9. 関連ファイル
```

**重要:** 結果が面白くなくても必ず報告書を書く。ネガティブ結果も科学的価値あり。

---

## ハルシネーション防止の絶対ルール

`cowork/next_directive.md` の冒頭に必ず記載：

```markdown
## 0. ハルシネーション防止の絶対ルール（必読）

1. アルゴリズムの出典が論文 DOI/arXiv ID + 式番号で特定できること
   - 「教科書通り」「標準的手法」だけでは不十分
2. 論文の式と実装コードの対応を docstring に明示
   - 例: # Implements Eq. (5) of Kirstein 2021 (arXiv:2112.15384)
3. 論文の値を再現できないものは「再現困難」と報告（値を改竄しない）
4. 論文に明示されていない数値・パラメータは Cowork に文献調査を依頼
5. 不明な式の導出を要求された場合、紙計算で出典と整合確認してから実装
```

これは Cowork も自分自身に課す。**Cowork 自身がハルシネーションしたら自己訂正 `directive_correction.md` を書く**（実例あり）。

---

## 「30 分ルール」（Claude Code 用）

```
30 分以上行き詰まったら、cowork/progress/.../「行き詰まったこと」に詳細を書いて
そこで一旦止まる。Cowork が次回巡回時に拾う。
```

これで Claude Code は自走と無謀な推測の中間を取れる。

---

## 高頻度ループの実現

Claude Code 側のルール:
- **サブタスク完了ごと** または **git commit ごと** に `cowork/next_directive.md` を読み直す
- コミット直前に `cowork/progress/*code_review*.md` の新着を確認

Cowork 側:
- 15 分ごとの supervisor タスクが進捗を巡回
- レビュー応答や directive 更新を書く

ユーザー側:
- 「続けて」「次は？」程度のキック
- 上記の汎用テンプレ「`cowork/progress/` と `cowork/next_directive.md` を読んで続けて」

---

## ユーザーが介入すべきタイミング

1. **大きな方向転換**：テーマ追加・削除、優先度シフト
2. **物理的判断**：モデル次数（2-band か 4-band か等）、近似の妥当性
3. **重大な scoop 検出**：novelty 監視からの通知
4. **ループが完全に止まったとき**：自動巡回で検出して通知
5. **論文化判断**：報告書のクオリティ評価、投稿先選択

これ以外は放置で OK。

---

## 新規プロジェクトへの適用手順

1. **既存プロジェクトに `cowork/` フォルダを作る**
   ```bash
   mkdir -p <project_root>/cowork/progress
   mkdir -p <project_root>/cowork/reports
   ```

2. **`COWORK_README.md` をプロジェクトルートに置く**（このパターンガイドを参考に、プロジェクト固有の説明を書く）

3. **`cowork/next_directive.md` v1 を Cowork に書かせる**
   - ユーザーから Cowork に「このプロジェクトで X を研究したい」と依頼
   - Cowork が文献調査 + research_ideas.md を作成
   - その中から優先順位 1 位を next_directive.md に展開

4. **2 つの scheduled task を Cowork で作る**（テンプレート使用）

5. **Claude Code に「`cowork/next_directive.md` を読んで Phase 1 を開始」と一言**

6. **以後、Claude Code が止まったら「`cowork/progress/` と `cowork/next_directive.md` を読んで続けて」と一言**

---

## 期待される動き（実例）

tb-perovskite プロジェクトでの 1 日の動き：

| 時刻 | イベント | 主体 |
|---|---|---|
| 07:00 | リサーチ開始、49 本の文献収集 | Cowork |
| 07:15 | research_ideas.md 作成、5 テーマ提案 | Cowork |
| 07:20 | next_directive.md v1 発行（Theme A: g因子） | Cowork |
| 07:23 | A1 (文献読み込み) 完了 | Claude Code |
| 07:27 | A1 のレビュー応答書く | Cowork（手動） |
| 07:40 | A2 (実装) 完了、レビュー依頼 | Claude Code |
| 07:50 | A4+A5 (スキャン+報告書) 完了 | Claude Code |
| 08:11 | supervisor 自動起動、レビュー作成 | Cowork supervisor |
| 08:31 | A6 (TB-derived P) 完了 | Claude Code |
| 08:40 | Phase 1.5 B4-B5 (光学9材料スキャン) 完了 | Claude Code |
| 09:00 | supervisor 自動レビュー、Theme F 着手指示 | Cowork supervisor |
| 09:12 | supervisor 自己訂正（ハルシネーション発見） | Cowork supervisor |

**ポイント:** ユーザーが介入したのは 3-4 回程度。あとは全自動でループが回った。

---

## トラブルシューティング

| 症状 | 原因 | 対処 |
|---|---|---|
| Claude Code が同じ作業を繰り返す | progress/ を読んでない | 「`cowork/progress/` を確認してから続けて」 |
| Cowork supervisor が止まる | Cowork app が閉じている | Cowork app を開く（次回起動時に巡回再開） |
| ハルシネーションを発見 | Cowork が出典確認怠った | Cowork 自身が `directive_correction.md` を書いて自己訂正 |
| Claude Code が無謀に推測する | 30 分ルール忘れ | next_directive.md §0 を強調、再周知 |
| トークン消費が大きい | 巡回頻度過剰 | supervisor 間隔を 15 分 → 30 分等に伸ばす |

---

## 制約・限界

- **真のリアルタイム連携は不可**：Cowork → Claude Code は scheduled task 経由で 15 分粒度
- **Claude Code の自動トリガーは別途必要**：Windows Task Scheduler や PowerShell ループで `claude --continue -p` を回す（API トークン要注意）
- **本パターンは「監督される側 = Claude Code」前提**：Claude Code が「指示を読む」習慣を持つことに依存
- **ユーザーの大局判断は依然必要**：方向転換は人間が決める

---

## ライセンス・引用

このパターンは tb-perovskite プロジェクト（2026-05-23）で実証されたものです。自由に転載・改変して構いません。

参考：
- Cowork デスクトップアプリ（Anthropic）
- Claude Code CLI（Anthropic）
- 本パターンの実証ログ: `cowork/progress/` （tb-perovskite）

---

## まとめ（一言で）

> **Cowork が監督役、Claude Code が実装役、ユーザーが大局役。 通信は `cowork/` フォルダのファイル経由。 supervisor タスクで 15 分ごとに自動巡回。 これで研究が回る。**
