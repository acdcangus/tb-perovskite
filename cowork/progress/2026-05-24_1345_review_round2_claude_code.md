# Review Round 2 — Claude Code（R2-1 対応 + R6/R7/R10 Round-1 自己レビュー）— 2026-05-24 13:45

Cowork Round 2（`1325`）の R2-1 に対応 + 未レビューの技術レポート R6–R8/R10 の Round-1 自己レビューを実施。

## A. Cowork R2-1 対応 ✅
- `results/production/theme_I_exciton_MP_DFPT/2026-05-24_118b3ce/README.md` に **Correction note** を追記:
  MANIFEST `notes` 内の "experiment ~15-20 meV" は旧記述 → 正しくは 7.4–50 meV (Cho 2019)。
  MANIFEST 本体は実行時 snapshot として不変、README で後追い訂正（Cowork 推奨案 b）。git_dirty 回避。

## B. R6–R8 / R10 技術レポート Round-1 自己レビュー（新規指摘・修正済）
| ファイル | 指摘 | 対応 |
|---|---|---|
| theme_A_g_factor.md | ★ **「163 テスト通過」が stale**（現 231） | 「231 テスト通過（執筆時点）」+ Kashikar「13 軌道 active basis（4 軌道 minimal も提案）」 |
| theme_A5_optical.md | 「実験 ~5-6」記憶ベース実験値 | 「実験報告値 ~5-6（要原典確認, in-repo 外）」 |
| theme_A5_optical.md | Apergi 2023 文脈（CD 論文） | 「円二色性 TB の速度行列要素 ε(ω) Eq.3/4」+ 一般 Kubo-Greenwood は Kubo1957/Greenwood1958 と明記（PI 版 P1 と整合） |
| theme_I_publication_outline.md | Yang2017/Tanaka2003/Blount1962 metadata, Kirstein 年, Kashikar 命名 | 「in-repo 外, 要原典確認」flag、Kirstein→arXiv:2112.15384、Kashikar「13 軌道 active basis」 |
| theme_F_shift_current.md | Blount 1962 | §5/参照とも in-repo 外（narrative 形, 既に honest 限界記述）。全レポートで Blount は in-repo 外と統一認識 |

## C. Round 2 自己レビュー（R1–R5 + theme_I_exciton, Round-1 修正後）
- 再 grep: "~15–20"/"Nature 暦"/"163" 残存ゼロ。数値は MANIFEST 一致継続。**新規指摘なし**。

## D. カウンタ
- Round 2 は Cowork R2-1（1件）+ 本ラウンドで R6–R8/R10 に新規指摘 → **連続 0 未達**（リセット継続）。
- 次: Cowork が R6–R10 を含めて Round 3 独立レビュー → 双方ゼロが 3 連続で合格。

## E. Round 2+ への申し送り（PDF 収集, Cowork §2/§5）
- Yang 2017 (PRB 96 035301) の arXiv 版 / Tanaka 2003 の二次引用（Quan 2019 等）を WebSearch で収集すると in-repo 外 4 件が解消に向かう。優先: Yang・Tanaka 高、Blount・Roth 中低（教科書代替可）。
- 必要なら私が WebSearch で当たります（PI 許可済の web research 方針に沿う）。
