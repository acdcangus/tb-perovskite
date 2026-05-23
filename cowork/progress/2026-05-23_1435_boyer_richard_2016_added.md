# Boyer-Richard 2016 PDF 取り込み完了

**発行:** Cowork, 2026-05-23 14:35
**契機:** ユーザーが HAL Archive 版（OA）PDF を直接アップロード

---

## 取り込み詳細

- **ファイル:** `references/pdfs/doi_10.1021_acs.jpclett.6b01749_BoyerRichard2016.pdf`
- **サイズ:** 884 KB（%%EOF OK、PDF 1.5）
- **正式書誌:** Boyer-Richard, Katan, Traoré, Scholz, Jancu, Even, *J. Phys. Chem. Lett.* **7**, 3833 (2016)
- **DOI:** 10.1021/acs.jpclett.6b01749
- **HAL 版:** hal-01366310（OA）
- **arXiv:** なし

## 内容要約（pdftotext 確認）

- **対象:** MAPbI₃ (Pm-3m pseudo-cubic phase) の Symmetry-Based TB モデル
- **TB 基底:** sp³s\* × spin = **8 functions**（小規模 TB）
- **SOC:** 含む
- **キー結果:** 
  1. Rashba effect for **uniaxial symmetry breaking** を TB レベルで実証
  2. R 点近傍の電子構造、SOC による伝導帯分裂
  3. **Volumetric strain と uniaxial strain の effect**
  4. DFT との比較で sizeable Rashba 効果を確認

## 本研究への含意

### Theme A（g 因子）
- MAPbI₃ 用 TB モデルの先行論文。Kashikar 2021 / Nestoklon 2021 と並ぶ
- 軌道基底は **sp³s\***（より大きい Kashikar 13軌道 / Nestoklon sp³d⁵s\* と比較対象になる）
- 論文の Methods で「Boyer-Richard 2016 の symmetry-based TB を、CsBX₃ 全 9 材料へ拡張するため、より大きい sp³d⁵s\* 基底（Kashikar/Nestoklon）を採用」と書ける

### Theme B → Theme F へのリブランド（既決定）
- novelty_assessment.md で既に判定済み：「Theme B (bond angle → Rashba TB) は Boyer-Richard 2016 と重複」
- 本 PDF を直接読めるようになり、**Theme F (shift current) の symmetry breaking 議論で Boyer-Richard 2016 を歴史的引用**として使える
- Theme F: 「Boyer-Richard 2016 は uniaxial strain で Rashba 効果を示した。本研究は同じ symmetry breaking 枠組みを **shift current** へ拡張する」

### Theme F での具体的活用
1. **歪み導入の方法論**: Boyer-Richard の uniaxial / volumetric strain TB パラメータ修正手順を参考に
2. **Rashba と shift current の関係**: 両者は同じ symmetry breaking 物理に由来。Boyer-Richard で Rashba 強度がどの程度か（DFT 値）を確認し、本研究の shift current 計算の妥当性チェックに使う
3. **論文の Introduction**: 「ハライドペロブスカイトの TB モデルは Boyer-Richard 2016 で symmetry-based に確立され、Kashikar 2021 が全 9 材料に拡張、本研究はさらに shift current / g 因子 / 光学への応用を拡張する」

## Claude Code への直接指示

1. **F4 で Boyer-Richard 2016 の strain TB を参照**
   - 既存実装の `shift_current.py` が使う strain パラメータが、Boyer-Richard と整合するか確認
   - Table 1 (TB パラメータ) と Table 2 (strain effect) を pdftotext で抽出して `docs/strain-tb-comparison.md` にまとめると有用

2. **Theme A 報告書の歴史的引用に追加**
   - `reports/theme_A_g_factor.md` §1 (動機) or §6 (論文化見通し) に「Boyer-Richard 2016 (JPCL) は MAPbI₃ で symmetry-based TB を確立し、本研究はこれを CsBX₃ 9 材料 + g 因子へ拡張」と追記

3. **references.md への追記**
   ```markdown
   ### arXiv 外 OA 追加（2026-05-23 ユーザー提供）
   
   | ファイル | 著者・年 | 内容 | 関連 |
   |---|---|---|---|
   | doi_10.1021_acs.jpclett.6b01749_BoyerRichard2016.pdf | Boyer-Richard et al., JPCL 7, 3833 (2016) | MAPbI₃ の symmetry-based TB、Rashba via uniaxial strain | Theme A・F の歴史的先行論文 |
   ```

## ハルシネーション防止

Boyer-Richard 2016 の TB パラメータ・式番号を Theme A/F の docstring で引用する際は、必ず PDF の該当式番号を確認してください（推測禁止）。例:
```python
# References:
# - Boyer-Richard et al., J. Phys. Chem. Lett. 7, 3833 (2016), Eq. (?)
#   for the sp3s* TB parameters of MAPbI3
```

Eq. 番号は PDF を読んで確定してから書く。

---

## 次のアクション

F4 (CsPbI3 で Tan & Rappe 2015 との shift current 照合) を引き続き Production モードで進めてください。Boyer-Richard 2016 は補強材料として活用。
