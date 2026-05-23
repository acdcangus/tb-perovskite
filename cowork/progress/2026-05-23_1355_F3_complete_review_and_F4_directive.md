# Code Review 返答 — F3 完了確認 & F4/F5 指示 (2026-05-23 13:55)

**対象:** commit `2147a3b` (`src/perovskite_tb/shift_current.py`, `tests/test_shift_current.py`)
**返答先:** `cowork/progress/2026-05-23_1320_theme_F_F3_complete.md`
**結論:** **F3 を構造的に受理 (accept-with-conditions)**。δ=0 で max|σ_zzz|=4.6e-15、δ>0 で線形発現は decisive な構造検証であり、Cowork の (B) 推奨をクリーンに実装したと判定します。**絶対符号・prefactor は F4 で Tan & Rappe MAPbI₃ ピーク照合をもって確定**してください。Aversa-Sipe 1995 PDF は **取得不可**（下記）。

---

## 1. F3 検証結果（独立確認）

### 1.1 δ=0 vanishing が decisive である理由（再確認）

- 中心対称 (δ=0, Pm-3m) では σ^(2)_zzz は **対称性で厳密に 0**（Sipe-Shkrebtii 2000 PRB 61, 5337 Sec. III.C ＝ inversion-odd の rank-3 polar tensor が consistent な唯一の値 0）。
- 4.6e-15 は double precision のラウンド shoulder（ε_machine ~ 2.2e-16 × O(N_band × N_k × N_l) ~ O(10²-10³) の和）と整合。
- これは **符号規約・prefactor 規約に非依存**な必要条件で、もし `r^z_{vc;z}` 公式の構造（"first-term + virtual-sum" の相対重みと相対符号）が誤っていれば、k と -k の cancellation が破綻して O(1) の残留が出る。
- 従って **(B) 公式の構造 ＝ 第 1 項（band-velocity 差項）と第 2 項（仮想中間状態の和）の比 ＝ 正しい** と判定。Kramers 縮退の扱い（deg_tol スキップ）も適切。

### 1.2 δ-依存性のチェック

報告されたピーク強度 0.13 / 0.26 / 0.54 (δ=0.05/0.10/0.20 Å) は概ね線形 (ratio 2.0, 2.08)。これは Pb-I_z bond の Harrison scaling が δ で O(δ) の inversion-odd 差を生むことと整合（最低次摂動）。実数性も TRS 帰結として OK。

### 1.3 既存テストへの影響

210 passed、xfail/skipped なし。前 phase の B5・A6・F2 はすべてグリーン継続を確認します（commit log で `_abelian_deprecated` への rename だけが破壊的変更で、production path には未使用）。

### 1.4 ハルシネーション防止ガード（評価）

- 旧関数を `_abelian_deprecated` で残置 → 回帰可能 ✅
- docstring に Aversa-Sipe / Sipe-Shkrebtii / Fregoso / Passos の出典明記 ✅
- "VALIDATION STATUS" セクションで「相対単位・符号未確定」を明示 ✅
- F3 完了通知で primary source の符号未照合を自己申告 ✅

**判定: ハルシネーション防止規律を完全に順守**しています。これは本 directive 0 節の運用模範例。

---

## 2. Aversa-Sipe 1995 PDF 取得 — 不可（Cowork 試行結果）

- **arXiv: なし**（1995-09 投稿、arXiv の cond-mat は当時存在しても投稿例少。確認済）
- **APS journals.aps.org**: Cloudflare bot challenge ＋ 購読壁。web_fetch path 経由では取得不可
- **OpenAlex / DOAJ / PMC**: PRB 52, 14636 (1995) は OA 化されておらず、PDF link なし
- **Sci-Hub 等の非正規ルート**: Anthropic 利用規約・著作権上不可

→ **以下の代替手段で符号を確定**してください（§3 F4 タスク参照）:
1. **既存 in-repo の Passos 2018 Eq.(13) commutator 形 ＋ Sipe-Shkrebtii 2000 Eq.(4.5) sum-over-states 形を「両方で実装」して数値一致確認**（length-gauge ↔ velocity-gauge 同値性チェック; Passos 2018 が言う通り無限バンドでは厳密一致）
2. **Tan & Rappe 2016 npj Comput Mater 2:16026 の MAPbI₃ σ_zzz ピーク位置（および可能なら符号）と照合**
3. **SSH toy model（1D 2-band）の解析解と peak 位置で比較**（Sipe-Shkrebtii 2000 §IV.B 付近に SSH 例題あり）

これら 3 つのうち 2 つが整合すれば、Aversa-Sipe を引かなくても符号・prefactor は確定できます。

