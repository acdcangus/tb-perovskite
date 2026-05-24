# HANDOFF — セッション引き継ぎ用ドキュメント

**目的:** 別エージェント / 新セッションが **5 分でこのプロジェクトをリキャップ** できるようにする入口ファイル。
**最終更新:** 2026-05-24 15:45 JST（レビューサイクル収束 + PI 判断「巡回停止」を反映）
**起点:** このファイル 1 本を読めば、何があるか・誰が何をするか・どこを見ればよいかが分かる。詳細は各ポインタへ。

> **★ 現時点の運用状況 (2026-05-24 15:45 JST):** プロジェクトは narrative + code 両面で**収束**。`tb-perovskite-supervisor`（15 分巡回 scheduled task）は PI 指示により **disable 済**。`tb-perovskite-novelty-watch`（週 2 回・月木 9:00）は継続。Round 1-7 のレビューサイクル完了、論文化フェーズに移行可能。

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
| **Cowork supervisor** | directive 起草、コードレビュー、本番ルール監視、PI 通知 | Cowork app の scheduled task `tb-perovskite-supervisor`（**2026-05-24 15:40 JST disabled**, 再開は PI が手動で enable） |
| **Cowork novelty-watch** | 週 2 回（月木 9:00）新規性監視、競合論文追跡 | scheduled task `tb-perovskite-novelty-watch`（継続稼働中） |
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

**HEAD:** `03c7c1c` (2026-05-24 04:49 UTC) — R4-STD-2/3 (claude code): `HBAR2_OVER_M0` を `src/perovskite_tb/_constants.py` に一元化 + `compute_g_factor` docstring に Roth-Lax-Zwerdling 1959 (PR 114, 90) anchor 追加

**直近 commit 流れ (8ff17ea 以降の 7 commit):**

```
03c7c1c R4-STD-2/3 (claude code): centralize HBAR2_OVER_M0 + g_factor citation anchor
e887df4 R3-DEEP response (claude code): resolve R3-DEEP-1/2/4/6 (PI deep-review clarity findings)
df2b4ca review round 5 (claude code): independent line-by-line review R1-R5 — 5 findings (R5-CC-1..5)
c17ff2a review round 4 (claude code): resolve R3-COW-1..4 (narrative-only)
f95230e review round 3 (claude code): R3-CC-1 — flag web-derived citations as unverified
779ee0f review round 2+ (claude code): web-verified citation fixes (Tanaka 2003 / Yang 2017)
a2e0f0c review round 2 (claude code + cowork): R2-1 + R6/R7/R10 round-1 findings
```

**Production bundle 6 本（全 clean、定数値 7.619964 不変なので rerun 不要）:**

