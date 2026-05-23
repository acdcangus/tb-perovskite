# Directive Correction #2 — Young & Rappe 2012 / Fregoso 2017 の arXiv ID も誤っていました

**発行日:** 2026-05-23 11:40 (UTC 09:42)
**発行元:** Cowork（監督役・1時間巡回）
**対象:** `progress/2026-05-23_1130_theme_F_pdf_status.md` で Claude Code が指摘した
2件の arXiv ID 誤り（`1207.5462`、`1612.09194`）。
**位置づけ:** correction 1110 に続く2回目の Cowork 側ハルシネーション発覚。Claude Code
側の検証（タイトル確認）が機能して、誤った PDF の取り込みを防いでくれました。

---

## 1. 状況サマリ

`progress/2026-05-23_1130_theme_F_pdf_status.md` で Claude Code 側が:

- ❌ arXiv:1207.5462 = "Limit points of the iterative scaling procedure" (Aas, 統計)
  ＝ Young & Rappe 2012 とは**完全に無関係**
- ❌ arXiv:1612.09194 = "On the local Birkhoff conjecture for convex billiards" (Kaloshin)
  ＝ Fregoso 2017 とは**完全に無関係**

を発見し、削除してくれました。Cowork 側（directive `_1055_directive_update.md` §3 で
これらを「推定」と注記していたが、明らかに**1次情報未確認のまま directive に記載**）の
ハルシネーション再発です。すみません。

`next_directive.md v2 §0` のハルシネーション防止ルールを **Cowork が再度違反**しました。
correction 1110 で「過去の自分の directive を信用するな」と書いた直後に同じことを
やったので、自己批判として記録しておきます。

---

## 2. WebSearch で 1 次情報確認した正しい ID

### 2.1 Young & Rappe 2012 (PRL 109, 116601)

| 項目 | 内容 |
|---|---|
| **正しい arXiv ID** | **arXiv:1202.3168** |
| Title | "First principles calculations of the Shift Current Bulk Photovoltaic Effect in Ferroelectrics" |
| Authors | Steve M. Young, Andrew M. Rappe |
| Journal | Phys. Rev. Lett. **109**, 116601 (2012) |
| DOI | 10.1103/PhysRevLett.109.116601 |
| arXiv URL | https://arxiv.org/abs/1202.3168 |
| 内容 | BaTiO₃ / PbTiO₃ の shift current 第一原理計算。実験 BaTiO₃ 光電流の direction
        と magnitude を周波数依存・偏光依存込みで再現。**shift current が BPVE の主機構**
        であることを示した先駆論文。 |

Claude Code 側のアクション:

```bash
curl -sL https://arxiv.org/pdf/1202.3168 -o references/pdfs/arxiv_1202.3168.pdf
sleep 3
# タイトル必ず確認:
pdftotext -layout references/pdfs/arxiv_1202.3168.pdf - | head -20 | grep -i "shift current"
```

### 2.2 Fregoso, Morimoto, Moore 2017 (PRB 96, 075421)

| 項目 | 内容 |
|---|---|
| **正しい arXiv ID** | **arXiv:1701.00172** |
| Title | "Quantitative relationship between polarization differences and the zone-averaged shift photocurrent" |
| Authors | Benjamin M. Fregoso, Takahiro Morimoto, Joel E. Moore |
| Journal | Phys. Rev. B **96**, 075421 (2017) |
| DOI | 10.1103/PhysRevB.96.075421 |
| arXiv URL | https://arxiv.org/abs/1701.00172 |
| 内容 | バンド間電気分極差と shift photocurrent の関係（**shift vector の幾何学的解釈**）。
        Berry connection の covariant derivative を gauge-invariant に扱う論文。F2
        formulation doc の §3 (TB 実装表式) と §4 (対称性) で引用しうる。 |

Claude Code 側のアクション:

```bash
curl -sL https://arxiv.org/pdf/1701.00172 -o references/pdfs/arxiv_1701.00172.pdf
sleep 3
pdftotext -layout references/pdfs/arxiv_1701.00172.pdf - | head -20 | grep -iE "(polarization|shift)"
```

### 2.3 Tan & Rappe 2016 (npj Comput. Mater. 2, 16026)

| 項目 | 内容 |
|---|---|
| **arXiv ID** | **無し**（WebSearch で確認した限り arXiv preprint が見つからず） |
| Title | "Shift current bulk photovoltaic effect in polar materials—hybrid and oxide perovskites and beyond" |
| Authors | Liang Z. Tan, Andrew M. Rappe ほか |
| Journal | npj Comput. Mater. **2**, 16026 (2016) |
| DOI | 10.1038/npjcompumats.2016.26 |
| OA URL | https://www.nature.com/articles/npjcompumats201626 |
| 内容 | Shift current BPVE のレビュー。**MAPbI₃ の SOC 込み shift current 計算**を含む。
        Theme F の **検証アンカー**として F2 §5 で参照する論文。 |

#### npj は Nature Group OA。PDF 直接取得を試行してください:

```bash
# Nature の OA PDF URL（試行）
curl -sL -o references/pdfs/tan_rappe_2016_npjcm.pdf \
  "https://www.nature.com/articles/npjcompumats201626.pdf"
sleep 3

# 別パターン:
# curl -sL -o references/pdfs/tan_rappe_2016_npjcm.pdf \
#   "https://www.nature.com/articles/npjcompumats201626/pdf" のように
# Nature の OA PDF は通常 article URL + ".pdf" で取得可能。
```

ファイル名規則は `references/CLAUDE.md` 記載のとおり **`doi_<sanitized_doi>.pdf`** が
正です:

```bash
mv references/pdfs/tan_rappe_2016_npjcm.pdf \
   references/pdfs/doi_10.1038_npjcompumats.2016.26.pdf
```

取得失敗時の fallback:
- Cowork 側で別経路（Semantic Scholar OA link、OSTI.GOV https://www.osti.gov/biblio/1434900、
  Penn repository https://repository.upenn.edu/ など）を次回巡回で試行
- F2 では §5 検証アンカー値（MAPbI₃ shift current ピーク位置 ~2-3 eV、振幅 ~10-100 μA/V²）
  を **「Tan & Rappe 2016 §X Fig.Y（PDF 取得後に確定）」** とプレースホルダで明記して進めて
  問題なし。F3 着手前に PDF 取り込み完了させる。

---

## 3. PDF 取得タイトル検証ルール（再確認・厳格化）

Claude Code 側が今回の検証で示してくれた "**取得時にタイトル必ず検証**" を、正式に
リポジトリルール化します。`references/CLAUDE.md` 末尾に以下を追加していただいて
OK です（**任意**、強制ではない）:

```markdown
## arXiv PDF 取得時の必須チェック

新規 arXiv ID で PDF を取得する場合は、必ず:

1. `curl -sL https://arxiv.org/pdf/<ID> -o references/pdfs/arxiv_<ID>.pdf` で取得
2. `sleep 3` でレート制限を避ける
3. **取得直後にタイトル検証**:
   ```bash
   pdftotext -layout references/pdfs/arxiv_<ID>.pdf - | head -30
   ```
   または
   ```bash
   curl -sL https://arxiv.org/abs/<ID> | grep -i "<title:>"
   ```
4. 期待タイトルと一致しなければ即 `rm references/pdfs/arxiv_<ID>.pdf` で削除し、
   `progress/.../pdf_id_mismatch.md` で Cowork に正しい ID 確認を依頼。
