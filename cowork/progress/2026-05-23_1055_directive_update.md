# Directive Update — Phase 2 着手 (Theme F = BPVE / shift current) + Theme A 論文図 polish

**発行日:** 2026-05-23 10:55
**発行元:** Cowork（監督役）
**前提:** Phase 1.5 (B1-B5) クローズ済み（`2026-05-23_1055_code_review.md` 参照）。
**位置づけ:** `next_directive.md v2` §3 (Theme F) の **F1-F2 を起動**するための補足指示。
F3 以降の実装は formulation doc Cowork レビュー後に正式 GO。

---

## 0. 並行進行モデル（重要）

`CLAUDE.md` のドキュメント承認ルール（「1 ファイルごと作成 → 承認 → 次」）に従い、
**Theme F は formulation doc を先に確定**してからコード実装に入ります。Cowork レビュー
を挟むため、**待ち時間に Theme A 論文図 polish を入れる**ことで idle time を減らします。

```
[Theme F メイントラック]
  F1 (PDF 確認, ~30 min)
    → F2 (docs/shift-current-formulation.md draft, 2-3 h)
       → Cowork レビュー（formulation only, ~30 min Cowork 側）
          → F3 着手許可（次 directive で正式 GO）

[Theme A 論文図 polish サブトラック, 並行]
  (a) Fig.1 universal curve に TB-P 散布の重畳
  (b) ge_universality.png の 2 段化（任意）
  (c) Fig.2 Δ-dependence 再整理（Sn/Ge の不確かさバンド）
```

**判断は Claude Code 側に裁量を残します。** F2 を集中して仕上げる、A 図 polish
を先にやる、いずれも構いません。**ただし F3（コード実装）は formulation doc が
Cowork で承認されるまで保留**してください。

---

## 1. Theme F メイントラック詳細

### 1.1 F1: PDF 確認・取得（**最初の 30 分**）

`references/pdfs/` を確認し、以下 4 本の存在を確認してください:

| 出典 | 必須度 | 確認結果（Cowork 側） |
|---|---|---|
| **Young & Rappe 2012**, PRL 109, 116601, DOI:10.1103/PhysRevLett.109.116601 | **必須** | ❌ 未収集 |
| **Tan & Rappe 2016**, npj Comput. Mater. 2, 16026, DOI:10.1038/npjcompumats.2016.26 | **必須** | ❌ 未収集（OA の可能性大、Cowork で取得試行中） |
| **arXiv:2207.00331** (Passos & de Juan 2022, nonlinear optics review, Sipe-Shkrebtii 代替) | **必須** | ❌ 未収集 |
| **Fregoso, Morimoto, Moore 2017**, PRB 96, 075421 | あれば便利 | ❌ 未収集 |

**Claude Code 側のアクション:**

1. `references/pdfs/` を `ls` で確認し、上記 4 本の不在を明示的に報告（`progress/.../theme_F_pdf_status.md` 等）。
2. 並行して、`references/pdfs/` 既存の **arxiv_2105.11310.pdf** (bulk photovoltaic 関連、v1
   directive で既収集と明記) を読み、shift current の物理背景と語彙を整理。これは
   F2 の draft 着手時に役立ちます。
3. arXiv:2207.00331 が OA であれば `references/pdfs/arxiv_2207.00331.pdf` として
   取得してください（`curl` または既存スクリプト流用）。sleep を必ず挟む（arXiv は 3
   秒以上、レート制限注意 — `references/CLAUDE.md` 記載のルール）。
4. **Cowork 側で並行作業**: Tan & Rappe 2016 (npj Comput. Mater. は Nature Group OA)
   と Young & Rappe 2012 (PRL は paywall、preprint arxiv:1207.5462 の可能性)
   を Cowork が取得試行します。**F1 で取得不能でも F2 (formulation doc) は着手可能**
   — arXiv:2207.00331 (Passos & de Juan) と既知の Sipe-Shkrebtii Eq.(3.13) の形式から
   shift current の TB 表式は再構成できます。

### 1.2 F2: `docs/shift-current-formulation.md` draft（**~2-3 時間**）

#### スコープ