### 2.1 ユーザー経由での入手依頼を提案

ユーザー（Teruhisa さん）に「PRB 52, 14636 (1995) の PDF を入手して `references/pdfs/doi_10.1103_PhysRevB.52.14636.pdf` に置いてほしい」と直接依頼することを提案。研究機関アクセスがあれば 1-2 分で済む。私（Cowork 監督）からこの回答に併せてユーザー通知を出します（§6）。

---

## 3. F4 指示: 検証 (Validation)

### 3.1 F4-1. 長さゲージ vs 速度ゲージの同値性チェック（最優先）

**目的:** Aversa-Sipe の符号・prefactor を **独立な 2 つの導出**で照合する。Passos 2018 の主張は「length と velocity gauge は無限バンドで厳密一致、TB 有限バンドで近似一致」。よって我々の有限バンド (n_orb=8 など) では完全一致は期待できないが、**符号と桁・スペクトル形状は一致**するはず。

**実装:**
- `src/perovskite_tb/shift_current_length_gauge.py` を新規作成
- 出典: Passos 2018 Eq.(13) `h^{α₁...αₙ}_kss' = ℏ⁻ⁿ [D^αₙ, [..., [D^α₁, H₀]]]_ss'`（in-repo: `references/texts/arxiv_1712.04924.txt` L130, L170 付近）
- n=2 の場合の σ^(2) を **共変微分の commutator 形**で書く（length-gauge 標準）
- 関数名: `shift_current_zzz_length_gauge(...)` （現 velocity-gauge 版と同じシグネチャ）
- テスト: `tests/test_shift_current_gauge_equivalence.py`
  - 同じ k グリッド・smearing で `shift_current_zzz` (velocity) と `shift_current_zzz_length_gauge` (length) を実行
  - ピーク位置と相対形状（cosine 類似度 > 0.95）が一致
  - 絶対振幅は有限バンド誤差で乖離 OK、**符号は一致必須**

**着手前に必読:** `references/texts/arxiv_1712.04924.txt` 全文（特に Appendix B "From length to velocity gauge"）。Passos らが length→velocity 変換の式を明示しているはず（L614-L616 付近で "From Eq. B5, we can give the position operator the following representation:" と続いている）。

### 3.2 F4-2. Tan & Rappe 2016 MAPbI₃ 照合

**目的:** **絶対符号 + 桁** の最終確定。

- `references/pdfs/doi_10.1038_npjcompumats.2016.26.pdf` を読み、Fig.2 (a)/(b) または Table の MAPbI₃ σ_xxx もしくは σ_zzz のピーク位置・符号・桁を抽出
- **重要:** 我々の Nestoklon-polar (P4mm, [001] off-centring) は MAPbI₃ の experimental Pnma 構造と異なるため **絶対振幅の一致は期待しない**。ピーク **位置** (eV) と **符号** だけ照合
- ピーク位置（gap + α·band-velocity）が ±0.2 eV で一致すれば OK
- 符号が逆なら、`shift_current.py` の最終 prefactor を反転する commit を分けて打つ（commit message に "sign flip per Tan & Rappe 2016 Fig.X" と明記）

### 3.3 F4-3. SSH toy validation

**目的:** 完全に閉じた解析解との照合で **prefactor 確定**。

- `tests/test_shift_current_ssh.py` 新規
- 1D 2-band SSH: `H(k) = (t₁ + t₂ cos k) σ_x + t₂ sin k σ_y + Δ σ_z`
  - 反転対称破れ: t₁ ≠ t₂（or sublattice on-site Δ）
- Sipe-Shkrebtii 2000 Eq.(4.5) の SSH 解析計算は **Cook, Fregoso et al. 2017 Nat Commun 8:14176 Methods** に閉じた形あり。`references/` 内に PDF があれば該当式を docstring 引用、無ければ追加収集を依頼
- ピーク位置（gap = 2|Δ|）と peak の **積分量**（sum rule、Sipe 2000 Eq.4.5）が解析値と数値積分で一致

### 3.4 F4-4. TRS / 対称性 self-consistency check（軽量）

- `tests/test_shift_current.py` に追加:
  - `test_real_valued`: σ_zzz(ω) が `np.allclose(sigma.imag, 0)` 相当（既に複素入りでないが、念のため）
  - `test_offdiag_vanishes_in_cubic`: 立方 (δ=0) で σ_xxx, σ_yyy も併せて 0（zzz だけでなく diagonal 全部）
  - `test_polar_axis_only`: P4mm δ>0 で σ_zzz ≠ 0 だが σ_xxx ≈ σ_yyy ≈ 0（[001] 偏極なので）

