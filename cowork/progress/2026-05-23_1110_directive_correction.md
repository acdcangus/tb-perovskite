# Directive Correction — arXiv:2207.00331 の著者・性格を誤っていました（要修正）

**発行日:** 2026-05-23 11:10 (UTC 09:10)
**発行元:** Cowork（監督役・1時間巡回）
**対象:** `2026-05-23_1055_directive_update.md`、および過去の review #2-#6 で参照した
arXiv:2207.00331 の著者・タイトル記載
**優先度:** **高** — F2 (formulation doc draft) 着手前に確認してください
**ハルシネーション防止ルール `next_directive.md v2 §0` の自己違反を発見したため自己修正**

---

## 1. 誤りの内容

`progress/2026-05-23_1055_directive_update.md` §1.1 表および §1.2 §6, §8、ならびに
過去の review #2 (`2026-05-23_0945_code_review.md`)、review #3 (`_1000_`)、review #4
(`_1025_`)、review #6 (`_1055_code_review.md`) で、私（Cowork）は以下を主張しました:

> **arXiv:2207.00331** = Passos & de Juan 2022, "Theory of nonlinear optical response",
> Sipe-Shkrebtii 代替の nonlinear optics review

これは **誤り** です。Cowork 巡回で `https://arxiv.org/abs/2207.00331` の abstract page
を直接取得して確認した結果、実際のメタデータは:

| 項目 | 真の内容 |
|---|---|
| **Title** | "Theory of nonlinear optical response" ← タイトルは合っていた |
| **Authors** | **Amin Maleki Sheikhabadi, Zahra Bagheri, Ali Sadeghi** （**Passos でも de Juan でもない**） |
| **Year / Submission** | 2022年7月1日 v1 |
| **Subject** | cond-mat.mes-hall |
| **内容** | 弱乱雑性結晶での 2nd-order optical response を density-matrix + Born 近似で扱う一般論。**TB nonlinear optics の review ではなく、disorder 入り 2nd-order response の formalism 論文**。Rashba model への適用例あり。Sipe-Shkrebtii とは direct な代替関係にない（似た系統だが別 formalism）。 |

つまり:
- (a) **著者を完全に間違えていた**（Passos & de Juan ではない）
- (b) **「review」ではなく formalism 論文**
- (c) **Sipe-Shkrebtii の "代替"** として直接使えるとは限らない（disorder 抜きの clean limit
  を取り出せば close だが、shift current の TB 実装公式の出典として**直接の参照論文には
  ならない**）

これは `next_directive.md v2 §0` の「論文に明示されていない数値・引用は推測しない」
ルールに対する **Cowork 側の違反** です。Claude Code 側ではなく Cowork 側のハルシネー
ション。すみません。

---

## 2. 正しい "Passos et al." 文献

WebSearch で確認した結果、Theme F (shift current / nonlinear optics) で本来引用したかった
論文は以下と思われます:

**D. J. Passos, G. B. Ventura, J. M. Viana Parente Lopes, J. M. B. Lopes dos Santos 2018**
- Title: "Nonlinear optical responses of crystalline systems: Results from a velocity gauge analysis"
- Journal: **Phys. Rev. B 97, 235446 (2018)**
- DOI: 10.1103/PhysRevB.97.235446
- arXiv: **arXiv:1712.04924**
- 内容: **TB velocity-gauge での任意次 nonlinear optical conductivity** の formalism、
  graphene を題材とした 2nd/3rd order の数値計算例。**Sipe-Shkrebtii length-gauge との
  関係も議論**。shift current 公式の **TB 実装上の符号・規約**を確認するのに最適。
- ライセンス: arXiv OA、PRB はジャーナル paywall だが arXiv preprint で式は読める。

これが本当に意図していた "Passos 文献" のはずです。"de Juan" は無関係でした（de Juan 氏は
Weyl semimetals の circular photogalvanic で著名ですが、TB shift current formalism の
主著ではない）。

---

## 3. arXiv:2207.00331 (Sheikhabadi 2022) は使えるか？

**部分的に Yes、ただし用途を限定**:

- 弱乱雑系での 2nd-order response の一般論として **disorder broadening の取り扱い**
  は引用に値する。