`docs/g-factor-formulation.md` および `docs/optical-formulation.md` と同じ構成で:

1. **§1 動機・適用範囲** — bulk photovoltaic effect (BPVE) の物理、shift current が
   p-n 接合を必要としない直接太陽電池機構である点、立方ペロブスカイトでは vanishing
   なので strain or octahedral tilting で対称性を破る点を明記。
2. **§2 支配方程式（Sipe-Shkrebtii / Young-Rappe）** — 出典付きで式を引用:
   ```
   σ^(shift)_abc(ω) = -π e³/ℏ² · ∫ dk/(2π)³
                       · Σ_{n,m} f_{nm} · Im[r^a_{mn} r^b_{nm;c}]
                       · δ(ω - ω_{nm})
   ```
   - Berry connection: `r^a_{mn} = i p^a_{mn} / (m₀ ω_{nm})` (n≠m)
   - covariant derivative `r^b_{nm;c} = ∂_c r^b_{nm} − i(r^c_{nn} − r^c_{mm}) r^b_{nm}`
   - δ → Lorentzian (η=0.05 eV, Tan & Rappe 2016 既定)
3. **§3 TB Hamiltonian での実装表式** — `velocity.py` の `velocity_operator(k)` から
   `p^a_{mn}` を得る方法、`r^b_{nm;c}` を **k 空間有限差分**で取る方法（Tan & Rappe 2016
   Methods に倣う）。**Wilson loop / projector trick** での代替計算法も併記
   （Fregoso 2017 で議論）。
4. **§4 対称性条件と symmetry breaker** — 立方 (Pm-3m) で σ^(2) = 0、空間反転対称を
   破る 3 オプションを比較:
   - **(I) Uniaxial strain** (5% [001] が標準、Tan & Rappe 2016 で使用)
   - **(II) Octahedral tilting** (Pnma 等の歪相、Theme B 旧計画の復活)
   - **(III) Static atomic displacement** (Cs offset etc.)
   - **推奨**: まず (I) uniaxial strain。1 軸スカラパラメータ ε で系統スキャン可能。
5. **§5 検証アンカー** — Tan & Rappe 2016 の MAPbI₃ shift current ピーク位置 (~2-3 eV)
   と振幅 (~10-100 μA/V²) を `±0.1 eV` ピーク位置、`order-of-magnitude` 振幅で再現
   できるかを受け入れ基準とする。立方等方無歪みで σ^(2) ≈ 0（数値積分誤差以内）。
6. **§6 既知の限界（Blount 1962 narrative の continuation）** — TB position operator
   `r = i ∂_k` は intra-atomic 成分を欠くため shift current の絶対振幅も系統的に過小
   になる可能性が高い（g 因子・f-sum と同根）。**論文の統一メッセージ**として明記。
   Tan & Rappe 2016 の Wannier 比較を引用予定。
7. **§7 数値設計** — k グリッド 6³/8³/12³, η, 強度依存 ε, smearing 検証計画。
   `results/shift_current/convergence.md` で記録予定。
8. **§8 参考文献** — Young & Rappe 2012, Sipe & Shkrebtii 2000, Tan & Rappe 2016,
   Fregoso 2017, Passos & de Juan 2022 (arXiv:2207.00331), Cook et al. 2017,
   Blount 1962（統一 narrative）。

#### Cowork レビューポイント（事前共有）

F2 完了報告（`progress/.../theme_F_F2_complete.md`）を Cowork が確認する際、以下を
チェックします:

- (a) σ^(2)_abc(ω) の **式に sign convention** が Sipe-Shkrebtii Eq.(3.13) と
  一致しているか（よくある符号ミスポイント）
- (b) Berry connection の **n=m 対角項**を除外する処理が明示されているか
- (c) **立方対称下で vanishing** を実装でどう保証するか（cancel by k-grid symmetry
  か、Bloch-state phase fixing か）
- (d) **symmetry breaker (uniaxial strain)** の Hamiltonian 修正方法が
  `data/parameters/SOURCES.md` の Kashikar/Nestoklon パラメータと整合する形で書かれ
  ているか（bond length × ハーモニック exponent η_strain で hopping 修正、出典付き）
