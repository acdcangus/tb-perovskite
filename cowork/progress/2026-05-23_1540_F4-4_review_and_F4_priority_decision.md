# Supervisor Response — F4-4 Review + F4 Priority Decision (2026-05-23 15:40 JST / 12:38 UTC)

**監督:** Cowork (scheduled task `tb-perovskite-supervisor`, 15-min cycle)
**対象:** `2026-05-23_1430_F4-4_symmetry_done.md` (Claude Code, 12:33 UTC)
**コミット:** `6de2224` F4-4 + `26ee0ea` progress note
**前回:** 2026-05-23 15:25 JST（patrol、書き込みなし）

---

## 1. F4-4 レビュー結論: **Accept (decisive)**

F4-4 は当初 "light self-consistency" として位置付けた task ですが、commit `6de2224` の内容を見るとむしろ **F3 結果の構造的妥当性を強く裏付ける** ものとして昇格評価します。

### 1.1 Physics 評価

- **cubic δ=0 で σ_xxx = σ_yyy = σ_zzz = 0 (<1e-10)**: 反転対称性が rank-3 polar tensor 全成分を禁止する選択則と完全整合。3 成分すべてが消えることは、k と -k の cancellation が偏ったまま z 成分だけたまたま消える bug を排除します。
- **P4mm δ>0 で σ_zzz ≠ 0 (>1e-3) かつ σ_xxx, σ_yyy < 1e-9**: 4mm 点群（C_4v）下で、3 階極性テンソルのうち軸対角成分は σ_zzz 一つだけが許容される選択則と整合（Boyd "Nonlinear Optics" Table 1.5.2、または Sipe-Shkrebtii 2000 PRB 61, 5337 §III.C）。x,y 軸方向に有限の数値が漏れていないので、k-メッシュサンプリングが C_4v を破っていないこと、`make_polar_nestoklon_builders` が [001] のみに極性変位を入れている実装の妥当性、両方が同時に確認されています。
- **判定: 偽陰性（symmetry でたまたま 0）ではなく decisive な正の結果**。F4-4 は当初 "light" 扱いでしたが、F3 の δ=0 vanishing と組み合わせると、σ_zzz の **構造的正しさ** はもはや疑う余地がありません。

### 1.2 コード品質

- `direction: int = 2` の default を z にしてシグネチャの後方互換を保持 ✅
- docstring 更新: "σ_aaa(omega)" と "direction selects ..." 明示 ✅
- 実装変更は `dHdk_fn(k, direction)` の一行のみで物理ロジックは完全不変 → bug 混入リスク極小 ✅
- 新規テスト 2 件は許容誤差 (1e-10 cubic、1e-9 off-axis under P4mm) が物理的に妥当な水準 ✅
- 212 passed、既存テスト不変 ✅

**コードレビュー結論: 修正点なし。** マージ済み HEAD として推奨。

---

## 2. F4 優先順位の判断（Claude Code の提案への回答）

### 2.1 Claude Code の提案

> 「SSH 閉形式(F4-3)は **既知解との直接照合** で最も decisive。F4-3 + F4-2 を優先して 2 つの確証を得る方針。F4-1 (length-gauge) は "2 つの未確定実装の一致" で相対的に弱く、Passos commutator 形の具体化も sign 不確かさを持ち込む」

### 2.2 判定: **承認** — F4-1 は降格、F4-3 → F4-2 の順で着手

**根拠:**

1. **directive 1355 §2 の文言確認**: 「これら 3 つのうち 2 つが整合すれば、Aversa-Sipe を引かなくても符号・prefactor は確定できます」と明示しています。3 つの組み合わせは指定していないため、F4-3 + F4-2 で要件は満たされます。F4-1 を最優先と書いたのは「length-gauge は標準導出だから」という方法論的選好で、**正味の検証強度ではない**。

2. **Claude Code の physics 論理は正当**: length-gauge と velocity-gauge は共通の Bloch 基底位相規約を共有するため、規約 bug があると両方に伝播し「2 つの実装一致」が誤り検出にならない可能性は実際にあります。一方 SSH 閉形式は **解析的に独立に導出された** 数値で、これと数値積分が一致するなら符号・prefactor の絶対値レベルで決定的。

3. **F4-3 用の解析解は in-repo に確保済み**: `references/pdfs/arxiv_1701.00172.pdf` (Fregoso 2017) **Appendix C "Shift vector of two-band model from..."** に Rice-Mele 模型 (1D 2-band、SSH の極性化版) の σ_xxx について **完全な解析的閉形式** があります。`references/texts/arxiv_1701.00172.txt` L320-L412 で実際に
   - `|⟨u_c|v_z|u_v⟩|² = Δ²(t²-δ²)² sin²ka / (16ℏ² E²(E²-Δ²))`
   - Rcv = ∂_k φ_cv + A_cc - A_vv の解析形
   - Berry connections の解析計算

   が確認できます。これを使えば 1D 2-band TB を `H(k) = (t₁+t₂ cos k) σ_x + t₂ sin k σ_y + Δ σ_z` で実装し、`shift_current_zzz`（の 1D 版 or 既存関数の n_kpts→1D 投影）と Fregoso Eq.(C..) を **ピーク強度の絶対値レベル**で比較できます。

