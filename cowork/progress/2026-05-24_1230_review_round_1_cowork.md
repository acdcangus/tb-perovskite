# ラウンド 1 supervisor (Cowork) レビュー — PI_explained 4 本 + overview — 2026-05-24 12:30 JST

**発行元:** Cowork (supervisor)
**プロトコル:** `cowork/progress/2026-05-24_1200_PI_review_protocol_standing_rule.md` 準拠
**ラウンド:** 1 / 連続 0 指摘必要数 3
**対象:** R1 (overview) + R2-R5 (PI_explained_theme_A/F/phase_1.5/I)
**照合実施:**
- PDFs: `arxiv_2101.08562` (Kashikar), `arxiv_2112.15384` (Kirstein), `arxiv_2305.10586` (Nestoklon 2023), `arxiv_2309.14002` (Apergi), `arxiv_1701.00172` (Fregoso), `arxiv_1202.3168` (Young-Rappe), `arxiv_1908.09436` (Cho)
- MANIFEST: 4 bundles × `key_numbers`

---

## 全体所見

- **数値の MANIFEST 一致**: PI_explained 4 本とも、表中の主要数値はほぼ完全一致（丸めの範囲内）。捏造はゼロ。
- **PDF 確認できた式・パラメータ**: Kirstein 2022 Eq.5/6 のパラメータ（Δ=1.5 eV, ~p/m0=6.8 eVÅ, Δg_e=-1）と Fregoso 2017 Eq.C2 の "w 項" は PDF で確認できた。
- **PDF が無い文献の引用**: Roth-Lax 1959, Blount 1962, Yang 2017, Tanaka 2003 は `references/pdfs/` に無く、本ラウンドでは現物照合できなかった（要追加収集 or 二次文献に切替）。
- **整合性**: overview の Theme A 説明と PI_explained_theme_A 本文の間に物理的記述の整合性問題（後述 O2）。
- **「Kashikar-13」命名問題**: Kashikar 2021 PDF abstract は **4-orbital minimal SK-TB model** を提唱（13 orbital は active basis）。報告書での "Kashikar-13" 表現は実装と原典の対応関係を明示する必要あり。

→ **指摘総数: 17 件**（A: 5、F: 4、Phase1.5: 3、I: 3、overview: 2）。詳細は §1-5。

---

## §1. PI_explained_theme_A.md 指摘 (5 件)

### A1 ★ Kirstein 2022 の発表誌 — 「Nature 暦」表記の誤り＋誌名再確認
- **箇所:** L133 `E. Kirstein et al. 2022, *Nature* 暦 / k·p 普遍関係（g_e, g_h の普遍式 Eq.5/6, P=6.8 eV·Å, Δ=1.5 eV）`
- **問題:**
  - 「Nature 暦」は「Nature 誌」の OCR/typo らしい
  - Kirstein 2021 (arXiv:2112.15384) の論文の被引用文献は `Nat. Commun.` が中心。出版誌は **`Nat. Commun.` 13 (2022)** の可能性が高い（DOI 確認必要）
  - また MANIFEST は "Kirstein 2021 arXiv:2112.15384" と記載しており、年号も 2021 vs 2022 で揺れている
- **PDF 検証:** arXiv version 2112.15384v1 dated 31 Dec 2021。本文中の `(Dated: January 3, 2022)`。
- **修正方針:**
  - 「Nature 暦」→ 出版誌の正式名（要 DOI 確認: `10.1038/s41467-022-...` ならば `Nat. Commun.`、Nature 本体ならば `Nature`）
  - 年号は arXiv preprint 2021 / journal 2022 を併記推奨: 「Kirstein et al. *Nat. Commun.* 13, ... (2022); arXiv:2112.15384 (2021)」
- **照合済 PDF 内容:** Eq.5/Eq.6 に該当する k·p 式中で `Δ=1.5 eV, ~p/m0=6.8 eVÅ, Δg_e=−1` を確認 ✓

### A2 ★ 「Kashikar-13」命名と Kashikar 2021 paper の実体の不一致
- **箇所:** L52 `Kashikar-13 軌道 TB パラメータ`
- **問題:** Kashikar 2021 paper (arXiv:2101.08562) abstract は
  > "while thirteen orbitals are active in constructing the valence and conduction band spectrum, here we establish that a **four orbital based minimal basis set is sufficient** to build the Slater-Koster tight-binding model (SK-TB)"
  → 元論文の提案モデルは **4-orbital SK-TB**。13 は "active" な軌道数だが minimal basis ではない。
