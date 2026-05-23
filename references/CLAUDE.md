# Claude Code 向け申し送り

このフォルダは「光デバイス用ペロブスカイト × タイトバインディング（TB）計算」の文献コレクションです。Cowork 側で収集まで終わっているので、Claude Code には残作業と分析をお願いしたいです。

## 現状サマリ

- **収集済み:** arXiv から 49 本（2016 年以降、`"tight binding" perovskite` 全文検索ヒット 74 件中の 2016+ 分）
- **保存場所:** `./pdfs/arxiv_<arxiv_id>.pdf`（合計 約 244 MB、すべて `%%EOF` まで完備の正常な PDF）
- **メタデータ:** `./references.md` に分類タグ付きで一覧化済み（光デバイス関連 / TB手法論 / Landé g因子・励起子 / 二次元層状 / トポロジカル・SOC / 酸化物系 の 6 カテゴリ）

過去に 3 本（2209.13267 / 2302.13773 / 2501.06503）が途中で切れて破損していたため再取得済み。現在はすべて健全な状態です。

## ユーザーの主な関心

- 光デバイス（太陽電池・LED・光検出器・非線形光学・円二色性・量子閉じ込め発光）に使えるペロブスカイト材料
- それらの電子構造を TB / Slater-Koster / DFTB / Wannier / k·p で記述する手法

## 残っている作業

### 1. arXiv 外の論文も追加で集める（最優先）

arXiv に無いオープンアクセスの主要論文を補完したい。Cowork 側で `Semantic Scholar API` を試したらレート制限に当たって失敗したので、Claude Code 側で WebFetch / WebSearch / curl を使って下記を当たってほしい。

候補ソース（オープンアクセスかつ抽出しやすい順）:

1. **Semantic Scholar API**（要 sleep）: `https://api.semanticscholar.org/graph/v1/paper/search?query=tight+binding+halide+perovskite&limit=50&fields=title,authors.name,year,openAccessPdf,externalIds,venue` で OA リンクを取得
2. **OpenAlex API**（レート制限ゆるい・OA リンク豊富）: `https://api.openalex.org/works?search=tight+binding+halide+perovskite&filter=is_oa:true,from_publication_date:2016-01-01&per_page=50`
3. **DOAJ**（OA ジャーナル）: `https://doaj.org/api/search/articles/tight%20binding%20perovskite`
4. **PubMed Central / Europe PMC**（材料科学のレビューが時々ここに OA で載る）
5. **Nature Communications / Scientific Reports / Communications Physics / NPJ Comput. Mater. / Materials Today / RSC Advances** など OA ジャーナルの個別検索

すでに arXiv で取得済みのものは重複なので、DOI または `externalIds.ArXiv` でフィルタしてください。

ダウンロード先: `./pdfs/`、ファイル名は arXiv 外なら `doi_<sanitized_doi>.pdf` または `oa_<short_id>.pdf` の規則でお願いします。

サニタイズ例: DOI `10.1038/s41467-019-10468-7` → `doi_10.1038_s41467-019-10468-7.pdf`

新しく取れたものは `references.md` に「### arXiv 外 追加分」セクションを作って追記してください。

### 2. 49 本（＋追加分）の本文分析

`references.md` の「重要論文の分類タグ」を起点に、以下の比較表を作るとユーザーに価値が高いです。

**a. TB モデル仕様の比較表**（必須）

| arXiv ID | 軌道基底 | パラメータ数 | SOC有無 | 対象材料 | パラメータ化手法 | 主な応用 |

`pdfs/arxiv_*.pdf` を `pdftotext` か Python の `pypdf` / `pdfplumber` で読んで、各論文の「Method」「Model」「Hamiltonian」セクションから抜き出してください。

**b. 材料カバレッジマップ**

ハライド系（MAPbX₃, FAPbX₃, CsPbX₃, Cs₂AgBiBr₆, 2D RP, ...）/ 酸化物系 / 窒化物系 / 二次元 / ナノ結晶 などで分類し、論文数と代表的な物性（バンドギャップ、g因子、SOC、励起子結合エネルギーなど）を表化。

**c. 計算結果の主要数値の抽出（可能なら）**

- バンドギャップ（直接 / 間接、計算値、実験値との比較）
- 有効質量（電子・正孔）
- Landé g因子
- スピン軌道分裂
- 励起子結合エネルギー

CSV か Markdown 表で `./analysis/` 配下に出力してほしいです。

**d. 手法の系譜図**

Slater-Koster 経験的 TB → DFT→Wannier → DFTB（GFN1-xTB 等）→ ML パラメータ化、の流れを論文の引用関係から再構築。Mermaid 図で `references.md` の末尾に追記してもらえると分かりやすいです。

### 3. 個別の深掘り候補（ユーザーが特に興味を持ちそうな順）

1. **2104.01738 (Vicent-Luna 2021, GFN1-xTB)** と **2412.07016 (Jiang 2024, 拡張 DFTB)** — ペロブスカイト用 DFTB の最新到達点。手法の差分と精度比較
2. **2101.08562 (Kashikar 2021, 汎用 Slater-Koster)** と **2012.14705 (Nestoklon 2020)** — 経験的 TB の枠組み比較
3. **2309.14002 (Apergi 2023, 円二色性 TB)** と **1908.09436 (Cho 2019, TB-GW-BSE)** — TB を使った光学応答計算の代表例
4. **2605.15807 / 2305.10586 / 2112.15384** — Landé g因子三部作（Nestoklon グループ）

それぞれ「使われている TB Hamiltonian の式」「フィット対象の物性」「予測精度」「実験との比較」をまとめてください。

## 推奨ワークフロー

```bash
# 1. PDF をテキスト化（一括）
mkdir -p texts
for f in pdfs/arxiv_*.pdf; do
  base=$(basename "$f" .pdf)
  pdftotext -layout "$f" "texts/${base}.txt"
done

# 2. 全文検索で軌道基底パターンを抽出（例）
grep -l "sp3d5s\*\|sp3s\*\|Slater-Koster\|Wannier" texts/*.txt

# 3. 分析結果を analysis/ 配下に出力
mkdir -p analysis
# tb_models_comparison.md, materials_coverage.csv, methodology_genealogy.md など
```

## 注意事項

- 大量に curl する場合は **必ず sleep を挟む**（arXiv は 1 秒以上、Semantic Scholar は 3 秒以上）。Cowork 側ではこれを怠ってレート制限に何度か当たりました
- ダウンロードした PDF は **必ず末尾の `%%EOF` を確認**してください。サイズが切りのいい数字（9MB、10.5MB など）の場合は切り捨てを疑う
- 重複チェックは DOI または arXiv ID で。タイトル一致だけだとプレプリント版とジャーナル版を別物扱いするミスが起きます
- 解析結果は `./analysis/` ディレクトリを作って分けて置いてください。`references.md` 直下に CSV を混ぜると見通しが悪くなります

## このドキュメントの場所

`C:\Users\kteru\tb-perovskite\references\CLAUDE.md`

進めていって何か判断に迷ったら、ユーザーに確認してから進めてください。よろしくお願いします。
