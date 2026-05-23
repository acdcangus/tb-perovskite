# Directive Update: 古典原典文献の取り込み（D:\Research\Papers\Paper から）

**発行:** Cowork, 2026-05-23 14:10
**契機:** ユーザーから「2017 年までの論文は `D:\Research\Papers\Paper` に原典が入っている、必要に応じてコピーして」との情報
**優先度:** 中（Theme A・G 論文化の引用強化に有用）

---

## 取り込んでほしい原典文献

Cowork で Glob 確認済み。以下を `references/pdfs/` にコピーしてください。Windows コマンドで OK：

```cmd
:: コピー先
set DEST=C:\Users\kteru\tb-perovskite\references\pdfs

:: Kane 1957 (k·p 原典、Theme A 必須引用)
copy "D:\Research\Papers\Paper\005Theory\Energy Bands\Kane-JPCS1-1957-1.pdf" "%DEST%\classic_Kane1957_JPCS1_part1.pdf"
copy "D:\Research\Papers\Paper\005Theory\Energy Bands\Kane-JPCS1-1957-2.pdf" "%DEST%\classic_Kane1957_JPCS1_part2.pdf"

:: Kane 1963 PR 131 (続編)
copy "D:\Research\Papers\Paper\004ProfHamaguchi\Laser\E. O. Kane, Physical Review, Vol.131, p.79 (1963).pdf" "%DEST%\classic_Kane1963_PR131.pdf"

:: Vogl 1983 (Empirical TB 原典)
copy "D:\Research\Papers\Paper\005Theory\Energy Bands\Vogl83-JPCS44.pdf" "%DEST%\classic_Vogl1983_JPCS44.pdf"

:: Luttinger k·p valence band (Theme A の補助、g_h の起源)
copy "D:\Research\Papers\Paper\005Theory\Energy Bands\Luttinger55-PR97.pdf" "%DEST%\classic_Luttinger1955_PR97.pdf"
copy "D:\Research\Papers\Paper\005Theory\Energy Bands\Luttinger56-PR102.pdf" "%DEST%\classic_Luttinger1956_PR102.pdf"

:: Wannier 1937 (Wannier function 原典、Blount 1962 問題の背景)
copy "D:\Research\Papers\Paper\005Theory\Energy Bands\Wannier37-PR52.pdf" "%DEST%\classic_Wannier1937_PR52.pdf"

:: Dresselhaus 1955 (Dresselhaus spin-orbit 原典)
copy "D:\Research\Papers\Paper\005Theory\Energy Bands\Dresselhaus55-PR98.pdf" "%DEST%\classic_Dresselhaus1955_PR98.pdf"

:: Ando 1982 RMP (2DEG レビュー、g因子の参考に)
copy "D:\Research\Papers\Paper\005Theory\Basic_Semicon\Ando82-RMP54.pdf" "%DEST%\classic_Ando1982_RMP54.pdf"

:: Hjarmarson 1980 (TB 拡張)
copy "D:\Research\Papers\Paper\005Theory\Energy Bands\Hjarmarson80-PRL.44.pdf" "%DEST%\classic_Hjarmarson1980_PRL44.pdf"

:: Bouckaert-Smoluchowski-Wigner 1936 (cubic 既約表現原典)
copy "D:\Research\Papers\Paper\005Theory\Energy Bands\Bouckaert36-PR50.pdf" "%DEST%\classic_Bouckaert1936_PR50.pdf"

:: Cardona 1966 / Cohen 1966 / Chelikowsky 1974 (empirical pseudopotential)
copy "D:\Research\Papers\Paper\005Theory\Energy Bands\Cardona66-PR142.pdf" "%DEST%\classic_Cardona1966_PR142.pdf"
copy "D:\Research\Papers\Paper\005Theory\Energy Bands\Cohen66-PR141.pdf" "%DEST%\classic_Cohen1966_PR141.pdf"
copy "D:\Research\Papers\Paper\005Theory\Energy Bands\Chelikowsky74-PRB10.pdf" "%DEST%\classic_Chelikowsky1974_PRB10.pdf"

:: Brust 1964 (band structure)
copy "D:\Research\Papers\Paper\005Theory\Energy Bands\Brust64-PR134.pdf" "%DEST%\classic_Brust1964_PR134.pdf"

:: Kohn 1955 (Wannier-Kohn)
copy "D:\Research\Papers\Paper\005Theory\Energy Bands\Kohn55-PR98.pdf" "%DEST%\classic_Kohn1955_PR98.pdf"
copy "D:\Research\Papers\Paper\005Theory\Energy Bands\Kohn55-PR97.pdf" "%DEST%\classic_Kohn1955_PR97.pdf"
```

**重要:** コピー前後に `%%EOF` 確認とサイズチェックは忘れずに（既存 CLAUDE.md ルール通り）。

---

## references.md への追記

`references/references.md` の末尾に「### 古典原典文献（D ドライブから取り込み）」セクションを作成し、以下のように追記してください：