- **修正方針:**
  - 実装が実際 13-orbital なら「13 軌道（Kashikar 2021 の active basis を採用）」と明示
  - 実装が 4-orbital なら「Kashikar 2021 SK-TB（4 軌道 minimal basis）」に修正
  - **コード側 `src/perovskite_tb/` の TB Hamiltonian 構築箇所**を確認して命名を確定すること
- **影響:** R1 overview L79 にも同種記述あり（O1 参照）

### A3 数値表の出所が MANIFEST `key_numbers` に全部は無い
- **箇所:** L78-86 の 9 材料表 + L4 のヘッダ「数値はすべて MANIFEST `key_numbers` から引用」
- **問題:** `key_numbers` には 9 項目のみ収録（CsPbI3/Br/Cl/SnI3/GeI3 の g_e と CsGeI3/SnI3 の gh_deviation, TB_P_nestoklon, P_universal）。9 材料全部の Eg, SOC Δ, g_e, g_h, gh_deviation はカバーしていない。
- **修正方針:**
  - ヘッダを「主要数値は MANIFEST `key_numbers`、9 材料の全表は bundle 内 `outputs/g_factors_9materials.csv` から引用」と明確化
  - もしくは MANIFEST `key_numbers` に 9 材料全数値を追加する（next bundle ver で）
- **影響:** F, Phase 1.5, I も同じパターン要確認

### A4 Roth-Lax-Zwerdling 1959 / Blount 1962 が PDF library 未収
- **箇所:** L135, L136
- **問題:** `references/pdfs/` に Roth-Lax-Zwerdling 1959 PR 114, 90 と Blount 1962 PR 126, 1636 は無い。本ラウンドで現物照合できなかった。
- **修正方針（いずれか）:**
  - (a) PDF を追加収集（Phys. Rev. 1959/1962 は paywall 越え必要、APS 公式から DOI 経由で OA かどうか要確認）
  - (b) これらを直接引用する代わりに、二次文献（教科書 Yu & Cardona; Vurgaftman 2001 review 等）で参照
- **推奨:** (b) — 1959/1962 PR を二次引用に格下げし、現代のレビューを一次引用にする

### A5 Nestoklon 2023 の役割記述が曖昧
- **箇所:** L134 `M. O. Nestoklon et al. 2023(TB から g 因子確認)`
- **問題:** Nestoklon 2023 (arXiv:2305.10586) は PDF abstract に明記の通り **CsPbX₃ ナノ結晶**の量子閉じ込め下での g 因子拡張（empirical tight-binding + k·p）。「TB から g 因子確認」は曖昧かつ範囲拡大解釈。
- **修正方針:** 「Nestoklon 2023: CsPbX₃ ナノ結晶での ETB+k·p による g 因子普遍関係の量子閉じ込め下での拡張」など正確に。

---

## §2. PI_explained_theme_F.md 指摘 (4 件)

### F1 CsSnI₃ gap 数値の丸め誤差
- **箇所:** L68 `CsSnI₃ ... gap (eV) 0.18`
- **MANIFEST 値:** `CsSnI3_gap_at_R_eV: 0.17458`
- **問題:** 報告書は 0.18 だが 0.17458 → 0.17 が正しい丸め（四捨五入）。
- **修正方針:** 0.18 → 0.17 に訂正

### F2 結果表のレイアウト不整合
- **箇所:** L66-73
- **問題:** 1-5 位は「材料 / σ_zzz / gap」が縦に揃うが、6-9 位は 1 行に圧縮されており gap が欠落
- **修正方針:** 9 材料すべて統一形式（行ごとに材料 / σ / gap を列）

### F3 Blount 1962 (PDF 未収) と他文献の混同
- **箇所:** L99-100 `Blount 1962: 位置演算子の原子内成分欠落で振幅過小`
- **問題:** A4 と同じ。PDF 未収のため現物照合不可。
- **修正方針:** A4 と統一対応

### F4 「Tan & Rappe 2016 の対称則」記述の典拠未明確
- **箇所:** L89 `δ→−δ で符号反転（Tan & Rappe 2016 の対称則と一致）`
- **問題:** Tan & Rappe 2016 (npj Comput. Mater. 2:16026) は PDF library 未収。この対称則の出典箇所（Eq. number 等）が不明。
- **修正方針:** PDF を追加収集 or 対称則の出典セクション（例: §IIB Eq.X）を明示

---

## §3. PI_explained_phase_1.5_optical.md 指摘 (3 件)

