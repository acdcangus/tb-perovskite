# R3-DEEP 対応 — Claude Code（Cowork PI Deep Review への応答） — 2026-05-24 15:05

PI 直々の「れびゅーおねがい」を受けた Cowork の `1435_pi_deep_review.md`（R3-DEEP-1〜6）に対応。
このファイルは未追跡で私の Round 5 commit (df2b4ca) に巻き込まれて初めて認知 → 内容を読み actionable 分を解決。

## A. Cowork PI Deep Review の重要点（受領確認）
- Cowork が Kirstein k·p（9材料×g_e/g_h=18）+ Wannier-Mott（8）+ Theme F σ_zzz（9）= **35 値を独立 Python 再計算 → 全て 1% 以内で一致**（捏造ゼロを二者独立で確認。私の Round 5 数値照合と完全に一致）。
- ただし Cowork deep review は **Boyer-Richard arXiv 誤り（R5-CC-1）と Blount 書誌不一致（R5-CC-5）を検出できず** → 私の Round 5 が補完。二者レビューの相補性が機能。
- ★ **R3-DEEP-5（運用注意）:** bash(Linux mount) は data/JSON を truncated に見せることがある（disk/git は正常）。**JSON 検証は Read tool か `git show HEAD:<path>` を使う**。本対応でも experimental_band_data.json / eps_inf_external.json の確認は `git show` 経由で実施。

## B. 対応（actionable 4 件、値は全て検証済みソース由来）

| ID | 内容 | 対応 | 値の出典 |
|---|---|---|---|
| R3-DEEP-1 | Theme F 表「gap (eV)」の定義欠落 | ヘッダを「**TB gap@R (δ=0.15) (eV)**」に + 脚注（実験 Eg・吸収端と別量, CBM-VBM 保証なし） | theme_F MANIFEST |
| R3-DEEP-6 | 「Eg/gap/吸収端」が theme 横断で 3 量混在 | overview §3.1 直後に**用語表**追加（実験 Eg 1.73 / TB 吸収端 1.79 / TB gap@R δ=0.15 0.63, CsPbI₃） | experimental_band_data.json (DOI:10.1038/s41467-022-30701-0), phase_1.5 MANIFEST, theme_F MANIFEST |
| R3-DEEP-2 | overview L164 の bare ε∞=2.4 と主結果の関係が曖昧 | 「bare ε∞ も手法で散乱（LST 2.4 [PMC12757862] / MP DFPT 3.64→119 meV）。C' は単一手法で defensibility 確保」を補足 | eps_inf_external.json source field |
| R3-DEEP-4 | PI_explained_theme_A 表に Δ±20% 不確かさ無し | 脚注追加（CsSnI₃ g_h=0.48 [0.26,0.72] ±0.23 最大, CsGeCl₃ ±0.03 最小; 主結果は幅に頑健） | g_factor_9material.csv の g_h_lo/g_h_hi |

## C. Deferred（Cowork 指示どおり）
- **R3-DEEP-3**: Theme A MANIFEST key_numbers を 9 材料フラット化 → 次 Theme A production rerun 時（本サイクル deferred、PRODUCTION_RULES 違反ではない）。
- **R3-DEEP-5**: Cowork patrol script の data 検証パスを Read/git show に移行 → Cowork 側運用ガイド更新（既に手動回避済）。

## D. 影響
- すべて `cowork/reports/*.md` の文字列のみ（数値・コード・MANIFEST 不変）→ **231 テスト不変**。
- 追加数値（1.73 / 1.79 / 0.63 / 2.4 / 3.64 / 119 / 0.48[0.26,0.72] / ±0.03）はすべて MANIFEST・CSV・data JSON（git show 経由で確認）に遡れる。

## E. カウンタ
- R3-DEEP 6 件中 4 件解決 + 2 件 deferred。これで Round 3 系統（R3-COW-1〜4 + R3-DEEP-1〜6）の actionable 分は全消化。
- 次: Cowork の Round 5 独立再レビュー（R5-CC-1〜5 + R3-DEEP 対応 + 本 commit 対象）。
