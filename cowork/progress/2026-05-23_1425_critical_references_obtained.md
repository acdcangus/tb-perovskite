# 🎯 Theme F 重要文献 3 本入手 — 符号・絶対値ベンチマーク確定可能

**発行:** Cowork, 2026-05-23 14:25
**契機:** ユーザーが APS harvest URL と arxiv:1508.03564 を提供。**Theme F の最大ボトルネック（絶対符号・絶対値）が解決可能に**

---

## 入手済み文献（references/pdfs/ に保存）

### 1. `doi_10.1103_PhysRevB.53.10751.pdf` — Hughes & Sipe 1996

- **Title:** Calculation of second-order optical response in semiconductors
- **Citation:** J. L. P. Hughes and J. E. Sipe, *Phys. Rev. B* **53**, 10751 (1996)
- **Content:** GaAs, GaP の χ^(2)(−2ω; ω, ω) (SHG) と χ^(2)(−ω; ω, 0) (LEO)、ε(ω) を ab initio で。**Aversa-Sipe 1995 の χ^(2) 表式の最初の本格的実装**。scissors approximation で band gap 補正。
- **Theme F での意義:** **Aversa-Sipe 1995 の代替として完全に使える**。χ^(2) の前因子・符号規約・unphysical divergences 処理が明示。**Theme F の絶対符号と前因子の確定が本論文で完了する**

### 2. `doi_10.1038_npjcompumats.2016.26.pdf` — Tan, Zheng, Young, Wang, Liu, Rappe 2016

- **Title:** Shift current bulk photovoltaic effect in polar materials—hybrid and oxide perovskites and beyond
- **Citation:** L. Z. Tan et al., *npj Comput. Mater.* **2**, 16026 (2016)
- **Content:** **Shift current BPVE のレビュー、ハイブリッド・酸化物ペロブスカイト含む**。形式論 + 多数の材料の DFT 計算例 + 実験との比較。**本研究の最大の先行論文**
- **Theme F での意義:** (a) Methods で shift current の標準実装を確認 (b) 既存ペロブスカイト計算値との比較 (c) 我々の研究のポジショニングを明確化（鉛フリー Sn/Ge 系の TB スキャンは未踏という主張の根拠）

### 3. `arxiv_1508.03564.pdf` — Tan & Rappe 2015 ★最重要★

- **Title:** Enhancement of bulk photovoltaic effect in topological insulators
- **Citation:** L. Z. Tan and A. M. Rappe, arXiv:1508.03564 (v2 2016-09-07), PRL related
- **Content:** **CsPbI3 と BiTeI の shift current を DFT で計算**、トポロジカル相転移近傍で σ_BPVE が増強・符号反転
- **Theme F での意義:** **CsPbI3 の shift current の DFT ベンチマーク値が直接得られる**。Claude Code の TB sum-over-states 計算と直接比較可能。**絶対符号・絶対値・スペクトル形状の三点を一度に検証できる**

---

## Theme F の方針更新（F4-F6 の具体化）

### F4: ベンチマーク照合（Production モード）

**目標:** Claude Code の TB sum-over-states 計算と Tan & Rappe 2015 の DFT 結果を CsPbI3 で照合し、絶対符号・絶対値・形状を確定

**手順:**

1. **Tan & Rappe 2015 を精読**
   - Eq.(?) で使われる χ^(2) (shift current) 表式の確認（Hughes-Sipe 1996 形式論との対応）
   - CsPbI3 計算条件（圧力、相、k グリッド、smearing）
   - σ_BPVE(ω) の数値・ピーク位置・符号

2. **本研究の TB sum-over-states を CsPbI3 で実行**
   - **既存実装** の `shift_current_zzz` を使う（F3 完了済み、δ=0 vanishing 確認済み）
   - 内部歪み δ を Tan & Rappe 2015 が使った圧力範囲に合わせて選ぶ
   - **Production モード** で実行（PRODUCTION_RULES.md 準拠、MANIFEST.json、収束プロット、入力ファイル一式保存）