- (e) **検証アンカー Tan & Rappe 2016 の Fig 番号と読み取り値**を明示しているか

#### Claude Code 側の判断ルール（重要）

- **F2 着手で文献の式が読めない場合**（Tan & Rappe / Young & Rappe が paywall で
  arxiv プレプリントも未収集 + Cowork 側取得も失敗）: arXiv:2207.00331 の Sipe-Shkrebtii
  representation + 既収集の **arxiv_2105.11310.pdf** の引用情報のみで σ^(2)_abc の
  TB 表式を sketch し、「**Tan & Rappe 2016 を読まずに書いた draft**」と明示して
  Cowork に提出してください。Cowork が PDF 取得後に式の照合を行います。
- **検証アンカー** (§5) は PDF 取得待ちなので、**「Tan & Rappe 2016 Fig X の MAPbI₃
  ピーク（要 PDF 取得）」** とプレースホルダで書いて OK。
- **F3 (コード実装) は formulation doc Cowork 承認待ち**。先走りで実装しないでください
  （`CLAUDE.md` プロジェクトメモリの「1 ファイルごと承認」ルール）。

### 1.3 F2 完了後の作業（参考、別 directive で詳細化）

- **F3**: `src/perovskite_tb/shift_current.py` 実装（σ^(2)_abc(ω) 計算）
- **F4**: 検証テスト（Sipe-Shkrebtii sum rule, MAPbI₃ ピーク再現, 立方対称 vanishing）
- **F5**: 9 材料 × strain スキャン（5% [001] uniaxial）
- **F6**: 報告書 `reports/theme_F_shift_current.md`

これらは F2 承認後の directive で正式着手指示します。

---

## 2. Theme A 論文図 polish サブトラック（並行・任意）

Theme F の Cowork レビュー待ち時間や、F2 集中疲れの息抜きとして、以下を進めて
いただけると論文ドラフト着手が早まります。**順不同・優先度低**:

### 2.1 (a) Fig.1 universal curve に TB-P 散布の重畳（**~30 分**）

既存 `results/g_factors/ge_universality.png` を発展させ、**論文 Fig.1** として:

- 横軸: 1/Eg
- 縦軸: g_e
- 黒線: 普遍 P=6.8 (Kirstein) の予測直線
- 黒四角: Pb Table-S2 ETB 値（実測アンカー）
- カラー丸: TB-derived P での 9 材料予測（Ge=green, Sn=orange, Pb=blue）
- インセット or 別パネル: 普遍 P 直線に対する **残差** (TB-derived 予測 − 普遍曲線)

これにより「**普遍曲線は zero-th order、TB-derived P の系統的不足が 1st order
correction**」が直接読み取れます。

### 2.2 (b) ge_universality.png の 2 段化（任意・推奨）

`scripts/plot_ge_universality.py` を 2 段プロットに拡張:

- 上段（現状）: g_e vs 1/Eg with universal-P line, TB-P points, Pb anchors
- 下段（新規）: P vs E_g の棒グラフで
  - 灰: 普遍 P=6.8（横線）
  - 黒: inverse-P from Pb Table-S2 (3 点、~6.80 一定)
  - カラー: TB-derived P (9 材料、4.1〜5.9 散らばる)

これにより A7 の semi-circular 性が一目で見え、論文 §5 の議論を支えます。

### 2.3 (c) Fig.2 Δ-dependence 再整理（**~1 時間**）

既存の Δ vs g_h プロット（`results/g_factors/` 内 該当ファイル）に:

- Sn/Ge の Δ 不確かさバンド（Kashikar Eq.9 から ±20% 推定範囲）をエラーバンドで追加
- 不確かさを反映した g_h 予測の uncertainty range も bar/band で表示

これは review #5 で言及した「Δ 推定の ±20% を g 因子に伝搬」の可視化です。
論文 Fig.2 として使えます。

### 2.4 サブトラックの完了条件

- (a)-(c) は **任意**。1 つでも実施したら commit + `progress/.../theme_A_figures_polish.md`
  で報告してください。
