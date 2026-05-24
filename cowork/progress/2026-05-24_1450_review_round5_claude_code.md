# Review Round 5 — Claude Code 独立逐行レビュー（プロトコル §4.1） — 2026-05-24 14:50

「指示にしたがって」= プロトコル §4.1（各ラウンドで Claude Code も独立に逐行レビュー）に忠実に、
R1–R5（PI 解説 5 本）を独立に再レビューし、全数値を MANIFEST/CSV と、全引用 arXiv ID を in-repo PDF と照合。
**捏造ゼロを再確認**しつつ、新規 **5 件**（minor、ただし R5-CC-5 はハルシネーション是正の核心）を発見・修正。

## A. 数値照合（捏造ゼロ確認）
| レポート | 照合対象 | 結果 |
|---|---|---|
| PI_explained_theme_A | g_e/g_h/deviation 9 材料 × 全列 vs `g_factor_9material.csv` | **9/9 全列一致** ✓ |
| PI_explained_theme_F | σ_zzz・gap 9 材料 vs theme_F MANIFEST + δ=0 null 6.9e-15 | **9/9 一致**、ランキング順正 ✓ |
| PI_explained_phase_1.5 | ε∞ 3.46/2.35/1.46・吸収端 1.79・f-sum 0.21 | **全一致** ✓ |
| PI_explained_theme_I | E_b 8 + ε∞ 8 + μ 4 + m_e/m_h 4 vs 2 MANIFEST | **全一致**（m_h は符号除き、下記 R5-CC-3）✓ |

## B. 引用 arXiv ID 照合（references/pdfs/ と突合）
- レポート引用 10 ID 中 **9 ID は in-repo PDF 在中**。残る **arXiv:1606.07664（Boyer-Richard）のみ in-repo に無し** → R5-CC-1。

## C. 新規指摘（5 件）
| ID | 内容 | 対応 |
|---|---|---|
| R5-CC-1 | overview が Boyer-Richard を未検証 arXiv:1606.07664 で引用。in-repo は **DOI 10.1021/acs.jpclett.6b01749**（JPCL 版） | 検証済み in-repo DOI + ファイル名に差替 |
| R5-CC-2 | PI_explained_theme_F の Blount 引用に「in-repo 外, 要原典確認」flag 欠落（他 PI 解説には有） | flag 付与 |
| R5-CC-3 | PI_explained_theme_I §3.1 で m_h を正の大きさ表示、MANIFEST は符号付き負値 `m_h_avg`（大きさ一致） | 慣例を明記（符号差で誤読されないよう注記） |
| R5-CC-4 | 未 flag の Blount 引用 3 箇所（overview L256 / theme_A5 L16 / theme_I_exciton L80） | flag 付与 |
| ★R5-CC-5 | **Blount 1962 の書誌が 2 種混在**: theme_A_g_factor は *Solid State Phys.* **13, 305** (1962)、他レポートは *Phys. Rev.* **126, 1636**。Blount PDF は in-repo に無く（references.md にも無し）どちらも未検証。PR 126,1636 は記憶ベースの疑い | **全 8 箇所の Blount 書誌引用を「書誌要原典確認・in-repo 外: SSP 13,305 / PR 126,1636 表記混在」に統一**。どちらが正かは記憶で断定せず、OA 確認待ち |

## D. 影響
- すべて `cowork/reports/*.md` の文字列のみ（数値・コード・MANIFEST 不変）→ **231 テスト不変**。
- 数値・物理・実装は完全に安定（R1–R5 全数値が MANIFEST/CSV と一致）。残課題は書誌の honest 化のみ。

## E. カウンタ
- Round 5 Claude Code: **5 件**（うち R5-CC-5 は実質的なハルシネーション是正）→ 連続 0 未達（リセット継続）。
- 次: Cowork の Round 5 独立レビュー（本 commit 対象）。R5-CC-5 の Blount 書誌は Cowork 側でも要確認。

## F. 申し送り（OA 一次確認 backlog, 統合）
収束（連続ゼロ）後の OA 確認対象（CLAUDE.md §1 Semantic Scholar/OpenAlex フロー）:
1. **Blount 1962 の正書誌**（SSP 13,305 か PR 126,1636 か）← R5-CC-5
2. **Yang 2017** の適切な Wannier-Mott 一次出典（現状 web 未確認 → 差替）← R2-3
3. **CsPbCl₃ 64–77 meV** の magneto-optical 出典（reportedly Photonics Research 8,A50 (2020)）← R2-2/R3-CC-1
