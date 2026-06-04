# 新規性アセスメント（2026-05-23）

**目的:** 提案した研究テーマの本当の新規性を検証し、必要なら方向修正する。

**方法:** Web 検索（Bing/Google）で関連キーワードを叩き、2025-2026 の最新動向と既存リポ 49 本の隙間を確認。

---

## Theme A — CsBX₃ 9 材料の Landé g 因子 系統マップ

### 新規性判定: ✅ 強い（推奨）

**先行論文（カバー範囲）:**
- **Kirstein 2022 Nat. Commun.** (2112.15384) — Pb 系のみ、g(Eg) 普遍関係
- **Nestoklon 2023 J. Phys. Chem. Lett.** (2305.10586) — Pb ナノ結晶
- **2025 Nanoscale** "Landé g-factors in CsPbI₃ NCs in glass" — Pb のみ、量子閉じ込め強い場合の renormalization
- **Kopteva 2026** (2605.15807) — 2D RP, Pb のみ
- **2024 JPCC** Sn/Ge-substituted 2D Dion-Jacobson (3-AMPY)₄Pb₄I₁₆ — 構造・光学物性のみ、**g 因子は計算していない**

**結論:** 鉛フリー（Sn, Ge）3D 立方ハライドペロブスカイトの体系的 g 因子 TB 計算は **2026-05 時点で存在しない**。

**強い新規ポイント:**
1. Ge/Sn 系 6 材料（実験未測定）の g_e, g_h 第一予測
2. Kirstein 普遍関係（Pb 系）が鉛フリーで成立するかの検証
3. 鉛フリー光学スピン素子の材料ランキング表

→ **方針: 維持。最優先で着手。**

---

## Theme B — Pb-X-Pb ボンド角 → Rashba 分裂の TB スキャン

### 新規性判定: ⚠️ 当初提案のままでは弱い。リフレーミング推奨

**先行論文（深刻な重複）:**
- **Boyer-Richard 2016 JPCL** "Symmetry-Based Tight Binding Modeling of Halide Perovskite Semiconductors" (DOI: 10.1021/acs.jpclett.6b01749) — MAPbI₃ 限定だが **TB + bond angle disparity → Rashba splitting を既に実証**。これがほぼ同じ問題設定
- **arxiv:2308.02481** (2023) "Lone-Pair Stereochemistry Induces Ferroelectric Distortion and the Rashba Effect in Inorganic Halide Perovskites" — CsSnI₃, CsSnBr₃ の lone pair 起源 Rashba を DFT で
- **2022 JPCC** "Understanding Layer-Dependent Stability and Rashba Spin Splitting of 2D α-FABX₃ (B=Ge,Sn,Pb)" — DFT で 9 材料系列カバー
- **2024 ACS Nano** "Tuning Rashba Splitting for Bright Ground-State Excitons in 2D CsPbBr₃ through Structural Distortions" — ボンド角 → Rashba を 2D CsPbBr₃ で

**当初提案の難点:**
- 「CsBX₃ 9 材料 × bond angle TB スキャン」というアイデアは、3D-only ・TB-only に絞っても **Boyer-Richard の方法論の自然な拡張**としか見えない可能性
- 2022 JPCC が DFT で 9 材料カバー済み（α-FA は 2D だが、3D 化への拡張は素直）

**残る新規余地:**
1. **3D 立方+ TB レベル**（既存は MAPbI3 単独 TB か、9 材料 DFT。両方が揃った報告は無さそう）
2. **Spin-LED figure-of-merit (FoM)** — 単に α(θ) を出すのではなく、α と E_g と光学吸収係数を組み合わせた素子設計指標を提案し、9 材料 × bond angle で最適化
3. **lone-pair 強度（Sn が最も強い）と α の系統相関**を TB レベルで定量

リフレーミング案: **「Spin-LED 設計指標による鉛フリー × 歪み × 軌道基底の同時最適化マップ」** ならまだ新規性あり。だが単独テーマとしてはやや弱い。

→ **方針: Theme A の延長として組み込む方向に変更。単独 Phase 2 ではなく、Theme A 完了後の発展研究に格下げ。**

---

## Theme C — Kashikar 9 材料 TB パラメータの ML 内挿で混合 B サイトを予測

### 新規性判定: ✅ そこそこ強い

