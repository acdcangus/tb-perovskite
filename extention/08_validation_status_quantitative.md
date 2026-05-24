# 定量的検証ステータス — tb-perovskite 実装報告書のレビュー

**作成日**: 2026-05-24
**目的**: ユーザの問い「全部論文の結果と検算はできてるの？定量的に論文の何と何パーセントの違いか、みたいなのもちゃんとみたい」に答えるため、`C:\Users\kteru\tb-perovskite\extention\08_tb-perovskite_implementation_report.md` の各機能の検証状況を「論文値との定量比較」の観点で仕分けし、ギャップと追加すべき検証項目を明示する。
**対象**: tb-perovskite F1–F14 のうち実装済み 12 機能
**結論**: **真に「論文の具体数値を % で比較」できているのは F6 polaron のみ**。他の機能は解析解・対称性・位相量子化等での「内部整合性アンカー」に留まる。これは SK-TB + Blount caveat（速度演算子に共有結合補正がない）に起因する **構造的な制約** で、実装エージェントは honest に明記している。

---

## 1. 仕分けカテゴリ

| カテゴリ | 意味 |
|---|---|
| **A** | 論文の具体的数値と % で比較済み（最も理想的）|
| **B** | 解析解・厳密則・位相量子化・対称性極限と機械精度〜許容誤差で一致（**内部アンカー**）|
| **C** | 既知の定性挙動（符号、消失、線形性等）のみ確認、定量比較なし |
| **D** | 絶対値を**意図的に未検証**（SK-TB/Blount caveat により絶対値信頼性に限界）|

---

## 2. 機能別 定量検証ステータス

### F1 Berry 曲率コア → AHC / SHC

| 検証項目 | カテゴリ | 比較対象 | 結果 |
|---|---|---|---|
| 質量 Dirac 下バンド Ω₋ = +m/(2(k²+m²)^{3/2}) | B | Xiao-Chang-Niu RMP 82, 1959 Eq.(1.13) を自前で再導出 | 解析解と機械精度一致 |
| QWZ 模型の整数 Chern + 相図 | B | Qi-Wu-Zhang PRB 74, 085308 の既知相図 | 一致（整数値）|
| Kubo ↔ Fukui-Hatsugai-Suzuki 一致 | B | 2 独立手法（連続 vs 離散）| 機械精度 |
| 立方 CsBX₃ で AHC = 0 | B | P·T 対称性予測 | **~1e-15**（機械精度）|
| **AHC 絶対値 (e.g., MAPbI₃ の AHC = ? S/cm)** | **D** | **論文値なし／実装エージェントが未検証宣言** | **未比較** |
| **SHC 絶対値** | **D** | **in-repo ベンチマーク材料なく未検証宣言**＋ Blount caveat | **未比較** |

### F2 Wilson ループ / WCC

| 検証項目 | カテゴリ | 比較対象 | 結果 |
|---|---|---|---|
| Wilson Chern == Fukui plaquette Chern (QWZ) | B | 2 独立手法一致 | 整数値一致 |
| Wilson 行列 unitary 性 | B | 数値線形代数の理論 | 機械精度 |
| 分極位相 gauge 不変性 | B | KSV 理論 | 数値で確認 |
| **既知材料（HgTe/CdTe, Bi₂Se₃ 等）の Z₂ 値再現** | — | 未実装（Z₂ parity は §4 で意図的未実装）| **N/A** |

### F4 Rashba スピン分裂

| 検証項目 | カテゴリ | 比較対象 | 結果 |
|---|---|---|---|
| 解析 2 バンド Rashba 模型 α_R 厳密回復 | B | Bychkov-Rashba JETP Lett. 39, 78 解析式 | 機械精度一致 |
| スピン ⊥ k | B | Rashba 理論予測 | 確認 |
| 立方 CsBX₃ → 分裂 0 | B | Kramers 縮退理論 | 確認 |
| 極性 (P4mm) → 分裂発生、Γ で消失、|k| で増大 | C | 定性挙動のみ | 確認（数値ではない）|
| **α_R 絶対値 (e.g., MAPbBr₃ の α_R ≈ 11 eVÅ) 再現** | **D** | **Niesner 2016 PRL 117, 126401** は **表面 Rashba** 測定値で、本実装は **バルク極性相** → 直接比較不能と honest 宣言 | **未比較**（構造的）|

### F11 Edelstein 効果

