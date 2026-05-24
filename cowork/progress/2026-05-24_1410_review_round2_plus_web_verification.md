# Review Round 2+ — Claude Code: web 検証による引用ミス 2 件の発見・訂正 — 2026-05-24 14:10

Cowork §5「PDF 収集（並行 task）」に従い、PI 許可済の web research 方針で Yang 2017 / Tanaka 2003 を
WebSearch で当たった。その結果、**新規の引用ミス 2 件**を発見・訂正した（記憶ベース引用の是正）。

## A. 新規発見（web 検証）

### R2-2 ★ Tanaka 2003 の誤帰属（CsPbCl₃ ではなく MAPb 系）
- **検証:** WebSearch で "Tanaka 2003 SSC 127 619" は実在を確認（K. Tanaka et al., *Solid State Commun.* **127, 619–623 (2003)**; 巻号正しい）。
- **問題:** ただし対象は **CH₃NH₃PbBr₃ / CH₃NH₃PbI₃（MAPb 系）の励起子**であり、**CsPbCl₃ ではない**。
  プロジェクト内で「CsPbCl₃ の E_b≈64 meV の実験出典」として Tanaka 2003 を充てていたのは**誤帰属**。
- **正しい CsPbCl₃ 出典:** ~64–77 meV は **magneto-optical 研究（例 *Photonics Research* 8, A50 (2020)）**由来（検索で別 paper として surface）。
- **対応:** 全レポート + data で Tanaka 2003 の役割を「MAPb 系励起子（CsPbCl₃ ではない）」に訂正。CsPbCl₃ 64 meV の出典は magneto-optical 研究（要原典確認）に差替。

### R2-3 ★ Yang 2017 PRB 96, 035301 が web 未確認（記憶ベースの疑い）
- **検証:** WebSearch で当該 metadata（PRB 96, 035301, 2017）は **surface せず**。記憶ベース引用の可能性が高い。
- **対応:** 「Yang 2017 PRB 96 035301 = 記憶ベース・web 検索で未確認 → 要原典確認/差替」と全箇所で明示的に降格。

### R2-4 ★ I2「~15–20 meV」が data/parameters に 2 箇所残存（Cowork R2-1 と同根）
- Cowork は R2-1 で MANIFEST `notes` の "~15-20 meV" 取り残しを指摘済み。横断 grep で **同じ残存が `data/parameters/eps_inf_external.json` に 2 箇所**（`_KEY_FINDING` と CsPbI3 `notes`）あることを発見。
- **対応:** 両方を「7.4–50 meV (Cho 2019); Cho 自身 μ=0.10 で 37 meV; ε=6.1 は 2D 層値」に統一。CsPbCl₃ の "~64 meV" も "~64–77 meV (magneto-optical 2020; Tanaka 2003 は MAPb で別物)" に。

## B. 訂正ファイル
- `cowork/reports/PI_explained_theme_I.md`（Yang/Tanaka 参照）
- `cowork/reports/theme_I_exciton.md`（同）
- `cowork/reports/theme_I_publication_outline.md`（§6 References）
- `cowork/reports/PI_explained_overview.md`（CsPbCl₃ 64 meV 出典）
- `data/parameters/eps_inf_external.json`（`_KEY_FINDING` + CsPbCl3/CsPbI3 `notes`; **数値 eps_inf は不変、注釈文字列のみ**）

## C. 影響
- コード変更なし・数値パラメータ変更なし（注釈/参照文字列のみ）→ **231 テスト不変**。
- Production bundle の数値・provenance に影響なし。

## D. カウンタ
- Round 2 で **新規 3 件（R2-2/R2-3/R2-4）** → **連続 0 未達**（リセット継続）。
- 今回の発見は「記憶ベース引用の是正」であり、標準ルール 1200（ハルシネーション禁止・文献事実に基づく確認必須）の核心。web 検証で初めて露見した。

## E. 次
- Cowork の Round 3 独立レビュー（本 commit + R6–R10 含む）待ち。
- 未解決の in-repo 外: Blount 1962 / Roth-Lax 1959（教科書代替可, 優先低）。Yang 2017 は要差替（適切な Wannier-Mott 出典を別途特定するか、Tanaka 2003=MAPb を Wannier-Mott 実適用例として活用）。