- Sipe-Shkrebtii 系統の clean limit との関係も論文中で触れられている（abstract 上は明示
  なし、Methods 要確認）。
- ただし **F2 formulation doc の primary reference にはせず**、補助引用にとどめてください。

---

## 4. Claude Code 側のアクション（差分指示）

### 4.1 PDF 追加取得（F1 に追加）

`references/pdfs/` に以下を追加取得してください（既存スクリプト or curl + sleep 3 秒）:

1. **arXiv:1712.04924** (Passos et al. 2018, velocity-gauge TB nonlinear optics)
   ```bash
   curl -sL https://arxiv.org/pdf/1712.04924 -o references/pdfs/arxiv_1712.04924.pdf
   sleep 3
   ```
   これが **F2 formulation doc の primary methodological reference** になります。

2. **arXiv:2207.00331** (Sheikhabadi et al. 2022, disorder-augmented 2nd-order response)
   — まだ未取得なら取得して構いません。ただし **「Passos & de Juan」ではなく
   Sheikhabadi et al. 2022** として扱ってください。F2 では補助引用。

### 4.2 F2 formulation doc 着手時の引用更新

`docs/shift-current-formulation.md` の §8 参考文献（および本文 §2-§3 の式引用元）で:

- ❌ "Passos & de Juan 2022 (arXiv:2207.00331)" → **削除**
- ✅ "Passos, Ventura, Lopes, dos Santos 2018, PRB 97, 235446 (arXiv:1712.04924)" → **追加**
- ✅ "Sheikhabadi, Bagheri, Sadeghi 2022 (arXiv:2207.00331)" → 補助引用として残す（disorder 効果議論時）

### 4.3 過去の Cowork レビュー記述の扱い

過去の review #2-#6 にも同じ誤りが残っていますが、これは履歴ファイルなので **書き換え
不要**（科学技術計算の git 履歴ルール上、過去ファイルは事実として保持）。**今後の引用
更新だけで対応**してください。

### 4.4 F2 着手前提条件の緩和

`2026-05-23_1055_directive_update.md` §1.2 の "F2 着手で文献の式が読めない場合" の
fallback ルールは、arXiv:2207.00331 を Sipe-Shkrebtii の primary 代替として頼る前提
だったので **本ルールで上書き**:

- **新 fallback**: arXiv:1712.04924 (Passos 2018) が取得できれば F2 着手十分。
- それも取得できない場合は、既存収集の arxiv_2105.11310.pdf + 文献内の Sipe-Shkrebtii
  Eq.(3.13) 引用形式から sketch、と既定どおり。

---

## 5. ユーザーへの通知

このハルシネーション発覚は次回の `notifyOnCompletion` でユーザーに伝えます。要点:

- Cowork 側が arXiv:2207.00331 を誤った著者・性格で参照していた
- F2 着手前に Cowork 自身で発見・自己修正
- 正しい文献 arXiv:1712.04924 (Passos 2018) を新 primary reference として指定
- Claude Code 側の作業は止めない（PDF 再取得 + 引用更新のみ）

---

## 6. 再発防止メモ（Cowork 自身向け）

- 文献名と arXiv ID を結びつけて記載する際、**少なくとも arXiv abstract page を 1 回は
  fetch して確認**してから directive に書く（特に新規著者の論文）
- 過去の自分の directive を引用する形で同じ誤りが連鎖していた（review #2 から review #6
  まで 5 回連続）。**履歴を信用せず、必須引用は毎回 1 次情報で再確認**

---

## 7. まとめ

| 項目 | 修正前 | 修正後 |
|---|---|---|
| Primary nonlinear-optics TB ref | arXiv:2207.00331 (Passos & de Juan 2022) | **arXiv:1712.04924 (Passos et al. 2018, PRB 97, 235446)** |
| Sub-ref (disorder 2nd-order) | — | arXiv:2207.00331 (Sheikhabadi et al. 2022) |
| F2 fallback OK? | Yes (with 2207.00331) | Yes (with 1712.04924) |
| 既存 directive `_1055_directive_update.md` | そのまま | 本ファイルで差分上書き |

F2 着手に **支障なし**。引用元の名前・ID だけ修正して進めてください。

引き続きよろしくお願いします。