| 検証項目 | カテゴリ | 比較対象 | 結果 |
|---|---|---|---|
| 中心反転（非縮退）模型 → χ = 0 | B | 対称性予測 | 確認 |
| Rashba 模型 → χ_yx ≠ 0, χ_xx ≪ χ_yx | C | Edelstein 1990 の予測（直交応答）| 定性確認 |
| χ_yx(−α) = −χ_yx(α) | B | パリティ性質 | 確認 |
| **χ 絶対値** | **D** | **τ 依存のため絶対値はスコープ外と honest 宣言** | **未比較** |

### F7 CPGE / Injection current

| 検証項目 | カテゴリ | 比較対象 | 結果 |
|---|---|---|---|
| de Juan 式簡約: −Im(ε_jkl r^k r^l) = Ω^j | B | de Juan-Grushin-Morimoto-Moore NC 8, 15995 一般式 | 解析的に一致 |
| 中心反転対称→ CPGE = 0 | B | 対称性 | 確認 |
| Weyl 量子化: Tr[β] が ω 非依存プラトー | B | 位相量子化 | 確認 |
| Weyl chirality 符号反転 | B | 理論予測 | 確認 |
| **|Tr| ≈ πe³/h² = 1/4π を 20% で数値再現** | **A**（部分）| **de Juan 2017 の universal value** | **20% deviation**（許容範囲だが精度限定）|
| **絶対値（具体的材料）** | **D** | **Berry 曲率規約 + Blount caveat により未検証** | **未比較** |

### F6 Fröhlich ポーラロン結合 ★★ 最も成功している例

| 検証項目 | カテゴリ | 比較対象 | 結果 |
|---|---|---|---|
| **MAPbI₃ 電子 α = 2.39 再現** | **A** | **Frost PRB 96, 195202 (2017)** | **<1% 誤差** |
| **MAPbI₃ 正孔 α = 2.68 再現** | **A** | **Frost PRB 96, 195202 (2017)** | **<1% 誤差** |
| **CsPbBr₃ α ≈ 2 再現** | **A** | **Sendner Nat. Commun. 12, 4945 (2021)** ε∞=4.8, ε_S=20.5, LO=19.2 meV, m*=0.22 | **再現**（具体的%は報告書に未記載、要確認） |
| 先頭次質量補正 1 + α/6 | B | Fröhlich 弱結合解析式 | 確認 |
| **9 材料 α マップ（CsPbX₃ 系等）** | **C** | 部分実装、CsPbBr₃ のみ ε_S/ω_LO 収集済 | 一部未完 |

### F9 Boltzmann 熱電輸送 (CRTA)

| 検証項目 | カテゴリ | 比較対象 | 結果 |
|---|---|---|---|
| **Wiedemann-Franz Lorenz 数 → π²/3 (k_B/e)²** | **A** | **普遍定数（バンド非依存厳密則）** | **rtol 0.5%** |
| Sommerfeld Seebeck（縮退極限）| B | Sommerfeld 展開 | 確認 |
| 正孔 S > 0 | C | 物理常識 | 確認 |
| Σ ∝ ε^{3/2} | B | 自由電子 DOS | 確認 |
| **絶対 σ / κ_e** | **D** | **τ (材料・散乱依存)** | **未実装宣言** |
| **絶対 Seebeck (e.g., CsPbI₃ S = ? μV/K)** | **D** | 同上 | **未比較** |

### F12 歪みバンド工学

| 検証項目 | カテゴリ | 比較対象 | 結果 |
|---|---|---|---|
| Harrison 則 t_* (1+ε)⁻² | B | Harrison 1980 教科書スケーリング | 数値で確認 |
| ε = 0 で無歪みギャップ（CsPbI₃ 0.6298 eV）回復 | B | 自己整合性 | 確認 |
| 線形性、引張/圧縮逆符号 | C | 定性 | 確認 |
| **変形ポテンシャル a_g 絶対値** | **D** | **SK-TB + Harrison は推定**、**Buin 2014 / Grumet 2018 の DFT/実験値との定量一致は非主張**と honest 宣言 | **未比較** |
| **dE_g/dε（実験値: e.g., MAPbI₃ で ~50 meV/%）再現** | — | 未検証 | **未比較**（追加検証余地あり）|

### F5+F13+F14-A スラブ / 超格子 / Stark スラブ