**先行論文:**
- **HAMSTER 2026 Nat. Commun.** "Physics-informed Hamiltonian learning for large-scale optoelectronic property prediction" — 巨大データ + ML で halide perovskite Hamiltonian を学習
- **HamGNN / DeepH** (2024-2025) — グラフニューラルネット系
- **2024 arxiv:2401.10998** "Leveraging Domain Adaptation for ML Predictions of New Halide Perovskites" — 物性予測の DA
- **2026 Feb MDPI** — CGCNN を含む 11 ML モデルで perovskite 物性予測

**残る新規余地:**
1. **小データ + 軽量 ML（GP やランダムフォレスト）で TB パラメータ内挿** — 既存研究は重い GNN ばかりで、9 材料程度の小データを直接活用する方法論は埋もれている
2. **「TB パラメータの物理整合性」を保つ制約付き回帰**（Slater-Koster の対称性関係を ML に埋め込む）

→ **方針: 維持。Theme A 完了後の Phase 2 候補に昇格（B から差し替え）。**

---

## Theme D — Apergi 2023 chiral CD を Sn/Ge 系へ拡張

### 新規性判定: ✅ 強い

**先行論文:**
- **Apergi 2023** (2309.14002) — Pb 系のみ、ハライド変えると CD どう変わるかは扱っているが、B サイトを Sn/Ge にした計算は無い
- **Liu 2025 Adv. Sci.** "Multifunctional Chiral Halide Perovskites" — レビュー。鉛フリー chiral perovskite の **必要性**を主張するが、TB 計算は提示せず
- **Gaurav 2026 Adv. Mater.** "Chiral Spin-LED" — 実験論文、Pb 系

**残る新規余地:**
1. Sn/Ge chiral perovskite の CD 予測（誰もやっていない、鉛フリー素子設計の鍵）
2. Apergi 方法論の独立な再実装と検証（科学コミュニティへの貢献）

→ **方針: 維持。Theme A 完了後の有力候補。**

---

## Theme E — 2D RP 層数依存 g 因子

### 新規性判定: 🟡 中程度（実験論文 2605.15807 と直接競合）

**先行論文:**
- **Kopteva 2026** (2605.15807) — 実験で 2D RP 層数依存 g 因子を既に測定済み。理論との比較を求めている

**残る新規余地:**
- 実験との照合理論パートとして直接接続できる
- ただし「実験との比較は他のグループも狙うだろう」というレースになる

→ **方針: 保留。実装が重く、競合がある。Theme A→C→D を優先。**

---

## 改訂版優先順位

| 旧 | 新 | テーマ | 新規性 | 実装規模 |
|---|---|---|---|---|
| 1 | **1** | **Theme A: g 因子 9 材料マップ** | ✅ 強 | 中（200-300 行）|
| 2 | **2** | **Theme C: ML 内挿 TB パラメータ** | ✅ 中 | 中（500 行） |
| 3 | **3** | **Theme D: Sn/Ge chiral CD** | ✅ 強 | 中（400-500 行） |
| - | **4** | **Theme A 延長: Spin-LED FoM with bond angle** | 🟡 中 | 大 |
| 5 | **5** | Theme E: 2D RP（実装重い、競合あり） | 🟡 中 | 大 |
| 旧 Theme B | **削除** | 単独テーマとしては不採用、Theme A の延長に統合 | ⚠️ 弱 | — |

---

## 監視継続

このアセスメントは時間とともに陳腐化する。**週 1 回**、Cowork 側の scheduled task で:
- 上記テーマのキーワードで arXiv 新着を再検索
- 重要な新着が出たら本ファイルに追記し、ユーザーに通知
- 必要なら方向転換

最新更新: 2026-05-29
次回確認予定: 2026-06-01

---

## 更新履歴

### 2026-05-23 09:00 — Theme A 報告書（A1-A5）完了後の緊急再確認

**契機:** Claude Code が Theme A 完了し報告書 `reports/theme_A_g_factor.md` を提出。Cowork で念のため再検索。