```markdown
### 古典原典文献（D ドライブから取り込み、2026-05-23）

ユーザー所蔵の研究論文アーカイブ（D:\Research\Papers\Paper）から、Theme A・G の論文で歴史的引用に使う原典を取り込みました。

| ファイル | 著者・年 | 内容 | 関連テーマ |
|---|---|---|---|
| classic_Kane1957_JPCS1_part1.pdf, _part2.pdf | E. O. Kane, J. Phys. Chem. Solids 1, 249 (1957) | k·p 摂動論原典、Kane parameter P の定義 | Theme A |
| classic_Kane1963_PR131.pdf | E. O. Kane, Phys. Rev. 131, 79 (1963) | k·p 続編 | Theme A |
| classic_Vogl1983_JPCS44.pdf | P. Vogl et al., J. Phys. Chem. Solids 44, 365 (1983) | Empirical TB パラメータ原典 | TB手法論 |
| classic_Luttinger1955_PR97.pdf, _1956_PR102.pdf | J. M. Luttinger, Phys. Rev. 97, 869 / 102, 1030 | k·p valence band Hamiltonian、Luttinger パラメータ | Theme A |
| classic_Wannier1937_PR52.pdf | G. H. Wannier, Phys. Rev. 52, 191 (1937) | Wannier 関数原典 | TB手法論 / Blount 1962 問題背景 |
| classic_Dresselhaus1955_PR98.pdf | G. Dresselhaus, Phys. Rev. 98, 368 (1955) | Dresselhaus spin-orbit 原典 | Theme A・B 関連 |
| classic_Ando1982_RMP54.pdf | T. Ando, A. Fowler, F. Stern, Rev. Mod. Phys. 54, 437 (1982) | 2DEG 包括レビュー、g因子・有効質量 | Theme A 文献調査 |
| classic_Hjarmarson1980_PRL44.pdf | H. Hjalmarson et al., Phys. Rev. Lett. 44, 810 (1980) | TB sp3s\* 拡張原典 | TB手法論 |
| classic_Bouckaert1936_PR50.pdf | L. P. Bouckaert et al., Phys. Rev. 50, 58 (1936) | 立方結晶既約表現 | 対称性解析 |
| classic_Cardona1966_PR142.pdf | M. Cardona, F. Pollak, Phys. Rev. 142, 530 (1966) | k·p 14-band model | Theme A 高次拡張 |
| classic_Cohen1966_PR141.pdf | M. L. Cohen, T. K. Bergstresser, Phys. Rev. 141, 789 (1966) | Empirical pseudopotential | バンド構造比較 |
| classic_Chelikowsky1974_PRB10.pdf | J. R. Chelikowsky, M. L. Cohen, Phys. Rev. B 10, 5095 (1974) | Empirical pseudopotential 改良 | バンド構造比較 |
| classic_Brust1964_PR134.pdf | D. Brust, Phys. Rev. 134, A1337 (1964) | バンド構造 | バンド構造比較 |
| classic_Kohn1955_PR97.pdf, _PR98.pdf | W. Kohn, Phys. Rev. 97, 1147 / 98, 915 | Wannier-Kohn 局在化理論 | TB手法論 |
```

---

## まだ無くて必要なもの（Cowork が継続調査）

D ドライブには **2017 年以前の古典中心**で、以下は無い：

- **Aversa & Sipe 1995** PRB 52, 14636 — Theme F shift current 符号確定（task #26）
- **Sipe & Shkrebtii 2000** PRB 61, 5337 — 非線形応答
- **Young & Rappe 2012** PRL — BPVE 原典
- **Tan & Rappe 2016** npj CM — ハライド shift current
- **Boyer-Richard 2016** JPCL — perovskite Rashba TB（Theme B 競合検証用）
- **Frost 2017** PRB — Fröhlich モビリティ（Theme G 核心）
- **Roth-Lax 1959** PR 114 — g 因子原典（古いので別図書館アクセスかも）
- **Blount 1962** Solid State Phys. 13 — TB position operator 不完全性原典

これらは Cowork が引き続き web 経由 + APS OA 等で探索します（task #18, #23, #26）。

---

## 取り込み後にやること

1. 上記コピーを実行（Claude Code）
2. `%%EOF` 確認と PDF タイトル検証（既存ハルシネーション防止ルール準拠）
3. `references/references.md` 末尾に古典セクション追記
4. その後 Theme F F4（既存進行中）に戻る

---

## 物理的考察への取り込み

これらの古典を入れることで、Theme A 論文の **Methods** や **Introduction** で：

- "We follow the standard k·p framework introduced by Kane [Kane1957] ..."
- "Our empirical tight-binding parameters follow the sp3s\* parameterization of Vogl et al. [Vogl1983], extended to sp3d5s\* by ..."
- "The hole g-factor formula reduces to the Luttinger k·p result [Luttinger1956] in the appropriate limit ..."
- "The atomistic underestimation of the orbital g-factor is consistent with the incomplete tight-binding position operator discussed by Wannier [Wannier1937] and Blount (in preparation, see Roth-Lax [in preparation]) ..."

といった**重みのある引用**が書けます。Reviewer に「TB 法を浅く理解している」と思われない、文脈の深さが出ます。

がんばってください。
