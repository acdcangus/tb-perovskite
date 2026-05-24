# HANDOFF — セッション引き継ぎ用ドキュメント

**目的:** 別エージェント / 新セッションが **5 分でこのプロジェクトをリキャップ** できるようにする入口ファイル。
**最終更新:** 2026-05-24 11:55 JST（PI 判断 3 件 directive v4 発行直後）
**起点:** このファイル 1 本を読めば、何があるか・誰が何をするか・どこを見ればよいかが分かる。詳細は各ポインタへ。

---

## 0. プロジェクトの 30 秒サマリ

光デバイス（太陽電池・LED・光検出器・BPVE）応用を見据えた **ハライドペロブスカイト（CsBX₃, B∈{Pb,Sn,Ge}, X∈{Cl,Br,I}）の Tight-Binding (TB) 計算プロジェクト**。9 材料を一貫した TB 枠組みで横断比較し、g 因子・shift current・光学誘電関数・有効質量・励起子結合エネルギーを Production レベルで確定済み。

**完了テーマ（3 点セット = Production bundle + 技術報告書 + PI 解説）:**

- Theme A: Landé g 因子 9 材料マップ（鉛フリー Sn/Ge で正孔 g 因子普遍関係の破れを発見）
- Phase 1.5: 光学応答 ε(ω)（f-sum=0.21 で TB-Blount 限界を定量化）
- Theme F: shift current / BPVE（鉛フリー Sn/Ge ヨウ化物が Pb 系より大）
- Theme I: 有効質量 + 励起子 E_b（C' = MP DFPT 8 材料絶対マップ / D' = CsPbI₃ 校正点）

詳細サマリ: **`cowork/PI_summary_2026-05-24.md`**、**`RESULTS.md`**

---

## 1. 体制（誰が何をする）

| ロール | 担当 | 物理的所在 |
|---|---|---|
| **PI (Teruhisa Kotani, `tk`)** | 研究方針・物理判断・論文化方針 | チャット越し |
| **Cowork supervisor** | 15 分巡回、directive 起草、コードレビュー、本番ルール監視、PI 通知 | Cowork app の scheduled task `tb-perovskite-supervisor` |
| **Claude Code (実装エージェント)** | TB 実装、Production scan、報告書執筆、テスト整備、commit | ローカル Claude Code セッション |

**通信パターン:**
- PI → Claude Code: 直接 chat（Claude Code 側 UI）
- PI → Cowork: チャット（Cowork app UI、これが「あなた」が話す相手）
- Cowork → Claude Code: `cowork/progress/YYYY-MM-DD_HHMM_directive_*.md`（非同期ファイル渡し）
- Claude Code → Cowork: `cowork/progress/YYYY-MM-DD_HHMM_*_log.md` / `_complete.md` / `BLOCKED_*.md` / `_question.md`
- Cowork ↔ PI: Cowork セッションで対話（scheduled task は autonomous; PI 在席時は interactive）

詳細運用パターン: **`cowork/COWORK_CLAUDECODE_PATTERN.md`**

---

## 2. ファイル配置（最重要 10 件）

| パス | 役割 |
|---|---|
| **`cowork/HANDOFF.md`** | **★ このファイル**（入口） |
| `cowork/next_directive.md` | 現行の Claude Code 向け指示書（v4 = PI 判断 3 件反映版） |
| `cowork/PI_summary_2026-05-24.md` | 直近の PI 起床サマリ（科学成果中心） |
| `RESULTS.md` | 進捗・再現結果サマリ（科学コンテンツ） |
| `CLAUDE.md` (ルート) | プロジェクト規律: docs/ 構造、.steering/ ルール、コード規約 |
| `references/CLAUDE.md` | 文献コレクションのルール（ハルシネーション防止含む） |
| `cowork/PRODUCTION_RULES.md` | 本番計算ルール（MANIFEST 必須 8 フィールド、git_dirty:false 等） |
| `cowork/COWORK_CLAUDECODE_PATTERN.md` | Cowork ↔ Claude Code 運用パターン |
| `cowork/research_ideas.md` | 研究テーマ全体像 |
| `cowork/novelty_assessment.md` | 各テーマの新規性判定 |

**ディレクトリ層:**

```
tb-perovskite/
├── CLAUDE.md, README.md, LICENSE (MIT, Copyright "tk"), RESULTS.md, COWORK_README.md
├── src/perovskite_tb/          TB 計算エンジン
├── tests/                       pytest 231 件
├── scripts/                     実行スクリプト（scan_theme_*.py, cowork_5min_poll.ps1 = DEPRECATED）
├── configs/, data/, notebooks/  入力・パラメータ・試行
├── results/production/          ★ 6 bundle、git_dirty:false 必須、再現性 100%
├── docs/                        永続ドキュメント（理論モデル・数値解法・V&V 等 13 件）
├── .steering/                   作業単位ドキュメント（YYYYMMDD-title/ で requirements+design+tasklist）
├── references/                  49 本 + 追加 OA 論文の PDF + references.md
└── cowork/                      ★ 研究方針・指示・巡回ログ
    ├── HANDOFF.md, next_directive.md, PI_summary_*.md
    ├── PRODUCTION_RULES.md, COWORK_CLAUDECODE_PATTERN.md
    ├── research_ideas.md, novelty_assessment.md, future_themes.md
    ├── progress/                ★ 200+ ファイル（時系列の連絡ログ）
    └── reports/                 テーマ別技術報告書 + PI_explained_*.md
```