**追加確認した文献:**
- **arXiv:2511.02956 (Rodina, Semina, Ivchenko, 2025-11)** "Electron and hole g factors in semiconductors and nanostructures (Review)" — 取得して `references/pdfs/` に追加
  - 内容確認: 鉛系ハライドペロブスカイト APbX₃ (A=Cs,MA,FA; X=Cl,Br,I) は扱う
  - **Sn / Ge / 鉛フリーの記述ゼロ**（pdftotext 全文 grep で確認）
  - **CsSnX₃ / CsGeX₃ への言及なし**

**判定:** Theme A の新規性は **2025/11 のレビュー後も堅持**。本研究は鉛フリー g 因子の最初の系統的計算予測。

**主結果の独立検証:**
- Cowork 紙計算で CSV 主要 3 点 (CsPbI₃, CsSnI₃, CsGeI₃) を独立確認 → g_h 計算式と一致
- 物理的考察「Δ→0 で g_h 補正項消滅」は数式から自明に正しい

**次回確認予定:** 2026-05-25（月）自動巡回

---

### 2026-05-25 09:00 — 定期自動巡回（Theme A, C, D, F, G 一括）

**実施:** Cowork scheduled task。arXiv recent 2 ページ + 各テーマ 4 クエリ WebSearch。詳細レポート: `cowork/progress/2026-05-25_0900_novelty_check.md`

**判定サマリ:**

| テーマ | 判定 | 前回比 |
|---|---|---|
| A | ✅ 堅持 | 不変 |
| C | ✅ 堅持 | 不変 |
| D | 🟡 **要注意（格下げ）** | ✅→🟡 |
| F | 🟡 **要注意（新規評価）** | 初判定 |
| G | ✅ 堅持 | 初判定 |

**Theme D 格下げ理由:**
- **arXiv:2511.19753 (2025-11-24)** "Full Minimal Coupling GW-BSE Framework for CD in Solids" 登場。(S-NEA)₂PbBr₄ と (S-MBA)₂PbI₄ に適用。Apergi TB の精度的後継候補
- **Coccia 2024 Angew. Chem.** (ClMBA₂SnI₄) + **MATSUSFall24 nanoGe** (ClMBA₂GeI₄, ClMBA₃GeI₅) で **2D 層状 Sn/Ge chiral perovskite の DFT 計算は既に着手**
- 3D CsSnX₃/CsGeX₃ の lone-pair 起源 chiral 歪みによる CD はまだ未開拓 → **テーマを「3D CsBX₃ lone-pair chiral CD」へリフレーミング推奨**

**Theme F 警告理由:**
- **PMC9833107 (2023)** で **CsGeI₃ shift current** は第一原理レベルで既に計算済み（40 μA/V² in visible）
- **CsPbI₃ 圧力下 shift current** も既報（band inversion との連動）
- ただし **9 材料系統スキャン + lone-pair vs shift current 相関** は未報告 → リフレーミングして進めれば novel

**Theme G 確認内容:**
- **ACS Nano 2026 (5c18264)** で 2D (PEA)₂GeI₄ が **small polaron hopping** を示すと報告。3D CsGeX₃ は未調査
- Frost 2017 / Bouhassoune 2019 の手法を 9 材料に展開する余地は依然大きい

**緊急通知:** なし（⚠️/❌ 該当なし）

**追加収集推奨:** 2511.19753, 2510.24874, 2508.04861（arXiv）+ PMC9833107（OA）+ Coccia 2024 + ACS Nano 2026（要検討）

**次回確認予定:** 2026-05-28（木）09:00 自動巡回

---

### 2026-05-29 09:00 — 定期自動巡回（Theme A, C, D, F, G 一括）

**実施:** Cowork scheduled task。arXiv recent 2 ページ + 各テーマ 4 クエリ WebSearch。詳細レポート: `cowork/progress/2026-05-29_0900_novelty_check.md`

**判定サマリ:**

| テーマ | 判定 | 前回比 |
|---|---|---|
| A | ✅ 堅持 | 不変 |
| C | ✅ 堅持 | 不変 |
| D | 🟡 要注意 | 不変（🟡 維持） |
| F | 🟡 要注意 | 不変（🟡 維持） |
| G | ✅ 堅持 | 不変 |

**Theme D 補強情報:**
- **arXiv:2401.07978 (Berquist 2024 JACS)** "Noncollinear Electric Dipoles in a Polar Chiral Phase of CsSnBr₃" — CsSnBr₃ Phase II は ferroaxial（カイラル）相。SHG は観測済み、**CD 計算は未実施**。3D Sn 系の chiral CD は構造的下地が固まっており、Apergi TB 適用論文が出る前に着手する緊急度が上昇