| 検証項目 | カテゴリ | 比較対象 | 結果 |
|---|---|---|---|
| 層ブロック再構成 H∥ + Te^{ik_z a} + h.c. == 3D H | B | 厳密同値性 | **機械精度** |
| 周期スタック == 3D バンド | B | Bloch-Floquet 理論 | k_z = 2πm/(Na) で一致 |
| ミニバンド崩壊 (inter-layer → 0) | B | 弱結合極限 | 確認 |
| open スラブのギャップ厚み収束 | B | 自己整合性 | 確認 |
| Stark: E=0 回復 + 幅 ~eE(N−1)a | B | Wannier-Stark 理論 | 確認 |
| **E_g(n) 絶対値（Blancon 2017 Science 355, 1288 実験値: n=1: ~2.4 eV, n=2: ~2.2 eV, ...）と比較** | — | **未比較**（実装報告は honest に「絶対値は SK-TB caveat」と宣言）| **追加検証余地あり** |
| **2D RP スペーサ厚 hard barrier 理想化** | D | Even 2014 ChemPhysChem 15, 3733 — 物理的限界 | 限界として明記 |

### F14-B Berry 位相分極 (KSV)

| 検証項目 | カテゴリ | 比較対象 | 結果 |
|---|---|---|---|
| **SSH Zak 位相 0/π 量子化** | **B** | **SSH 1979 PRL 42, 1698 の厳密値** | **厳密一致（位相量子化）** |
| 位相転移で π ジャンプ | B | SSH 理論 | 確認 |
| Rice-Mele（反転破れ）→ 連続シフト | B | Rice-Mele 1982 | 確認 |
| **ペロブスカイトの分極絶対値** | **D** | **電子寄与のみ計算（イオン寄与なし）と honest 宣言**、total polarization のみ gauge 不変 | **未比較**（用途は ΔP のみ）|

---

## 3. 全体サマリ（定量検証マトリックス）

| 機能 | A: 論文%比較 | B: 解析/位相 | C: 定性のみ | D: 意図的未検証 |
|---|---|---|---|---|
| F1 Berry/AHC/SHC | — | 4 項目 | — | AHC/SHC 絶対値 |
| F2 Wilson/WCC | — | 3 項目 | — | Z₂ parity（未実装）|
| F4 Rashba | — | 3 項目 | 1 項目 | α_R 絶対値 |
| F11 Edelstein | — | 2 項目 | 1 項目 | χ 絶対値 |
| F7 CPGE | **Weyl 20%** | 4 項目 | — | 材料絶対値 |
| **F6 polaron** | **MAPbI₃ <1%, CsPbBr₃ 再現** | 1 項目 | 部分実装 | — |
| F9 thermoelectric | **WF 0.5%** | 3 項目 | 1 項目 | 絶対 σ/κ/S |
| F12 strain | — | 2 項目 | 1 項目 | a_g 絶対値, dE/dε |
| F5+F13+F14-A | — | 5 項目 | — | E_g(n) 絶対値 |
| F14-B 分極 | — | 3 項目 | — | 絶対分極 |

**集計**：
- 真の「論文値 % 比較」**A** に到達: **F6 polaron（最重要例, <1%）, F9 WF (0.5%), F7 Weyl quant (20%)**
- 内部アンカー **B** での厳密検証: 全機能で複数項目
- 絶対値 **D**: ほとんどの機能で意図的未検証（SK-TB/Blount caveat）

---

## 4. なぜ多くの機能で「論文値の絶対値 % 比較」が無いのか

実装エージェントが honest に明記する **構造的理由**：

1. **SK-TB (Slater-Koster Tight-Binding) の Blount caveat**
   - 速度演算子 v = ∂H/∂k に共有結合（covalency）補正がないため、輸送・光学応答の **絶対値はモデル系統誤差** を含む。
   - 結果として AHC, SHC, α_R, CPGE, Edelstein 等の **絶対値は信頼区間が不明**。

2. **対応戦略（honest）**
   - **対称性**：消失（cubic で 0）、符号、選択則の一致を厳密に確認 → **B / C カテゴリ**
   - **位相量子化**：Chern（整数）, Zak（0/π）, Weyl（普遍値）→ **B カテゴリ**
   - **解析模型**：QWZ, Rashba, SSH, Rice-Mele, 質量 Dirac → **B カテゴリ**
   - **絶対値が信頼できる量のみ**を **A** に: ポーラロン α（Fröhlich は SK-TB の弱点に影響されない）, Wiedemann-Franz（普遍定数）, Weyl quantization（位相量子化）

3. **これは「捏造」ではない**：報告書 §3.3 で明示：
   > 検証アンカーが立たない量（SHC/Rashba/Edelstein/CPGE/分極の絶対値）は **未検証であることを honest に明記** し、対称性・構造・相対トレンド・量子化のみを信頼する立場

---

## 5. 追加で実施可能な定量比較（提案）

仕様 §「論文 figure/table 再現テスト」の要件をより厳格に満たすため、以下を実装エージェントに追加要請する余地がある：

### 5.1 即実施可能（既存ベンチマーク文献あり）

