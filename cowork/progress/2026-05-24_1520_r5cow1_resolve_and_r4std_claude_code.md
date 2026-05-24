# R5-COW-1 解決 + R4-STD 対応 — Claude Code — 2026-05-24 15:20

Cowork Round 5 patrol（`1440`, R5-COW-1）+ 標準6観点レビュー（`1445`, R4-STD-1〜3）に対応。

## A. ★ R5-COW-1（disk-HEAD 乖離）の真因確定 → **候補(A): Cowork sandbox mount stale のみ。ユーザー repo は健全**

Cowork は bash/disk 経由で reports 全 10 本が HEAD より truncated に見えると報告（theme_I_exciton disk 5099 vs HEAD 7255 等）。私の環境で厳密検証:

| 検証 | 結果 |
|---|---|
| `git status` | **正常**（index 破損なし。Cowork 側の `unknown index entry format` は再現せず） |
| `git diff HEAD` | **空**（working tree = HEAD, 未コミット差分ゼロ） |
| 各 report の `git show HEAD` vs working tree バイト数 | **全て一致**（overview 19878=19878, theme_I_exciton 7255=7255, PI_explained_theme_I 8977=8977, theme_A 11508=11508, theme_F 9607=9607） |

➡️ **ユーザーのローカル working tree は truncation ゼロ・git clean**。Cowork が見た短縮版は **sandbox mount の stale snapshot**（R3-DEEP-5 と同根）。`git checkout HEAD --` は不要。
➡️ 私の Round 1〜5 の編集は full content 上で行われていた（末尾 §出典 を編集でき、バイト数が HEAD 一致 = 証拠）。**実害なし**。
➡️ **運用教訓**: Cowork patrol の file 検証は bash cat/wc ではなく Read tool か `git show HEAD:<path>` を使う（R3-DEEP-5 を再確認）。

## B. R4-STD（標準6観点 minor 3 件）対応

PI「通常のきじゅんでレビューして」→ Cowork 標準6観点レビューは**総合合格・論文化に十分耐える**判定。code-quality minor 3 件:

| ID | 内容 | 対応 | 検証 |
|---|---|---|---|
| **R4-STD-2** | `HBAR2_OVER_M0=7.619964` が4モジュール重複（DRY） | `_constants.py` 新規作成し一元化。exciton/optical/velocity は `from ._constants import HBAR2_OVER_M0`、g_factor は `as C_HBAR2_OVER_M0` で **公開名・値を完全保持** | grep: 7.619964 のコード定義は `_constants.py` のみ。smoke test で 4 モジュール一致 |
| **R4-STD-3** | g_factor 公開関数 docstring の式番号 anchor | `g_factor_kp` は既出「Kirstein 2021, Eqs.5,6」→ `compute_g_factor` に **Roth-Lax-Zwerdling 1959 (PR 114,90)** anchor 追加（モジュール docstring 既出の出典のみ使用） | — |
| R4-STD-1 | shift_current 内部 helper 17 関数の型ヒント | **deferred**（Cowork 推奨 (b)）。戻り値型を本体で検証せず付けると新たな不正確記述化のため、後続コード整備でまとめて。`.steering/20260524-code-quality-r4std/` で追跡 | — |

### CLAUDE.md 準拠
- コード変更につき `.steering/20260524-code-quality-r4std/`（requirements/design/tasklist）整備（PI v4 指示「プログラムに手を入れているなら…ドキュメント整備も」）。
- 定数値**不変**（7.619964）→ Production 数値・provenance 影響ゼロ → rerun 不要。
- **V&V: `pytest` 全 231 通過（62.85s）**。回帰なし。

## C. カウンタ / 次
- R5-COW-1 close（infrastructure, ユーザー repo 健全）。R4-STD-2/3 実装、R4-STD-1 deferred。
- 次: Cowork の独立再レビュー（本コミット = src 変更を含むため、標準6観点の物理/テスト観点で再検証してほしい）。
- 残: OA 一次確認 backlog（Blount 書誌 SSP13,305/PR126,1636・Yang 2017・CsPbCl₃ 64–77 meV）→ narrative 収束後。
