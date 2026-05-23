# Directive 補足 — ε_∞ fallback は Cowork が Chrome で検索

**発行元:** Cowork supervisor（PI 起床判断 (v) を受領）
**発行時刻:** 2026-05-24 07:35 JST (22:35 UTC, 5/23)
**親 directive:** `2026-05-24_0715_directive_theme_I_hybrid_and_license.md` §1 Task Y1-c-1
**スコープ:** Y1-c-1（ε_∞ 文献抽出）で `references/texts/*.txt` から見つからない材料が出た場合の fallback 方針を確定。

---

## 確定事項

PI から本セッションで以下の判断を受領:

> 「ε_∞ 抽出で見つからない材料が出た場合 cowork が chrome 使って検索してください」

→ **見つからない材料は Cowork が Claude in Chrome で外部検索して補完**します。Claude Code は手を止めず、見つからない材料リストだけ Cowork に渡してください。

## Claude Code 側のワークフロー変更

親 directive Y1-c-1 §5 を以下で **上書き**:

### 旧（親 directive）
> 5. 9 材料すべて見つかれば理想。**見つからない材料があれば**:
>    - `eps_inf: null, status: "not_found_in_references", searched: [arxiv_id list]` で明記
>    - その材料は Y1-c-3 の E_b production 対象から外す（部分 production OK）
>    - PI に報告（progress notification）し、後で PI 入力 or DFT-RPA database 引きで補完判断

### 新（本補足）
> 5. 9 材料すべて見つかれば理想。**見つからない材料があれば**:
>    - `data/parameters/eps_inf_external.json` の該当材料を `"eps_inf": null, "status": "pending_cowork_chrome_search", "searched_refs": [arxiv_id list], "search_keywords_used": [...]` で **暫定マーキング**
>    - **そこで Y1-c-3 / Y1-d は止めず、見つかった材料だけ先に E_b production scan を実行**（部分 production OK）
>    - 不足材料リストを **`cowork/progress/<YYYY-MM-DD>_<HHMM>_eps_inf_missing_request.md`** に以下のフォーマットで書いて Cowork に依頼:
>
>      ```markdown
>      # ε_∞ 補完依頼 — <date> <time>
>      
>      Y1-c-1 で `references/texts/` から ε_∞ が見つからなかった材料:
>      
>      | 材料 | phase | 探した keywords | 探した arxiv_ids | 備考（バンドギャップ域・既知の難点等） |
>      |---|---|---|---|---|
>      | CsSnCl3 | cubic | ε_∞, eps_inf, high-frequency dielectric, optical dielectric | arxiv_2104.01738, arxiv_2412.07016, ... | Sn は文献少なめ、wide-gap側 |
>      | ...     | ...   | ...                                                   | ...                                    | ...                       |
>      
>      Cowork は Claude in Chrome で以下のソース順に検索してほしい:
>      1. Materials Project (https://materialsproject.org)
>      2. NoMaD (https://nomad-lab.eu)
>      3. Google Scholar（実験値優先）
>      4. arXiv 検索（既収集外の論文）
>      
>      出典は必ず明記して `data/parameters/eps_inf_external.json` に追記してください。
>      ```
>
>    - Cowork が補完した値を `data/parameters/eps_inf_external.json` に追記してきたら、Claude Code は次の polling cycle で検出 → 該当材料を含めて Y1-c-3 を **再 run**（追加 bundle として、または既存 bundle を `_v2/` として）。

## Cowork 側で実施する補完手順（参考、Cowork 自身向けメモ）

依頼ファイル `*_eps_inf_missing_request.md` を patrol で検出したら:

1. `mcp__Claude_in_Chrome__navigate` で Materials Project の material search ページを開く
2. 材料 ID（mp-XXXX）を特定 → dielectric tensor の eps_inf 値を取得
3. Materials Project に無ければ NoMaD → Google Scholar → arXiv の順で fallback
4. **必ず出典（URL or DOI or arXiv ID + 式番号 or 表番号）を併記**してから `data/parameters/eps_inf_external.json` を直接 edit
5. 完了通知 `cowork/progress/<YYYY-MM-DD>_<HHMM>_eps_inf_search_complete.md` を書く（PI が再現できる出典リスト付き）
6. ハルシネーション防止: URL が開けない / 値が抽出できない場合は「未取得」と明示し、捏造しない

## なぜ Cowork 側でやるか（PI 判断の合理性）

- Cowork は Chrome MCP（`mcp__Claude_in_Chrome__*`）と WebSearch が使える → Materials Project / NoMaD などのインタラクティブなデータベース UI に強い
- Claude Code は repo 内ローカル作業が主タスク → 外部 web 検索でセッションを長引かせない方が良い
- 役割分担: **Claude Code = repo 内の計算/コード、Cowork = repo 外の文献/web 検索 + 監督**

## 親 directive §6 への追記

親 directive `0715` §6「残る PI 判断」の (v) は本補足で確定 → 残 PI 判断は (i)（`claude --continue` 動作検証）のみ。

## 完了通知パターン

| イベント | ファイル名 |
|---|---|
| Claude Code が不足材料リストを Cowork に渡す | `<HHMM>_eps_inf_missing_request.md` |
| Cowork が Chrome 検索完了 + json 更新 | `<HHMM>_eps_inf_search_complete.md` |
| Claude Code が補完値で Y1-c-3 再 run | `<HHMM>_Y1c3_binding_energy_production_v2.md` |

---

**本補足で Y1-c-1 の fallback フローが PI 不在でも自走可能になりました**（Claude Code が見つからないものを書き出す → Cowork patrol が拾って Chrome で補完 → Claude Code が次サイクルで再 run）。Claude Code はそのまま親 directive の優先順序 Y2 → Y1-a → Y1-c-1 → ... で進めてください。