| 機能 | 追加検証 | 出典文献 | 期待される deviation |
|---|---|---|---|
| **F12 strain** | dE_g/dε（一軸/静水圧）の符号と大きさ比較 | Buin 2014 / Grumet 2018 DFT 値（MAPbI₃ で ~30-50 meV/%）| 範囲一致レベル（SK-TB 推定値で 30% 程度の許容を予想）|
| **F5 (n=1,2,3,4 layered RP)** | E_g(n) の実験値再現 | **Blancon 2017 Science 355, 1288** Fig. 2 — (BA)₂(MA)_{n-1}Pb_nI_{3n+1} で n=1: 2.43 eV, n=2: 2.16 eV, n=3: 2.03 eV | 絶対値は SK-TB caveat だが **減衰トレンド** は数値で比較可能 |
| **F6 polaron** | 9 材料 α マップ完成 + CsPbBr₃ の <1% 数値明記 | Sendner 2021 Nat. Commun. 12, 4945 / Frost 2017 PRB 96, 195202 | 既に部分実装、残り材料の ε_S/ω_LO 収集が必要 |

### 5.2 中期的に検討（既存実装の拡張要）

| 機能 | 追加検証 | 出典 | 備考 |
|---|---|---|---|
| F4 Rashba | バルク極性相 α_R を DFT 値と比較 | Niesner 2016 表面測定とは異なる比較対象が必要 | 適切な文献選定要 |
| F1 AHC | trivial vs topological 相の差 | ペロブスカイトでは小さい（量的に検証困難）| 模型材料での再現性を担保 |
| F14-B 分極 | 強誘電ペロブスカイトでの ΔP（gauge 不変）| Frohna 2018 等 | 電子寄与のみで意味のある量 |

### 5.3 構造的に困難（D カテゴリ）

これらは SK-TB の本質的限界。**改善には GW or DFT スターターハミルトニアン**が必要：

- F1 SHC 絶対値, F4 α_R 絶対値（表面）, F11 χ 絶対値, F7 材料絶対値, F14-B 絶対分極

---

## 6. 結論と推奨

### 6.1 現状評価

- **F6 polaron** は **真の論文値定量比較を含む唯一の機能**（MAPbI₃ Frost α を <1% で再現）
- **F9 (WF), F7 (Weyl quantization)** は **普遍定数 / 位相量子化** との比較で 0.5%, 20% 達成
- **他の機能**は **論文の Fig./Table の絶対値再現** には到達していない。ただしこれは捏造ではなく、SK-TB の構造的限界を honest に開示した結果である

### 6.2 仕様書「論文品質」基準への適合度

仕様書 `00_README.md` §4 の Acceptance 基準：

| 基準 | 達成度 |
|---|---|
| A. 検証可能性（解析解一致）| **○ 全機能で達成** |
| A. 収束テスト | **○ 達成** |
| A. 文献結果の再現テスト | **△ F6 polaron のみ厳密、他は内部アンカー** |
| B. 妥当性（実験/DFT との比較）| **△ F6 のみ**、他は構造的に困難 |
| C. 新規性 | **○ Berry 統合インフラ、Z₂、CPGE、polaron は新規** |

### 6.3 ユーザ選択（2026-05-24 確定）

ユーザ指示「**追加機能は全部やりたいね**」（2026-05-24）に基づき：

- **§5.1 (Tier-1) 全件着手**: F5 Blancon n 依存, F12 Buin/Grumet dE/dε, F6 9 材料 α
- **§5.2 (Tier-2) 全件着手**: F4 バルク Rashba DFT, F1 AHC 3D 模型 + F2 Z₂ parity 完成, F14-B 強誘電 ΔP, F11 χ/σ 比
- **§5.3 (Tier-3) は構造的限界**: SK-TB / Blount caveat 由来のため、本タスクのスコープ外（GW/DFT 連携の別仕様で対応）

実装エージェントへの具体指示は **`09_additional_validation_tasks.md`** に整理した（Tier-1 / Tier-2 各タスクの文献・Acceptance・工数・作業フロー）。

想定総工数: **9–13 週**（既存実装 + 既存 314 テスト不変、追加テスト想定 30–50）。

---

**注**: 本ドキュメントは tb-perovskite 実装報告（`C:\Users\kteru\tb-perovskite\extention\08_tb-perovskite_implementation_report.md`）の **§1 V&V 記述を批判的にレビューし、論文値との定量比較の有無を仕分けたもの**。実装エージェントの honest な未検証宣言を尊重しつつ、Acceptance 基準（仕様書 §4-B 妥当性）に対するギャップを明示する。