---

## 4. F5 指示: 9 材料 × δ スキャン

F4 完了後（少なくとも F4-1 と F4-2 で符号確定後）に着手:

### 4.1 タスク

- `scripts/scan_shift_current.py`
- 9 材料 (Cs{Pb,Sn,Ge}{Cl,Br,I}₃) × δ ∈ {0.00, 0.05, 0.10, 0.15, 0.20} Å（5 点）
- ω_grid: [0.5, max(Eg_i) + 2.0] eV、step 0.01 eV
- η = 0.05 eV (Tan & Rappe 既存と同じ)
- n_kpts = 8 × 8 × 8 で初回、収束チェックで 12³ も
- 出力: `results/shift_current/sigma_zzz_<material>_<delta>.npz` (各 45 ファイル) ＋ サマリ `results/shift_current/sigma_peak_summary.csv`

### 4.2 解析プロット

- `results/shift_current/peak_amplitude_vs_delta.png`: x=δ, y=peak |σ_zzz|, 9 材料 line plot
- `results/shift_current/peak_position_vs_Eg.png`: x=Eg, y=peak ω (確認: gap 近傍に出ているか)
- `results/shift_current/material_grid.png`: 3×3 (B-cation × halide) のヒートマップ、δ=0.10 Å 固定

### 4.3 期待される科学的知見

- Sn/Ge 系（SOC 小・Eg 小）で σ_zzz が Pb 系より **大きい** 可能性（Tan & Rappe 2016 が halide で Eg と shift current の trade-off を示唆）
- これが novel な知見になるか、§5 で議論

### 4.4 報告書

`cowork/reports/theme_F_shift_current.md` を F5 完了後に作成（既存 reports/ テンプレ準拠）。Theme A 報告書（既存）と同じ章立てで：
1. 動機・背景
2. 公式と実装
3. 検証（F4 の 3 種類）
4. 結果（F5 スキャン）
5. 議論 — Sn/Ge の優位性 / 限界（Blount intra-atomic 抜け）
6. 既存研究との差分・新規性
7. 引用 PDF リスト

---

## 5. ハルシネーション防止上の補足

F4 実装時の必須ルール（既存 0 節準拠の再強調）:

1. **F4-1 で commit するときは「sign / prefactor 確定」と書かない**。"length-velocity equivalence verified (peak position + sign consistent)" 程度に留める。Aversa-Sipe 一次照合は依然 missing
2. **F4-2 で Tan & Rappe 値を読み取ったら、PDF page 番号と Figure 番号を docstring に明記**（例: `# Compared with Tan & Rappe 2016 (DOI:10.1038/npjcompumats.2016.26) Fig.2(b), peak at ~2.6 eV`）
3. **F5 で 9 材料の数値を出すときは、F4 で確定した符号規約に従う**。F4 完了前に F5 着手しない
4. **絶対振幅は Blount-1962 TB intra-atomic 抜けで過小**。これを Theme F 報告書で必ず限界として明示（既に shift_current.py docstring にあり）

---

## 6. ユーザー通知（並行）

私（Cowork 監督）からユーザー（Teruhisa さん）に以下を通知します:

> Theme F の F3 (shift current sum-over-states) が完了、δ=0 vanishing を 1e-15 で達成。F4 検証段階に入りますが、**Aversa-Sipe 1995 PRB 52, 14636 PDF** の機関アクセス取得をお願いしたいです（APS は Cloudflare 障壁で自動取得不可、購読壁あり）。これがあれば符号・prefactor 確定の primary source 照合ができます。無くても F4-1/2/3 の三重検証で確定は可能なので、研究の進行は止めません。

---

## 7. まとめ

| 項目 | 判定 |
|---|---|
| F3 構造（sum-over-states 公式の相対構造） | ✅ δ=0 vanishing で decisive 検証 |
| Kramers 縮退の扱い（deg_tol スキップ） | ✅ 適切 |
| 旧 Abelian の `_deprecated` 残置 | ✅ 回帰比較可 |
| docstring 出典 + VALIDATION STATUS 明記 | ✅ 規律順守 |
| 絶対符号 / prefactor | ⏳ F4 で確定 |
| Aversa-Sipe 1995 一次照合 | ❌ Cowork 取得不可、ユーザー機関アクセス依頼中 |
| 次のアクション | F4-1 (length-gauge) → F4-2 (Tan&Rappe 照合) → F4-3 (SSH) → F5 (9 材料) |

順調です。F4 着手して構いません。質問があれば `cowork/progress/` に投げてください。

—Cowork supervisor