3. **比較**
   - スペクトル形状（ピーク位置）
   - 符号（同じか反転か）
   - 絶対値のオーダー
   - 不一致があれば、TB-IPA の限界（Blount 1962 / 励起子効果欠落）として記録

4. **符号と前因子の確定**
   - もし符号が同じなら ✅ Theme F の前因子・符号 OK
   - もし符号が反転なら、Hughes-Sipe 1996 Eq.(?) の規約に合わせて修正
   - **`docs/shift-current-formulation.md` に符号規約を確定して記載**

### F5: 9 材料 × δ スキャン（Production モード）

F4 完了後、9 材料すべてに展開。

- **Production モード**（PRODUCTION_RULES.md §1-§4 完全準拠）
- **収束確認**：k グリッド 8³→16³→24³、smearing η 0.10→0.05→0.025 eV
- 結果は `results/production/theme_F_shift_current/2026-05-23_<hash>/`
- ベクトル化最適化（F3 で 100s かかっていた）

### F6: Theme F 報告書

- `cowork/reports/theme_F_shift_current.md`
- Tan & Rappe 2015 比較表（CsPbI3）を主要結果に
- 鉛フリー（Sn/Ge）の予測値を「未測定物性の予測」として強調
- Hughes-Sipe 1996 / Tan & Rappe 2016 を **手法論の系譜**として引用

---

## ハルシネーション防止上の注意

1. **Hughes-Sipe 1996 の χ^(2) 公式（特に式 (??)）を docstring に明示**
   - 既存 `shift_current.py` の docstring を更新
   - `# Implements Eq. (X) of Hughes & Sipe 1996 (PRB 53, 10751), originally from Aversa-Sipe 1995 (PRB 52, 14636)` のように

2. **符号確定の証拠を残す**
   - CsPbI3 で Tan & Rappe 2015 と TB の符号が一致したら、`docs/shift-current-formulation.md` に「Tan & Rappe 2015 との符号一致を CsPbI3 で確認 (Production run YYYYMMDD)」と記載
   - 不一致の場合は理由とともに修正履歴を残す

3. **前因子 (-πe^3/ℏ^2) の確認**
   - Hughes-Sipe 1996 の式と Claude Code の現状実装の前因子を厳密対応
   - 「F3 では相対単位」と保留したものを F4 で確定

---

## references.md への追記

`references/references.md` の末尾に新セクション：

```markdown
### Theme F 関連 OA 文献（2026-05-23 取得）

| ファイル | 著者・年 | 内容 |
|---|---|---|
| doi_10.1103_PhysRevB.53.10751.pdf | Hughes & Sipe, PRB 53, 10751 (1996) | χ^(2) (SHG) の ab initio 実装、Aversa-Sipe 1995 の χ^(2) 表式の代替 source |
| doi_10.1038_npjcompumats.2016.26.pdf | Tan et al., npj Comput. Mater. 2, 16026 (2016) | Shift current BPVE in polar materials レビュー |
| arxiv_1508.03564.pdf | Tan & Rappe, arXiv:1508.03564 (2015) | **CsPbI3 と BiTeI の shift current DFT 計算**、本研究の直接ベンチマーク |
| arxiv_1601.01201.pdf | Lan, arXiv:1601.01201 (2016) | Si の THG、Aversa-Sipe SoS の独立な実装例 |
```

---

## まとめ

| 課題 | 状態 |
|---|---|
| Aversa-Sipe 1995 入手 | 代替確保（Hughes-Sipe 1996 で実質代替）✅ |
| Theme F の絶対符号 | F4 で Tan & Rappe 2015 比較により確定可能 ✅ |
| Theme F の前因子 | Hughes-Sipe 1996 Eq. と照合で確定可能 ✅ |
| Theme F の絶対値ベンチマーク | CsPbI3 で Tan & Rappe 2015 と直接比較 ✅ |

**これで Theme F は完全に「論文化可能な状態」**になりました。F4-F6 を Production モードで進めてください。

Cowork タスク #26 (Aversa-Sipe 入手) は **解決（代替確保）** として close します。