**Theme G 補強情報:**
- **arXiv:2505.20092 (Phys. Rev. B 2025-05)** "Impact of anharmonicity on CsSnBr₃ carrier mobility" — TDEP + ab initio BTE で CsSnBr₃ 単体の μ_e/μ_h を計算。**9 材料スキャンではないが、9 材料拡張版が登場する可能性あり**。着手は早めが望ましい
- **PMC11173484 (2024)** 9 材料 CsBX₃ の DFT bands/defects 系統スキャンが既存だが mobility は未計算 → Theme G と棲み分け可能

**Theme A 補強情報:**
- **Adv. Funct. Mater. 2026 (Nikiforov, 2D PEPI Rydberg g-factor)** — 2D Pb のみ、3D 9 材料 Sn/Ge は依然空白
- **arXiv:2604.28081 (Ge/SiGe QD g-tensor optimization, 2026-04)** — 半導体 Ge 量子ドット、ハライドペロブスカイトではないが手法的関連

**緊急通知:** なし（⚠️/❌ 該当なし）

**次回確認予定:** 2026-06-01（月）09:00 JST 自動巡回

---

### 2026-06-01 09:00 — 定期自動巡回（Theme A, C, D, F, G 一括）

**実施:** Cowork scheduled task。arXiv recent 2 ページ（100 件）+ 各テーマ 4 クエリ WebSearch。詳細レポート: `cowork/progress/2026-06-01_0900_novelty_check.md`

**判定サマリ:**

| テーマ | 判定 | 前回比 |
|---|---|---|
| A | ✅ 堅持 | 不変 |
| C | ✅ 堅持 | 不変 |
| D | 🟡 要注意 | 不変 |
| F | 🟡 要注意 | 不変 |
| **G** | **🟡 要注意（降格）** | **✅→🟡** |

**Theme G 降格の理由（重要）:**

**JPCL 2026** "Exploring the Polaron Landscape in Germanium Halide Perovskites: CsGeCl₃, CsGeBr₃, CsGeI₃" (DOI: 10.1021/acs.jpclett.5c02516, PMC12908147) が登場。**3D CsGeX₃ 3 材料の polaron 系統計算がすでに発表済み**。

- Pb 系（Frost 2017 等）+ Sn 系（arXiv:2505.20092 で CsSnBr₃ 単独）+ Ge 系（JPCL 2026 で 3 材料）が個別には埋まり始めている
- ただし **9 材料一貫 + TB / Slater-Koster ベース + 一貫した手法での Pb/Sn/Ge 比較** はまだ未報告
- Theme G を素朴に「9 材料 polaron mobility 計算」とすると Ge セクションが scoop されてしまう

**推奨リフレーミング:**
- 「**TB ベース 9 材料一貫 Fröhlich coupling + bandgap-mobility-effective mass 系統相関**」へ
- 既存 Pb/Ge の独立研究との接続・差別化を明確化
- JPCL 2026 を取得して手法詳細を確認、TB ベースとの比較余地を見極めることが必須

**Theme D / F 状況:**
- D: 新たな脅威論文なし。ChemPhysChem 2025 / JACS 2025 は Pb/Bi 中心、Sn/Ge は未着手のまま
- F: NbOBr₂ shift current（Nat. Commun. 2025）は登場したが対象がペロブスカイトでない。9 材料 CsBX₃ TB スキャンは依然空白

**Theme A / C 状況:**
- A: g 因子 TB は Pb 系のみ。鉛フリー系統計算は依然ゼロ。Phase 1 最優先継続
- C: TB パラメータ自体の ML 内挿は依然未開拓。arXiv:2602.06893 (Cs₂KInI₆ symmetry) は二重ペロ DFT で重複なし

**緊急通知:** あり（Theme G リフレーミング推奨）。⚠️/❌ レベルの scoop ではない

**追加収集推奨（🔴 高優先）:**
- JPCL 2026 acs.jpclett.5c02516 (Ge 3 材料 polaron landscape) — Theme G 判断のため必須

**次回確認予定:** 2026-06-04（木）09:00 JST 自動巡回