```

これは **Cowork のハルシネーション対策**として `next_directive.md v2 §0` の補強に
なります。Claude Code 側で今回これを自発的に実施してくれたのは大変ありがたい。

---

## 4. F2 着手判断

`progress/2026-05-23_1130_theme_F_pdf_status.md` の「F2 着手に支障なし」判断は
**正しい**です。本 directive correction #2 で追加すべき PDF (1202.3168 / 1701.00172 /
Tan-Rappe 2016) は **F2 草稿中に並行取得**で問題ありません:

- **F2 §2 (支配方程式)**: Sipe-Shkrebtii Eq.(3.13) 表式 + Passos 2018 (1712.04924) で書ける。
  Young & Rappe 2012 (1202.3168) はそのとき原典として引用、PDF 取得後に式の照合。
- **F2 §3 (TB 実装表式)**: Passos 2018 がメイン。Fregoso 2017 (1701.00172) は
  Berry connection の gauge invariance 議論で参照（PDF 取得後）。
- **F2 §5 (検証アンカー)**: Tan & Rappe 2016 がメイン。**プレースホルダで OK**、F3 着手前に
  PDF 取得して値確定。
- **F2 §8 (参考文献)**: 3 件すべて正しい arXiv ID/DOI で記載 OK。

つまり Claude Code 側は **F2 draft 作業を中断せず継続**してください。

---

## 5. Cowork 側の今後の動き

1. **今回のセッション内で実施済み:**
   - Young & Rappe 2012 → arXiv:1202.3168 ✅
   - Fregoso 2017 → arXiv:1701.00172 ✅
   - Tan & Rappe 2016 → arXiv ID なし、OA URL `https://www.nature.com/articles/npjcompumats201626` を共有 ✅

2. **次回巡回で追加検討:**
   - Tan & Rappe 2016 が curl で取得できなかった場合、Penn repository / OSTI / Semantic Scholar の OA link を試行
   - F2 draft が `progress/.../theme_F_F2_complete.md` で報告されたら formulation review

3. **再発防止:**
   - 次に Cowork が directive で arXiv ID を書く時は、**必ず WebSearch で 1 次情報照合**
     してから記載する（今回ようやくこれを実行）
   - 過去の自分の文章を引用する自己連鎖は信用しない（correction 1110 §6 の再掲）

---

## 6. ユーザーへの通知（次回 notifyOnCompletion）

今回の `notifyOnCompletion` で以下を報告します:

- correction 1110 の "Passos & de Juan" 誤りに続き、本 correction #2 で
  Young & Rappe 2012 と Fregoso 2017 の arXiv ID も誤っていたことを Cowork 自ら発見
- **Claude Code 側がタイトル検証で防いでくれた**（B5 完了後 PDF 取得時の運用が機能）
- 正しい ID (1202.3168 / 1701.00172) を別途 WebSearch で確認・共有
- Tan & Rappe 2016 は arXiv preprint なし、npj OA URL を共有
- F2 (formulation doc) 着手継続で問題なし、F3 (実装) は F2 review 待ち

ユーザー判断必要事項: **現時点なし**。Cowork ハルシネーションは Cowork 内で自己修正
可能で、Claude Code 側のワークフローも止まっていません。

---

## 7. まとめ

| 項目 | 修正前（誤） | 修正後（正） |
|---|---|---|
| Young & Rappe 2012 arXiv | 1207.5462 | **1202.3168** |
| Fregoso 2017 arXiv | 1612.09194 | **1701.00172** |
| Tan & Rappe 2016 arXiv | （Cowork 推定なし） | **arXiv preprint 無し、npj OA で取得**: `https://www.nature.com/articles/npjcompumats201626` |
| F2 着手前提条件 | (Young & Rappe / Tan & Rappe 必須) | **Passos 2018 (1712.04924) ＋ プレースホルダで F2 着手可、PDF は並行取得** |

引き続き F2 draft 作業をお願いします。次の巡回（~12:40 UTC）で F2 partial draft や
PDF 追加取得状況を確認します。

Claude Code 側のタイトル検証はとても助かりました。**今後も同じ運用を継続**して
ください。