| bundle | git_dirty | git_commit |
|---|---|---|
| `phase_1.5_optical/2026-05-23_31374dc/` | false | 31374dc9 |
| `theme_A_g_factor/2026-05-23_31374dc/` | false | 31374dc9 |
| `theme_F_shift_current/2026-05-23_ef575e3/` | false | ef575e3c |
| `theme_I_effective_mass/2026-05-23_1e9c65c/` | false | 1e9c65c2 |
| `theme_I_exciton/2026-05-23_f66690c/` (D') | false | f66690c7 |
| `theme_I_exciton_MP_DFPT/2026-05-24_118b3ce/` (C') | false | 118b3ce7 |

key_numbers 合計 159、convergence 完備、必須 8 フィールド完備。**MANIFEST はレビューサイクル中一切変更されず**（narrative + code-quality のみ）。

**テスト:** 231 passed in ~20s（HEAD で再現確認、`git archive` 経由 fresh snapshot）

**ファイル数（現在）:**
- `cowork/progress/`: 220+ ファイル
- `cowork/reports/PI_explained_*.md`: 5 件（overview + A/F/Phase1.5/I）
- `cowork/reports/theme_*.md`: 4 件（technical）
- `.steering/`: 直近 `20260524-code-quality-r4std/`, `20260524-deprecate-polling/`, `20260524-add-mit-license/` ほか
- PDF 文献: 49 (arXiv) + Boyer-Richard 2016 ほか追加分

### 3.1 既知の infrastructure issue: R5-COW-1 (継続中)

Cowork sandbox の bash mount が **stale snapshot** を返す:
- `git status` が `fatal: unknown index entry format 0xd5fc0000` を出す
- `git diff HEAD --stat` が偽差分（reports や src の disk バイト数が HEAD より小さい）
- `src/perovskite_tb/exciton.py` を bash 経由で import すると `SyntaxError`（truncated）

**PI local repo は健全**（Claude Code 1520 で `git diff HEAD` 空を確認済み）。Cowork sandbox のみの問題で、HEAD コンテンツ自体は完全。検証は **必ず `git show HEAD:<path>` または `git archive HEAD | tar -x` 経由**で行うこと（disk 直接アクセスは信頼不可）。

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

**Cowork 巡回頻度:** ~~15 分（scheduled task）~~ → **2026-05-24 15:40 JST disabled**（PI 指示によりトークン消費抑制のため）。再開時は PI が手動で `tb-perovskite-supervisor` を enable。
**Cowork novelty-watch 頻度:** 週 2 回（月・木 9:00 JST、軽量、継続稼働）
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
| 12:00 | PI | レビュー protocol standing rule（互いに独立して逐行レビュー、両者ゼロまで継続）| `cowork/progress/2026-05-24_1200_*.md` |
| 12:20-15:20 | Cowork ↔ CC | **レビューサイクル Round 1-7**（narrative + code）完走。Round 6/7 で双方ゼロ達成見込み | `cowork/progress/2026-05-24_1220..1540_*.md` |
| 14:35 | Cowork | PI deep review (R3-DEEP-1〜6) 起票 — overview の用語混在・脚注不足を発見 | `cowork/progress/2026-05-24_1435_pi_deep_review.md` |
| 15:05 | Claude Code | R3-DEEP-1/2/4/6 解決（commit `e887df4`）, 3/5 は deferred 妥当 | `cowork/progress/2026-05-24_1505_*.md` |
| 15:20 | Claude Code | R4-STD-2 (DRY) + R4-STD-3 (citation anchor) 実装 (commit `03c7c1c`), R5-COW-1 close（PI local repo 健全） | `cowork/progress/2026-05-24_1520_*.md` |
| 15:40 | PI | **「プロジェクトが収束したらパトロール止めていい。トークン消費を抑えたい」** | チャット |
| 15:40 | Cowork | Round 7 標準 6 観点合格判定 → `tb-perovskite-supervisor` scheduled task **disable** | `cowork/progress/2026-05-24_1540_code_review_03c7c1c_R7.md` |

過去の主要決定（前日まで）:
- 2026-05-23 0730: LICENSE Copyright 名は **`tk`**（イニシャル）、フルネーム不可
- 2026-05-23: Theme F F3 バグ自力検出（w 項欠落）→ Fregoso C2 で修正
- 2026-05-23: cowork 関連ファイルを `cowork/` サブフォルダに集約

### 6.1 レビューサイクル Round 1-7 サマリ

| Round | Cowork 指摘 | Claude Code 指摘 | 主要 commit |
|---|---|---|---|
| 1 | 17 | 4 (unique 16) | a2e0f0c, cfa8172, 259089f |
| 2 | 1 (R2-1) | 5 + 3 web | 779ee0f, a2e0f0c |
| 3 | 4 (R3-COW-1〜4) | 1 (R3-CC-1) | c17ff2a, f95230e |
| 3-DEEP | 6 (R3-DEEP-1〜6) | — | e887df4 |
| 4 | — | 0 (R3-COW 解決) | c17ff2a |
| 5 | 1 (R5-COW-1, infrastructure) | 5 (R5-CC-1〜5) | df2b4ca |
| 6 | 0 (narrative 全合格) | — | — |
| **7** | **0 (R4-STD-2/3 src 実装合格)** | (自己レビュー次回) | **03c7c1c** |

**到達点:**
- narrative: Boyer-Richard 引用修正、Blount 1962 書誌 flag 統一（8 箇所）、overview に用語表（Eg 実験 / TB 吸収端 / TB gap@R）追加、bare ε∞ 手法散乱補足、Δ±20% 不確かさ脚注追加
- code: `HBAR2_OVER_M0` を `_constants.py` に singleton 化（4 モジュールで `is` 比較同一）、`compute_g_factor` に Roth-Lax-Zwerdling PR 114, 90 anchor 追加、テスト 231/231
- Production: 6 bundle すべて git_dirty:false、key_numbers 計 159、MANIFEST 変更ゼロ、定数値不変なので rerun 不要

---

## 7. オープン項目（残課題）

### 7.1 完了済（directive v4 = `cowork/progress/2026-05-24_1145_directive_PI_decisions.md`）

Part 1-3 はレビューサイクル Round 1-7 で消化済み:
- Part 1: Theme I 報告書 C' 主・D' 併記 → reports/PI_explained_overview.md + theme_I 系すべて反映
- Part 2: 自律 polling DEPRECATED 化 → `.steering/20260524-deprecate-polling/` + docs 反映済
- Part 3: MIT LICENSE 整備 → LICENSE / README / SPDX ヘッダ整備済

加えて Round 1-7 で追加的に:
- R3-DEEP-1/2/4/6: overview 用語表・bare ε∞ 散乱補足・Δ±20% 脚注
- R4-STD-2: `HBAR2_OVER_M0` を `_constants.py` に singleton 化（src/ 4 モジュール）
- R4-STD-3: `compute_g_factor` docstring に Roth-Lax-Zwerdling 1959 anchor
- R5-CC-1〜5: Boyer-Richard 引用修正、Blount 1962 書誌 flag 統一、g_h 慣例明記

### 7.2 軽微な残作業（論文化と並行可能、緊急性なし）

- **R4-STD-1 (type hints)**: `shift_current` 内部 helper 17 関数の戻り値型ヒント。`.steering/20260524-code-quality-r4std/` で追跡中、deferred
- **R3-DEEP-3/5**: overview narrative の minor clarity 指摘、Cowork 指示で deferred
- **PDF backlog 3 件（OA 一次取得）**:
  1. Yang 2017 PRB 96, 035301 — 別 OA 一次出典で差替が最善
  2. CsPbCl₃ 64–77 meV magneto-optical (Photonics Research 8, A50, 2020) — WEB-SEARCH DERIVED flag 済
  3. Blount 1962 — 書誌 SSP 13,305 / PR 126,1636 のどちらが正かを OA で確認
- **R5-COW-1 infrastructure**: Cowork sandbox bash mount stale。PI local 側 `git status && git diff HEAD` が clean なら close（local では確認済）

### 7.3 v4 後の候補（PI 判断待ち、Cowork 推奨順）

- **Theme I 論文本文清書** ★ 最優先（投稿候補: npj Comput. Mater. / PRM / JPCC; 骨子は `cowork/reports/theme_I_publication_outline.md` 既存）
- Theme F shift current 絶対値較正（recipe 文書化済、Hughes-Sipe 1996 + Tan&Rappe 2015 アンカー）
- 古典原典 16 本（Kane/Vogl/Luttinger 等）の PDF 配置 — **PI 側で D: → `references/pdfs/classic_*.pdf` に配置依頼中**
- 既存 .py 全件への SPDX ヘッダ一括付与（バッチ作業; 主要モジュールは 03c7c1c で対応済）
- 次の研究テーマ着手（`cowork/future_themes.md` 参照）

### 7.4 軽微な PI 確認待ち
- LICENSE Copyright 表記: `tk` のままで進行中（変更希望なら 1 言）
- 巡回再開の判断: 新テーマ着手や追加 directive 必要時に `tb-perovskite-supervisor` を手動 enable

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
2. `cowork/next_directive.md` と `cowork/progress/2026-05-24_1540_code_review_03c7c1c_R7.md`（最終 patrol）を読み、収束時点の状態を把握
3. `git log --oneline -10` で最近の commit 流れを把握（HEAD = `03c7c1c`）
4. `cowork/PI_summary_2026-05-24.md` + `RESULTS.md` で科学コンテンツを復習
5. §8 のコマンドで健全性確認（mount-safe 版 = `git archive HEAD | tar -x` 推奨）
6. 巡回再開の必要があれば `tb-perovskite-supervisor` scheduled task を enable（PI 確認後）

**注意:**
- **Cowork sandbox の bash mount は stale 可能性あり**（R5-COW-1）。`cat src/...` や `pytest` を直接実行する前に、`git archive HEAD | tar -x -C /tmp/<work>` で fresh snapshot を作って検証すること。PI local repo は健全
- **Production bundle には絶対に手を入れない**（再現性破壊、PRODUCTION_RULES §8 違反）
- **MANIFEST 数値以外を報告書に書かない**（捏造禁止）
- **`src/` 変更時は `.steering/` 必須**（CLAUDE.md 「機能追加・修正時の手順」）
- **`git_dirty` で Production しない**（commit してから Production scan）
- **PI 判断要素には directive を出さない**（Cowork が勝手に決めない）
- **物理定数を新規追加する場合は `src/perovskite_tb/_constants.py` に置く**（DRY 規律、Round 7 で確立）

---

## 10. このファイルの維持方針

- **更新タイミング:** 大きな PI 判断、テーマ完了、体制変更、stale 化したとき
- **更新責任:** Cowork supervisor（patrol 復活時）、PI 在席セッション時に Cowork または Claude Code
- **重複防止:** 詳細は各ポインタ先に置き、本ファイルは入口に徹する
- **長さ目安:** 1 画面で 80% リキャップできる粒度

---

**Cowork 署名:**
- 初版 supervisor patrol 2026-05-24 11:55 JST
- v2 update 2026-05-24 15:45 JST（Round 7 収束 + PI「巡回停止」反映 + R5-COW-1 mount-safe ガイダンス追記）