---

## 7. 追加検証タスク（09）実施結果 — 2026-05-24（Claude Code）

`09_additional_validation_tasks.md` の Tier-1/Tier-2 を **全 7 件着手・完了**。ユーザ追加制約「**追加機能はコア TB のエネルギー・波動関数で計算**（論文値は検算用）」を全件で順守。テスト 314→**330**（全 pass）。**新規参照文献の DOI は全件 web/crossref で事前検証**し、**誤引用を 4 件訂正**（下記）。

### 7.1 達成カテゴリ（honest）

| タスク | 機能 | コア TB 由来 | 達成カテゴリ | 要点 |
|---|---|---|---|---|
| T1-1 | F5 閉じ込め E_g(n) | slab (CsPbI₃) | **C→B** | 減衰指数 p_TB≈0.93 vs Blancon 自由粒子 p_exp≈0.85 → 15%以内（トレンド限定; 材料差+SK-TB で絶対値は非主張）|
| T1-2 | F12 歪み dE_g/dε | bandengr | **C（符号）/ D（絶対）** | 符号一致（加圧で gap 減; 実験 Pieniazek 2023 と一致）。大きさは TB が ~5–16× 過大（tilting 欠如）|
| T1-3 | F6 polaron α | TB m\*（全9材料）| **A（公式）/ B** | TB R 点 m\* で α 算出。CsPbBr₃ α_TB=1.66 vs 文献 2.0（差は質量比 √(0.151/0.22) で説明）。9材料マップは Cs 系誘電データ非存在で部分（捏造回避）|
| T2-1 | F4 Rashba α_R | polar TB | **C（順序）/ D（絶対）** | CBM>VBM 順序は DFT(CsPbF₃)一致。絶対値は ~40× 過小（剛体変位+Blount）|
| T2-2 | F1/F2 Z₂ parity | （手法）| **B** | Fu-Kane parity 実装、Wilson-Dirac で相図再現。「未実装」解消。実ペロブスカイト適用は反転演算子未確定で保留 |
| T2-3 | F14-B ΔP | polar TB | **C→B** | 電子 ΔP が FE 符号反転、~1–8 μC/cm²（DFT FE と同オーダ）。電子寄与のみ（ionic 別）|
| T2-4 | F11 χ/σ 比 | polar TB + Rashba | **B** | τ 非依存効率 χ_yx/σ_xx を 2D Rashba 解析値 mα/(4μ) と 15%以内一致。ペロブスカイト効率は TB 予測 |

### 7.2 引用訂正（ハルシネーション点検; no-hallucination）

1. **Blancon「Scaling law」**: 09 の「Science 355,1288 (2017)/10.1126/science.aal4211」は **edge-states 論文との取り違え**。正しくは **Nat. Commun. 9, 2254 (2018)**。
2. **Buin 2014 (Nano Lett. 14, 6281)**: 内容は **trap-free 合成**で歪み dE_g/dε とは無関係 → 削除。
3. **Grumet PRB 98, 155143 (2018)**: crossref で **"Fully self-consistent GW calculations"** と確認＝ペロブスカイト歪みと無関係 → 削除。代替に **Pieniazek 2023 (JPCL 14, 6470)** + **Liu 2023 (Molecules 28, 7643, B)** を採用。
4. **Sendner 2018 Mater. Horiz. 5,118**: 標準の Sendner 光フォノン論文は **Mater. Horiz. 3, 613 (2016)** で **MA 系**（Cs 系無機は非カバー）。

### 7.3 結論の更新

- **真の A（論文値%比較）**は依然 F6 polaron（公式 <1%）と F9 WF（0.5%）が中心。追加で **T1-3 が TB-駆動 α** を加えた。
- 多くは **SK-TB/Blount の構造的限界**により **符号・順序・トレンド・量子化・τ非依存比**での検証（B/C）に留まり、絶対値は honest に D を維持——これは 09 の楽観的「全 A 化」想定に対する**誠実な現実**であり、捏造を避けた結果。
- 新規導入の検証可能インフラ: `bandstructure.effective_mass`（TB m\*）, `bandengr.pressure_coefficient`, `topology.z2_invariant_from_parities`/`parity_delta_at_trim`, `edelstein.longitudinal_conductivity`/`edelstein_ratio`, `polarization.ferroelectric_polarization_difference`。

詳細・式・図は `docs/numerical-methods.md`（§10/§12/§13/§15/§16/§17）と各 `data/parameters/*_benchmark.json`、`results/figures/blancon_E_g_n.png`、`results/tb_effective_masses.json` を参照。

**(EOF)**