### P1 Apergi 2023 (arXiv:2309.14002) の文脈ずれ
- **箇所:** L97 `M. Apergi et al. 2023（Kubo-Greenwood TB 光学応答の式）`
- **問題:** Apergi 2023 PDF タイトル: "Calculating the **Circular Dichroism** of Chiral Halide Perovskites: A Tight-Binding Approach"。本研究の Phase 1.5 は CD ではなく**通常の ε(ω)**（吸収）。Apergi 2023 は CD 専用論文であり、Kubo-Greenwood 一般式の出典ではない。
- **修正方針:**
  - 「Apergi 2023」を「**TB の速度行列要素を用いた光学応答の実装例**」と限定的に位置付け、本研究で参照したのは Apergi の Eq.3,4（MANIFEST 記載）の具体形であることを明示
  - Kubo-Greenwood 一般式は Kubo 1957 / Greenwood 1958（または Yu-Cardona 教科書）を別に引用

### P2 f-sum 比 0.21 の物理的解釈の出典不明
- **箇所:** L70-74 `本計算では 0.21（理想の 1 の約 1/5）。これは TB の速度演算子が原子内成分を欠く（Blount 1962）ため`
- **問題:** Blount 1962 PDF 未収。f-sum が 1 未満になる物理的根拠の現物照合不可。
- **修正方針:** A4 と同じ対応 + Apergi 2023 PDF か別のレビューで f-sum 議論を確認

### P3 ε(∞)（高周波誘電率）の Theme I との接続が不正確
- **箇所:** L16 `ε(∞)（高周波誘電率）は励起子（Theme I）の遮蔽計算に使う基礎データ`
- **問題:** Theme I で実際使ったのは Phase 1.5 の ε(∞) ではなく **Materials Project DFPT ε_∞**（独立データ）。Phase 1.5 の ε(∞) は使われていない。
- **修正方針:** 「将来 Theme I で利用検討（実際は MP DFPT を採用）」など正確化

---

## §4. PI_explained_theme_I.md 指摘 (3 件)

### I1 E_b 表に 8 材料中 6 材料しか記載されていない
- **箇所:** L70-77
- **問題:** MANIFEST `materials_included` は 8 材料（CsPbI/Br/Cl, CsSnI/Br, CsGeI/Br/Cl）だが、表に **CsSnBr₃ (E_b=11.6) と CsGeBr₃ (E_b=19.0) が欠落**。報告書本文では「8 材料マップ」と記載しているのに表は 6 材料。
- **修正方針:** 表に CsSnBr₃ と CsGeBr₃ の行を追加（MANIFEST 値: 11.6, 19.0 meV）。

### I2 ★ Cho 2019 の引用が因果誤り — ε=6.1 で 22 meV ≠ Cho 自身の値
- **箇所:** L85 `校正点 CsPbI₃: 実効 ε≈6.1（励起子論文 Cho 2019）なら E_b=22 meV（実験 ~15–20 と一致）`
- **PDF 検証:**
  > Cho 2019 (arXiv:1908.09436): "Using µ = 0.10m0 (consistent with the band masses reported above) and **ε = 6.1, we find Eb1s = 37 meV**. This is in reasonable agreement with experimental values, which range from **7.4 to 50 meV**."
- **問題:**
  - Cho 2019 自身は **ε=6.1 + μ=0.10 で E_b=37 meV** と報告。
  - 本研究の「22 meV」は **Cho の ε=6.1 を借用 + 本研究の μ=0.0592** で得た値（μ が異なるため答えも異なる）。
  - また Cho 2019 の実験範囲は **7.4–50 meV**。報告書の「実験 ~15–20」はどこから？
- **修正方針:**
  - 「Cho 2019 の ε=6.1 を採用、本研究 μ=0.0592 と組合せて E_b=22 meV」と明示（Cho 自身の 37 meV は別計算と区別）
  - 「実験 ~15–20 meV」の出典を明記 or 「7.4–50 meV（Cho 2019 Ref.29,41,53–57 系列）」に置換
  - また Cho 2019 の `ε = 6.1` は本文中で **層状（2D RP）系の「inorganic layer dielectric constant ε_i」** として登場している。bulk CsPbI₃ への直接転用の正当性も要検証

### I3 Yang 2017 PRB 96 035301 と Tanaka 2003 SSC 127 619 が PDF library 未収
- **箇所:** L114-115
- **問題:** `references/pdfs/` に無く、本ラウンドで現物照合不可。
- **修正方針:** A4 と同じ（PDF 追加収集 or 二次文献に置換）。Yang 2017 は arXiv 版が存在する可能性あり (arXiv:1706.... 等)。

---

## §5. PI_explained_overview.md 指摘 (2 件)