---

## 3. 現状（HEAD と健全性）

**HEAD:** `8ff17ea` (2026-05-24 02:53 UTC) — Claude Code が directive v4 を受領、LICENSE 名不整合をフラグ済み、Part 1-3 着手開始

**Production bundle 6 本（全 clean、49 連続 patrol で違反 0）:**

| bundle | git_dirty | git_commit |
|---|---|---|
| `phase_1.5_optical/2026-05-23_31374dc/` | false | 31374dc9 |
| `theme_A_g_factor/2026-05-23_31374dc/` | false | 31374dc9 |
| `theme_F_shift_current/2026-05-23_ef575e3/` | false | ef575e3c |
| `theme_I_effective_mass/2026-05-23_1e9c65c/` | false | 1e9c65c2 |
| `theme_I_exciton/2026-05-23_f66690c/` (D') | false | f66690c7 |
| `theme_I_exciton_MP_DFPT/2026-05-24_118b3ce/` (C') | false | 118b3ce7 |

**テスト:** 231 件通過維持

**ファイル数:**
- `cowork/progress/`: 200+ ファイル
- `cowork/reports/PI_explained_*.md`: 5 件（overview + A/F/Phase1.5/I, 計 742 行）
- `cowork/reports/theme_*.md`: 4 件（technical）
- PDF 文献: 49+ 件

---

## 4. ワークフロー（イベント駆動）

```
PI chat
    └─→ Cowork (Cowork app セッション)
            └─→ patrol で気付く / 直接 directive 起草
                    └─→ cowork/progress/YYYY-MM-DD_HHMM_directive_*.md
                            └─→ Claude Code が受領
                                    ├─→ cowork/progress/YYYY-MM-DD_HHMM_directive_received.md
                                    ├─→ 実装 (src/, scripts/, docs/, .steering/, cowork/reports/)
                                    ├─→ Production scan → results/production/<theme>/<date>_<hash>/
                                    ├─→ commit + push
                                    └─→ cowork/progress/YYYY-MM-DD_HHMM_*_complete.md
                                            └─→ Cowork 次 patrol でレビュー
                                                    └─→ cowork/progress/YYYY-MM-DD_HHMM_code_review.md
                                                            └─→ PI 通知（必要なら）
```

**Cowork 巡回頻度:** 15 分（scheduled task）
**Claude Code 巡回頻度:** イベント駆動（**5 分自律 polling は 2026-05-24 停止**、`scripts/cowork_5min_poll.ps1` は DEPRECATED）

---

## 5. 重要な規律（必読）

### 5.1 本番計算ルール（`cowork/PRODUCTION_RULES.md` §8）
- `results/production/<theme>/<date>_<hash>/` に保存
- **MANIFEST.json 必須 8 フィールド**: `theme`, `git_commit`, `git_dirty`, `inputs`, `outputs`, `key_numbers`, `software`, `references`
- **`git_dirty:false` 必須**（dirty な状態の Production は禁止）
- 報告書内の数値は **MANIFEST から引用、捏造禁止**
- 収束プロットを `convergence/` 配下に保存

### 5.2 CLAUDE.md 準拠（`tb-perovskite/CLAUDE.md`）
- `src/` / `docs/` を変更する作業は **必ず `.steering/[YYYYMMDD]-[title]/` を作成**
- `.steering/` には `requirements.md` / `design.md` / `tasklist.md` の 3 ファイル
- 永続 `docs/` 更新が必要なら同時実施
- 単体テスト + V&V テストを実装と並行整備

### 5.3 ハルシネーション防止（`references/CLAUDE.md`）
- 新規 arXiv PDF 取得時は**必ずタイトル照合** (`pdftotext` で先頭確認)
- 不一致なら即削除
- 出典なき数値・式を docstring / 報告書に書かない

### 5.4 ライセンス
- MIT License（`LICENSE`、Copyright `tk` = PI イニシャル、フルネーム不可）
- 新規 `.py` には `# SPDX-License-Identifier: MIT` を冒頭付与

---

## 6. 直近の意思決定ログ（2026-05-24）

| 時刻 | 主体 | 決定 | ソース |
|---|---|---|---|
| 11:40 | PI | Theme I 論文化: C' 主・D' 併記 | チャット |
| 11:40 | PI | 自律 5 分 polling 停止 | チャット |
| 11:40 | PI | LICENSE = MIT | チャット |
| 11:42 | PI | プログラムに手を入れる場合は CLAUDE.md 準拠で `.steering/` + `docs/` も整備 | チャット |
| 11:45 | Cowork | directive v4 (`...1145_directive_PI_decisions.md`) 発行 | `cowork/progress/2026-05-24_1145_*.md` |
| 11:50 | Claude Code | 受領 + LICENSE 名 `tk` 維持判断（PI 0730 supplement 尊重） | `cowork/progress/2026-05-24_1150_directive_received.md` |

過去の主要決定（前日まで）:
- 2026-05-23 0730: LICENSE Copyright 名は **`tk`**（イニシャル）、フルネーム不可
- 2026-05-23: Theme F F3 バグ自力検出（w 項欠落）→ Fregoso C2 で修正
- 2026-05-23: cowork 関連ファイルを `cowork/` サブフォルダに集約

---

## 7. オープン項目（残課題）

### 7.1 進行中（directive v4 = `cowork/progress/2026-05-24_1145_directive_PI_decisions.md`）
- Part 1: Theme I 報告書 C' 主・D' 併記再構成 + 論文骨子
- Part 2: 自律 polling DEPRECATED 化 + `.steering/20260524-deprecate-polling/` + `docs/repository-structure.md`
- Part 3: MIT LICENSE 整備（既存 LICENSE 残置）+ README + SPDX + `.steering/20260524-add-mit-license/` + `docs/development-guidelines.md`
- 3 commit に分割、緊急性は低

### 7.2 v4 後の候補（PI 判断待ち、Cowork 推奨順）
- Theme F shift current 絶対値較正（recipe 文書化済み、Hughes-Sipe 1996 + Tan&Rappe 2015 アンカー）
- 既存 .py 全件への SPDX ヘッダ一括付与（バッチ作業）
- Theme I 論文骨子の本文清書（投稿候補: npj Comput. Mater. / PRM / JPCC）
- 古典原典 16 本（Kane/Vogl/Luttinger 等）の PDF 配置 — **PI 側で D: → `references/pdfs/classic_*.pdf` に配置依頼中**
- 次の研究テーマ着手（`cowork/future_themes.md` 参照）

### 7.3 軽微な PI 確認待ち
- LICENSE Copyright 表記: `tk` のままで OK か（current 維持で進行中、変更希望なら 1 言）

---

## 8. 健全性チェックコマンド（機械検証）

新セッション開始時、以下を実行して状態を確認:

```bash
cd /sessions/<session>/mnt/tb-perovskite

# 1. HEAD と直近 commit
git log --oneline -10

# 2. Production bundle 6 本の git_dirty + 8 フィールド確認
find results/production -name MANIFEST.json | while read f; do
  python3 -c "
import json
m = json.load(open('$f'))
required = ['theme','git_commit','git_dirty','inputs','outputs','key_numbers','software','references']
missing = [k for k in required if k not in m]
print(f'$f: git_dirty={m.get(\"git_dirty\")}, missing={missing}')
"
done

# 3. 過去 30 分の cowork/progress 更新
find cowork/progress -mmin -30 -type f

# 4. テスト通過確認（時間かかる場合は skip OK）
pytest tests/ -x --tb=short -q

# 5. cowork/next_directive.md と最新 directive をペアで読む
cat cowork/next_directive.md | head -50
ls -lt cowork/progress/*directive*.md | head -3
```

---

## 9. 別エージェントでセッション再開する場合の手順（最初の 5 分）

1. **このファイル `cowork/HANDOFF.md` を読む**（全文 5 分）
2. `cowork/next_directive.md` を読み、現行作業を把握
3. `find cowork/progress -mmin -120` で直近 2 時間の連絡を確認
4. `git log --oneline -10` で最近の commit 流れを把握
5. §8 のコマンドで健全性確認
6. 必要なら `cowork/PI_summary_2026-05-24.md` と `RESULTS.md` で科学コンテンツも復習
7. 進行中の directive があれば、`cowork/progress/YYYY-MM-DD_HHMM_directive_received.md` を作成して受領確認 → 着手

**注意:**
- **Production bundle には絶対に手を入れない**（再現性破壊、PRODUCTION_RULES §8 違反）
- **MANIFEST 数値以外を報告書に書かない**（捏造禁止）
- **`src/` 変更時は `.steering/` 必須**（CLAUDE.md 「機能追加・修正時の手順」）
- **`git_dirty` で Production しない**（commit してから Production scan）
- **PI 判断要素には directive を出さない**（C-bot/Cowork が勝手に決めない）

---

## 10. このファイルの維持方針

- **更新タイミング:** 大きな PI 判断、テーマ完了、体制変更、stale 化したとき
- **更新責任:** Cowork supervisor（patrol で気付いたら更新）
- **重複防止:** 詳細は各ポインタ先に置き、本ファイルは入口に徹する
- **長さ目安:** 1 画面で 80% リキャップできる粒度

---

**Cowork 署名:** 初版 supervisor patrol 2026-05-24 11:55 JST