- 全部やる必要はなく、Theme F の F2 が忙しければスキップして OK。
- 完成図は `reports/theme_A_g_factor.md` 末尾の図リストに自動で組み込まれるので、
  論文ドラフト着手時に再利用できます。

---

## 3. PDF 取得 Cowork タスク（参考）

Cowork 側で並行進行する PDF 取得タスク（Claude Code は意識不要、`references/pdfs/`
に新規ファイルが現れたら使えると思ってください）:

| 出典 | 取得方針 | 完了予定 |
|---|---|---|
| arXiv:2207.00331 (Passos & de Juan) | `curl -sL https://arxiv.org/pdf/2207.00331` | F2 着手まで |
| Tan & Rappe 2016 npj Comput. Mater. | DOI:10.1038/npjcompumats.2016.26 (Nature Group OA) | F2 検証アンカー記載まで |
| Young & Rappe 2012 PRL | arxiv:1207.5462 (preprint) を試行、無ければ Cowork → ユーザー相談 | F3 着手前 |
| Fregoso 2017 PRB | arXiv:1612.09194 (推定) | F3 着手前 |

**Claude Code 側へのお願い**: F1 で `references/pdfs/` を確認した時点で、上記の
**どれが追加で必要か**を `progress/.../theme_F_pdf_status.md` で報告してください。
Cowork が優先順位を組み直します。

---

## 4. タイムライン目安

```
今 (10:55) ──┬── [F1] PDF 確認 (~30 min) ─── progress 報告
             │
             ├── [Theme A polish (a)] (~30 min, 任意)
             │
             └── [F2] docs/shift-current-formulation.md draft (~2-3 h)
                     │
                     └── progress/.../theme_F_F2_complete.md
                             │
                             └── Cowork レビュー (次の巡回時間)
                                     │
                                     └── F3 GO 指示 (次 directive)
```

巡回は 1 時間ごとなので、F2 完了報告は次の巡回（~12:00）で拾います。それまでに
F2 が終わらなくても問題ありません — partial draft でも Cowork が現状を確認できます。

---

## 5. CLAUDE.md ルール再確認

実装フェーズ (F3) に入ったとき、特に以下を厳守してください:

- **物理量には必ず単位を明記**（変数名・コメント・docstring）
- **浮動小数点の等価比較禁止**（許容誤差使用）
- **マジックナンバー禁止**（出典明示）
- **乱数シード明示管理**（shift current で MC 積分する場合）
- **計算結果メタデータ**（コミットハッシュ・パラメータ・実行日時）
- **既存テスト（205 個）破壊なし**

ハルシネーション防止ルール（`next_directive.md v2 §0`）も厳守:
- 全実装に DOI/arXiv ID + 式番号を docstring 明記
- 論文に明示されていない数値は推測しない（不明なら Cowork 確認）

---

## 6. ユーザー判断が必要かもしれない箇所（事前列挙）

以下は Phase 2 進行中に**ユーザー相談が必要になる可能性**がある事項。Cowork が
途中で判断に迷ったらユーザー通知します:

1. **Tan & Rappe 2016 が OA で取得できない場合**: 代替論文 (Cook 2017 Nat. Commun.
   等) で進めるか、ユーザーに paywall PDF 提供を依頼するか。
2. **Symmetry breaker の選択**: uniaxial strain (推奨) で進めるか、octahedral tilting
   も含めるか。後者は Theme B (旧) を復活させる規模感のため、ユーザー方針確認したい。
3. **9 材料 × strain スキャン後**、Sn/Ge の予測が「shift current 顕著に大きい」と出た
   場合、論文の主結果として強調する判断（実験との照合可能性をユーザーに確認）。

これらは現時点では発生していません。

---

## 7. まとめ

- **Phase 1.5 クローズ** ✅
- **Phase 2 Theme F 着手**: F1 (PDF 確認) → F2 (formulation doc draft) を **指示**
- **F3 (実装) は formulation doc 承認後** に正式 GO
- **Theme A 論文図 polish** を並行サブトラックとして任意実施
- **Cowork 側で PDF 取得を並行進行**

質問・判断に迷う点があれば `progress/.../theme_F_question.md` で報告してください。
1 時間ごとの巡回で拾います。

引き続きよろしくお願いします。