### O1 Kashikar 2021（13 軌道）表記
- **箇所:** L79 `既に検証されたパラメータセットがある: Kashikar 2021（13 軌道）、Nestoklon 2020（sp³d⁵s\* 軌道）`
- **問題:** A2 と同じ。Kashikar 2021 paper の SK-TB model は 4-orbital minimal basis。
- **修正方針:** A2 と同じ統一対応

### O2 ★ Theme A 説明の物理的記述が theme_A 本文と矛盾
- **箇所:**
  - overview L118: `9 材料すべての電子 g 因子（g_e）が、バンドギャップ Eg の単一普遍曲線上に乗る`
  - PI_explained_theme_A L93: `電子 g_e は「見かけの普遍性」`
- **問題:** overview は「電子 g_e は全 9 材料で普遍曲線」と無条件に言うが、theme_A 本文は「見かけの普遍性」と限定的（k·p 式が SOC Δ 依存を内包しているという含意）。両者で読者の理解が食い違う。
- **修正方針:** overview に theme_A と同じ honest 記述（「全 9 材料で k·p 普遍曲線にほぼ載るが、Δ 依存を含む見かけの普遍性」）を反映

### O3（追加・要 PDF）「実験 ~64 meV」（CsPbCl₃ E_b）の出典
- **箇所:** L164 `CsPbCl₃ で bare ε_∞=2.4 を使うと E_b=273 meV（実験 64 meV の 4 倍過大）`
- **問題:** 実験 E_b=64 meV と bare ε_∞=2.4 の出典が overview 本文に無い（Tanaka 2003 と推測）。
- **修正方針:** 出典を脚注で明示

---

## §6. 文献追加収集の推奨リスト（Round 2 開始前）

以下を `references/pdfs/` に追加収集すると Round 2 で物理引用照合が大きく進む:

| 文献 | DOI | 入手難易度 | 用途 |
|---|---|---|---|
| Roth, Lax, Zwerdling 1959 Phys. Rev. 114, 90 | 10.1103/PhysRev.114.90 | APS paywall（要 OA 確認）| Theme A g 因子原典 |
| Blount 1962 Phys. Rev. 126, 1636 | 10.1103/PhysRev.126.1636 | APS paywall | TB 限界・f-sum 議論 |
| Tan, Zheng, Young, Wang, Liu, Rappe 2016 npj Comput. Mater. 2:16026 | 10.1038/npjcompumats.2016.26 | OA (Nature) | shift current 対称則 |
| Kirstein 2022 Nat. Commun. journal version | 10.1038/s41467-022-... | OA (Nat. Commun.) | g 因子 publication 版 |
| Yang 2017 PRB 96, 035301 | 10.1103/PhysRevB.96.035301 | APS paywall（arXiv 版あり？要検索）| Wannier-Mott |
| Tanaka 2003 Solid State Commun. 127, 619 | 10.1016/S0038-1098(03)00566-0 | Elsevier paywall | CsPbX₃ exciton 実験 |
| Boyer-Richard 2016 | （要 arXiv ID 確認） | | overview L173 |

---

## §7. 次アクション

### Claude Code 担当（Round 1 finishing）

1. 本指摘 17 件に対して **Round 1 Claude Code 自己レビュー**を独立に実施
2. 重複指摘と新規指摘をマージして修正 commit
3. commit message: `review round 1 (claude code + cowork): NN findings addressed across PI_explained × 4 + overview`
4. 必要なら追加 PDF 収集を別 commit で

### Cowork 担当（Round 2）

1. Claude Code 修正 commit 後、再度 PI_explained 4 本 + overview を独立にレビュー
2. 新 commit に残存する問題と新たに発見した問題を `cowork/progress/YYYY-MM-DD_HHMM_review_round_2_cowork.md` で記録
3. **指摘ゼロにならない限りラウンドカウンタは 0 にリセット**

### 連続 0 指摘 3 ラウンド合格条件

- 連続 3 ラウンドで **Claude Code 側 0 + Cowork 側 0** の場合に R1-R5 を "clean" とマーク
- 1 件でも出ればカウンタリセット

---

## §8. Round 1 完了の宣言

- Cowork supervisor のラウンド 1 レビューは **本ファイル commit をもって完了**
- Claude Code のラウンド 1 自己レビュー結果待ち
- 並行して **R6-R10 (technical reports `theme_*.md` × 5) のラウンド 1 レビュー**は次 patrol サイクル以降で開始予定（緊急性なし）
- MANIFEST 数値の追加 audit はラウンド 2 と並行
