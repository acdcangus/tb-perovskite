# PDF/OA 一次確認 — 要原典確認 3 件を検証済み出典に置換 — 2026-05-24 15:35

PI 選択（「PDF/OA 一次確認を先に」）に従い、残る「要原典確認」backlog 3 件を PI 許可済の web research
（CLAUDE.md §1 OA フロー: Semantic Scholar / ScienceDirect / Optica / CiNii）で一次確認し、報告書の hedge を
**検証済み一次出典**に置換した。

## A. 一次確認の結果（3/3 解決）

### 1. Blount 1962 の正書誌 → **確定: SSP 13, 305**
- **"Formalisms of band theory", E. I. Blount, *Solid State Physics* **13**, 305–373 (1962)**, Academic Press（eds. Seitz & Turnbull）, **DOI 10.1016/S0081-1947(08)60459-2**。
- 確認源: Semantic Scholar, ScienceDirect (S0081194708604592), CiNii, CoLab。
- ➡️ 報告書の一部にあった **"Phys. Rev. 126, 1636" は誤り**（記憶アーティファクト）と確定。R5-CC-5 の「両表記混在」hedge を解消し、全 8 箇所を SSP 13,305 + DOI に統一（in-repo PDF は paywall のため未収だが**書誌は OA 確認済**）。

### 2. CsPbCl₃ 励起子 → **確定: Baranowski et al. 2020, E_b=64 meV**
- **Baranowski, Plochocka, Su, Legrand, Barisien, Bernardot, Xiong, Testelin, Chamarro,
  "Exciton binding energy and effective mass of CsPbCl₃: a magneto-optical study," *Photonics Research* **8**, A50 (2020)**（Optica）。**E_b = 64 meV**。
- 確認源: Optica abstract (prj-8-10-a50), researching.cn 図表ページ。
- ➡️ 「reportedly Photonics Research / WEB-SEARCH DERIVED」を **Baranowski et al. 2020（OA 確認済, 値 64 meV）** に格上げ。"~64–77 meV" は 64 meV（一次値）に統一。

### 3. Yang 2017 PRB 96, 035301 → **削除（記憶アーティファクト確定）**
- 複数の検索で **当該 metadata は surface せず**。記憶ベースの誤引用と確定。
- ➡️ 全 3 箇所（PI_explained_theme_I L118 / theme_I_exciton L77 / publication_outline L43）から **削除**し、検証済みの Wannier-Mott 実験適用例（**Baranowski 2020** + 既出の Tanaka 2003=MAPb）に置換。「〔旧 Yang 2017 は web 未確認のため削除〕」と痕跡を明記。

## B. 変更ファイル（reports + data JSON の文字列のみ）
- reports 8 本（Blount 引用統一）+ theme_I 系 3 本（Yang 削除/Baranowski 追加）+ overview（CsPbCl₃ 64 meV）。
- `data/parameters/eps_inf_external.json`: `_KEY_FINDING` + CsPbCl3 `notes` を Baranowski 2020 検証済みに（**数値 eps_inf は不変**）。
- grep 最終確認: Yang 2017 引用ゼロ（削除注記のみ）、誤書誌 PR126,1636 の断定ゼロ、WEB-SEARCH DERIVED/両表記混在ゼロ。

## C. 影響 / 残
- コード・数値・MANIFEST 不変（reports + JSON 注釈文字列のみ）→ **231 テスト不変**（最終検証 commit 03c7c1c）。JSON は有効性確認済。
- **ハルシネーション防止（standing rule 1200）の核心を強化**: 記憶ベース/web-derived の hedge を OA 検証済み一次出典に置換。残る "要原典確認" は theme_A5 の実験 ε∞~5-6（別件・honest flag 済、backlog 外）と、in-repo PDF 未収（paywall）の明示のみ。
- PDF 実体の in-repo 収集（Blount/Baranowski とも paywall; mirror はあるが provenance 留保）は任意の follow-up。書誌・値は OA 確認済なので citations は honest。
