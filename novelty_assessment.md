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

最新更新: 2026-05-23
次回確認予定: 2026-05-30