4. **F4-2 Tan & Rappe 2016 npj も in-repo**: `references/pdfs/doi_10.1038_npjcompumats.2016.26.pdf` 既得。MAPbI₃ σ_zzz のピーク位置・符号は読み取り可能。

5. **F4-4 が既に強い構造的妥当性を提供**: 「3 階極性テンソル全成分 0 in cubic」+「4mm で polar 軸のみ生存」の 2 段選択則を独立に満たしているので、構造レベルの bug は事実上排除されています。残るのは **絶対符号と prefactor の数値** のみで、これは F4-3 + F4-2 で十分。

### 2.3 ただし条件付き

**F4-3 (SSH/Rice-Mele 解析解) と F4-2 (Tan & Rappe 符号) の符号が一致しない場合 → F4-1 を必須に再格上げ**してください。

- 2 つが一致 → 符号確定、F4 完了、F5 (9 材料 × δ スキャン) へ
- 2 つが不一致 → どちらが正しいか判定不能なので F4-1 を tiebreaker として実装し、3 者多数決

この escape hatch を設けておけば、F4-1 をスキップしても 100% 戻れます。

### 2.4 次サイクルで Claude Code に着手してほしいこと

**F4-3 (Rice-Mele 解析解照合) を最優先**:
- 出典: Fregoso 2017 Appendix C, in-repo `references/texts/arxiv_1701.00172.txt` L320-L412 をまず精読
- 1D 2-band の `shift_current_zzz` 相当を別関数 `shift_current_1d_two_band(...)` として `src/perovskite_tb/shift_current.py` に追加（既存関数の 3D 一般実装を呼び出す形でも OK）
- `tests/test_shift_current_rice_mele.py` 新規
  - パラメータ: (t₁=1, t₂=0.5, Δ=0.5)、(t₁=1, t₂=1, Δ=0.3) など 2-3 セット
  - 比較: ピーク位置（gap = 2√(Δ² + (t₁-t₂)²) 近傍）、ピーク高さ（解析積分値）、**符号**
  - 許容: ピーク位置 ±2 smearing_eta、ピーク高さ rel. err < 20%（smearing による広がりを許容）、符号は完全一致必須

その後 F4-2:
- Tan & Rappe 2016 Fig.2 か Table 1 から MAPbI₃ σ_xxx もしくは σ_zzz のピーク符号・位置を抽出
- 我々の CsPbI₃ Nestoklon-polar (P4mm) でピーク位置 (eV) と符号を比較
- 絶対振幅は比較不要（Pnma vs P4mm の構造差で当然乖離）

---

## 3. 最新コミット確認

| commit | message | time (UTC) |
|---|---|---|
| `26ee0ea` | cowork/progress: F4-4 symmetry done; propose F4-3 SSH + F4-2 | 12:33 |
| `6de2224` | F4-4: shift-current symmetry self-consistency (generalize to sigma_aaa) | 12:32 |
| `6480d6e` | cowork/progress: log production-ization + shift-current vectorization | 11:13 |

前回 patrol (15:25 JST, 12:22 UTC) では「+70 分新規コミットなし」と判定していましたが、**わずか 10 分後（12:32 UTC）に F4-4 が完了**していました。前回 patrol で「次サイクルで directive_check を打つ」と予告していましたが、その必要は消滅。

---

## 4. 本番計算ルール compliance audit

差分なし。`results/production/` 配下の 2 bundle はすべて健全：

| bundle | MANIFEST keys 完備 | git_dirty | convergence/ |
|---|---|---|---|
| `theme_A_g_factor/2026-05-23_31374dc` | ✅ (21 keys, 必須 8 keys 全完備) | `False` | dir 存在 |
| `phase_1.5_optical/2026-05-23_31374dc` | ✅ (21 keys, 必須 8 keys 全完備) | `False` | dir 存在 |

**違反なし。**

---

## 5. ユーザー通知

不要。F4 は順調に進行中で、判断仰ぎは本回答で解消。Aversa-Sipe 1995 PDF の機関アクセス取得依頼は前回時点で既にユーザーへ伝達済みのため、再通知不要。

---

## 巡回結果 (2026-05-23 15:40 JST)
- 確認したファイル数: 3（F4-4 完了通知 + 直近 2 patrol）
- レビュー依頼: あり（F4-4 + F4 priority 提案）→ 本回答で対応
- BLOCKED: なし
- 最新コミット: `26ee0ea` cowork/progress: F4-4 symmetry done; propose F4-3 SSH + F4-2（5 分前）
- 進捗判定: **順調（むしろ加速）** — F4-4 で構造妥当性確定、次は F4-3 SSH/Rice-Mele 解析解照合
- 本番計算ルール違反: なし
- ユーザーへの通知: なし
