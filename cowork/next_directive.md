# Next Directive — Claude Code 向け作業指示（更新版 v3 - 夜間自走モード）

**発行日:** 2026-05-23 08:15（v3 で 14:40 に PI 不在中の長時間タスクキュー追加）
**発行元:** Cowork（監督役）
**PI 状態:** 2026-05-23 14:40 から約 10 時間 不在（睡眠中）。Cowork supervisor は 1 時間に 1 回巡回。
**Claude Code への期待:** 起床後の PI が kick したら、以下の **10+ 時間分のタスクキュー** を順次自走で消化してほしい

---

## 🌙 PI 不在中の作業優先順位（最重要）

PI が起きるまでに、以下を可能な限り進めてください。**順序通り**ですが、ブロックされたら次に進んで OK：

### 優先 1: Theme F F4 — CsPbI3 で Tan & Rappe 2015 ベンチマーク

**目的:** Theme F shift current の絶対符号・絶対値を確定する

**手順:**
1. `references/pdfs/arxiv_1508.03564.pdf` (Tan & Rappe 2015) を pdftotext で読み、CsPbI3 の以下を抽出：
   - 計算条件（圧力範囲、相、k グリッド、smearing）
   - σ_BPVE(ω) の数値・ピーク位置・符号・グラフのスケール
2. `references/pdfs/doi_10.1103_PhysRevB.53.10751.pdf` (Hughes-Sipe 1996) で χ^(2) 公式の前因子を再確認
3. `references/pdfs/doi_10.1038_npjcompumats.2016.26.pdf` (Tan & Rappe 2016 review) で BPVE の現代的レビュー視点を確認
4. **Production モード**で CsPbI3 の shift current を本研究の TB sum-over-states で計算
   - 内部歪み δ を Tan & Rappe 2015 の圧力範囲に合わせる
   - 収束確認 3 段階（k グリッド 8³→16³→24³、η 0.10→0.05→0.025 eV）
   - `results/production/theme_F_shift_current/2026-05-23_<hash>/` に全データ + MANIFEST.json
5. **比較:**
   - スペクトル形状（ピーク位置、形）
   - 符号（同じ or 反転）
   - 絶対値オーダー
6. **符号・前因子の確定**を `docs/shift-current-formulation.md` に記載
7. `cowork/progress/.../F4_complete.md` で Cowork に通知

### 優先 2: Theme F F5 — 9 材料 × δ スキャン（Production モード）

**目的:** 鉛フリー (Sn/Ge) で強い BPVE 材料があるかを示す

**手順:**
1. `shift_current.py` のベクトル化最適化（einsum 化、F3 で 100s かかっていたものを 10s 以下に）
2. 9 材料 × δ ∈ {0.05, 0.10, 0.15, 0.20} で σ_zzz(ω) を計算
3. Production モード（収束 + MANIFEST）
4. `results/production/theme_F_shift_current_9material/2026-05-23_<hash>/`
5. 比較プロット（9 材料の σ_max vs Eg, vs B サイト など）
6. 鉛フリー優位な材料候補ランキング

### 優先 3: Theme A・Phase 1.5 の遡及 Production 化

PI からの指示通り（`PRODUCTION_RULES.md`）:
1. `results/g_factors/` の既存結果を `results/production/theme_A_g_factor/2026-05-23_<hash>/` にコピー
2. MANIFEST.json 作成（key_numbers に CsPbI3/CsSnI3/CsGeI3 の g_e, g_h）
3. 入力 JSON + cli.txt + git_info.txt + env.yml を `inputs/` に
4. 同様に `results/optical/` を `results/production/phase_1.5_optical/2026-05-23_<hash>/`
5. 既存 reports の数値表に MANIFEST 参照を追記

### 優先 4: Theme A 報告書の論文化磨き

`cowork/reports/theme_A_g_factor.md` を **公開クオリティ** に仕上げる：

1. **歴史的引用の系譜を Introduction に明記:**
   - Roth 1960 (PR 118, 1534, in `references/pdfs/classic_Roth1960_PR118_1534.pdf`) - g因子 k·p 原典 (Ge, Si)
   - Kane 1957 (要 D ドライブからコピー、`cowork/progress/2026-05-23_1410_directive_update.md` 参照) - k·p 原典
   - Yafet 1963 - g因子拡張（要追加調査）
   - Boyer-Richard 2016 (in `references/pdfs/doi_10.1021_acs.jpclett.6b01749_BoyerRichard2016.pdf`) - MAPbI3 symmetry-based TB 原典
   - Kirstein 2022 (in collection) - Pb halide perovskite で普遍関係発見
   - Nestoklon 2023 (in collection) - TB から確認
   - **本研究 (Sn/Ge halide perovskite で普遍関係破れ)**

2. **Figure 1-3 の本格化:**
   - Fig.1: 9 材料の g_e と g_h を Eg の関数として、Pb 普遍曲線重畳
   - Fig.2: g_h deviation vs Δ (材料別)
   - Fig.3: g テンソル等方性（Roth-Lax 数値、立方等方性確認）
   - PDF として results/production/theme_A_g_factor/figures/ に保存

3. **Discussion 強化:**
   - Blount 1962 / Roth-Lax 1959 の TB 不完全性議論
   - g_e 「見かけ普遍性」（P が ~40% 変動）
   - g_h 「真の普遍性破れ」（Δ→0 で g_h→+2）
   - 磁気光学（Faraday rotation）実験への含意

4. **References 整理:**
   - 全ての引用を BibTeX 形式で `cowork/reports/theme_A_g_factor.bib` に作成

### 優先 5: D ドライブの古典原典 16 本のコピー

`cowork/progress/2026-05-23_1410_directive_update.md` の通り、Windows `copy` コマンドで以下を `references/pdfs/` に。タイトル検証必須。

- Kane 1957 (parts 1, 2), Kane 1963
- Vogl 1983
- Luttinger 1955, 1956
- Wannier 1937
- Dresselhaus 1955
- Ando 1982 RMP
- Hjarmarson 1980
- Bouckaert 1936
- Cardona 1966, Cohen 1966, Chelikowsky 1974
- Brust 1964
- Kohn 1955 (×2)

### 優先 6: Theme F 報告書 (reports/theme_F_shift_current.md) draft

F4・F5 完了後に draft を書く。Hughes-Sipe 1996 と Tan & Rappe 2015 を方法論の根拠として引用。

### 優先 7: 全体のテスト・品質チェック

- `pytest` 全テスト通過確認（既存 200+ 個、破壊なし）
- `git log --oneline` で commit メッセージが分かりやすいか確認
- `RESULTS.md` の更新（最新の達成状況を反映）

---

### 優先 8: 全部終わったら → `cowork/future_themes.md` の追加テーマへ

PI から「全部終わってたらテーマ追加してね」との指示。優先 1-7 が全て完了したら、`cowork/future_themes.md` の以下を **軽い順**に着手：

1. **Theme I — Exciton binding energy (Wannier-Mott)** ★軽量、すぐ実装可
2. **Theme H — Berry curvature / Hall conductivity** ★velocity op 再利用
3. **Theme J — Circular Photogalvanic Effect (CPGE)** ★Theme F の自然な拡張
4. **Theme L — Carrier mobility (Fröhlich)** 中規模
5. **Theme K — 2D Ruddlesden-Popper g-factor (Kopteva 2026 直接照合)** 重め

各テーマも **Production モード必須**（`PRODUCTION_RULES.md` 準拠）。報告書 `reports/theme_<X>_<name>.md` も忘れずに。

---

## 🤖 PI 不在中の自律判断の原則

- **30 分以上行き詰まったら**: `cowork/progress/.../BLOCKED_<topic>.md` に詳細を書いて次の優先タスクへ進む（PI 起床まで待つ必要なし）
- **物理的判断に迷ったら**: 既存ルール（出典明記、改竄禁止）に従い、判断根拠を `progress/` に書く。後で PI レビュー
- **新しい論文や式が必要になったら**: `progress/.../need_paper_<topic>.md` に書く。Cowork supervisor が次回巡回時に拾って取得試行
- **テスト失敗したら**: 既存テストを修正せず、原因を `progress/.../test_failure_<file>.md` に書いて次へ

## 📊 PI が朝起きた時に見たいもの（最終目標）

1. ✅ `reports/theme_F_shift_current.md` draft v1
2. ✅ `reports/theme_A_g_factor.md` 公開クオリティ
3. ✅ `results/production/` 配下が Production 整備済み
4. ✅ git log に 10+ 新規 commit、すべてテスト通過
5. ✅ `RESULTS.md` が最新状態
6. ✅ `cowork/progress/.../PI_summary_2026-05-24.md` で「PI 不在中に何をやったか」の総括

朝に PI が `RESULTS.md` と `PI_summary_2026-05-24.md` だけ読めば全体把握できるように。

---

---

## ⚠️ フォルダ構造変更（2026-05-23 10:20）

Cowork 関連ファイルを **`cowork/`** サブフォルダに移動しました。以前 `progress/`, `reports/`, `next_directive.md`, `research_ideas.md`, `novelty_assessment.md` をルート直下で参照していた箇所は **すべて `cowork/` プレフィックスを付ける**ようにしてください。詳細は `COWORK_README.md`（プロジェクトルート）参照。

| 旧パス | 新パス |
|---|---|
| `progress/` | `cowork/progress/` |
| `reports/` | `cowork/reports/` |
| `next_directive.md` | `cowork/next_directive.md`（このファイル） |
| `research_ideas.md` | `cowork/research_ideas.md` |
| `novelty_assessment.md` | `cowork/novelty_assessment.md` |

開発プロジェクト本体（`src/`, `tests/`, `data/`, `configs/`, `scripts/`, `docs/`, `notebooks/`, `.steering/`, `references/`, `results/`, `CLAUDE.md`, `README.md`, `RESULTS.md`, `pyproject.toml`, `requirements.txt`）は触らない。

---

## ⭐ 本番計算ルール（2026-05-23 10:35 追加）

**論文・公開・最終報告書に使う計算は必ず `cowork/PRODUCTION_RULES.md` に従う**。要点：

- 計算は **Exploratory（試行錯誤）/ Production（本番）** を明示的に分ける
- Production は **収束確認**（k グリッド、η、ω 分解能を 3 段階以上）必須
- Production は `results/production/<theme>/<date>_<commitHash>/` に**全データ保存**（生数値・収束プロット・ログ・乱数シード含む）
- 入力ファイル一式（config, parameters, env.yml, git_info）を `inputs/` に保存
- 中心索引 `MANIFEST.json` を必ず置く（テンプレ PRODUCTION_RULES.md §4）
- Production 実行時は uncommitted modification なし
- `cowork/reports/` で引用する数値は **MANIFEST.json への参照付き**

既存の Theme A / Phase 1.5 結果は次の自然な作業区切りで遡及的に Production 化。

詳細・テンプレートは `cowork/PRODUCTION_RULES.md` を参照。

---

## 0. ハルシネーション防止の絶対ルール（必読）

**コード実装に着手する前に、以下を必ず満たすこと:**

1. **アルゴリズムの出典が論文 DOI/arXiv ID + 式番号で特定できる**こと
   - 本 directive で出典を提示します。出典が無い実装は禁止
   - 「TB の標準的な手法」「教科書通り」だけでは不十分。具体的な文献を本 directive に列挙します

2. **論文の式と実装コードの対応を docstring に明示**
   - 例: `# Implements Eq. (5) of Kirstein 2021 (arXiv:2112.15384)`
   - 改変・近似する場合は理由も明記

3. **論文の値（Table の数値）を再現できないものは「再現困難」と報告**
   - 値を改竄しない（既存 CLAUDE.md ルールの徹底）

4. **論文に明示されていない数値・パラメータは「文献調査」タスクとして Cowork に依頼**
   - 推測しない。「Sn の Δ は ~0.7 eV だろう」のような曖昧推定は禁止
   - `progress/.../「行き詰まったこと」` で Cowork に確認

5. **不明な式の導出を要求された場合、紙計算で出典と整合確認してから実装**
   - Cowork レビュー時に式展開を含めて再現可能にしておく

---

## 1. 現在の進捗（2026-05-23 08:15 時点）

| Phase / Theme | 状態 |
|---|---|
| Phase 1 Theme A (g-factor) A1 | ✅ 完了 (commit 83553f0) |
| Phase 1 Theme A A2 | ✅ 完了 (commits 354e5be, 57aeaee)、Cowork レビュー応答 #2 済み |
| Phase 1 Theme A A3 (検証テスト) | ✅ A2 内で実施済み（21 + 5 = 26 tests、既存 163 維持で計 189） |
| Phase 1 Theme A A4 (9 材料スキャン) | 🔵 **着手 OK（本 directive で指示）** |
| Phase 1 Theme A A5 (解析・報告書) | ⏳ A4 完了後 |
| Phase 1.5 光学特性 | ⏳ A4 と並行可能 |
| **Phase 2 NEW** Theme F (BPVE/shift current) | ⏳ Phase 1 完了後 |
| Phase 3 Theme D (chiral CD) | ⏳ |
| **Phase 4 NEW** Theme G (carrier mobility) | ⏳ |
| ~~Phase 2 旧 Theme C (ML)~~ | 機会があれば（優先度低） |

---

## 2. Phase 1 Theme A A4: 9 材料 g 因子スキャン（最優先・即着手）

### 2.1 文献根拠（必読）

実装の根拠となる論文と式を明示します。**実装中は常にこれらを参照すること:**

| 出典 | 取り出す情報 | 該当箇所 |
|---|---|---|
| Kirstein 2021, arXiv:2112.15384 | g_e, g_h の k·p 普遍公式、普遍パラメータ | Eq.(5), Eq.(6), Fig.5 caption |
| Nestoklon 2023, arXiv:2305.10586 | Table S2 のバルク ETB g 因子（Pb 3 ハライド）、k·p 公式の SI 版 | SI Eq.(S3), Eq.(S7), Table S1, Table S2 |
| Kopteva 2026, arXiv:2605.15807 | 2D RP 層依存 g 因子の実験ベンチマーク | 本文表 |

### 2.2 文献から抽出する数値（Cowork が以下を提供）

**実験 Eg と SOC 分裂 Δ（A4 で使用）:**

```json
{
  "CsPbCl3": {"Eg_eV": 3.04, "Delta_eV": 1.53, "Eg_source": "DOI:10.1038/s41467-022-30701-0", "Delta_source": "arXiv:2305.10586 Table S2"},
  "CsPbBr3": {"Eg_eV": 2.36, "Delta_eV": 1.44, "Eg_source": "同上", "Delta_source": "同上"},
  "CsPbI3":  {"Eg_eV": 1.73, "Delta_eV": 1.26, "Eg_source": "同上 (alpha phase)", "Delta_source": "同上"},
  "CsSnCl3": {"Eg_eV": 2.85, "Delta_eV": null, "Eg_source": "DOI:10.1021/ja4023298 (Stoumpos JACS 2013)", "Delta_source": "未確定（Cowork 調査中）"},
  "CsSnBr3": {"Eg_eV": 1.77, "Delta_eV": null, "Eg_source": "同上", "Delta_source": "同上"},
  "CsSnI3":  {"Eg_eV": 1.30, "Delta_eV": null, "Eg_source": "同上", "Delta_source": "同上"},
  "CsGeCl3": {"Eg_eV": 3.40, "Delta_eV": null, "Eg_source": "DOI:10.1063/1.5045820 (Lin 2018)", "Delta_source": "同上"},
  "CsGeBr3": {"Eg_eV": 2.32, "Delta_eV": null, "Eg_source": "同上", "Delta_source": "同上"},
  "CsGeI3":  {"Eg_eV": 1.60, "Delta_eV": null, "Eg_source": "同上", "Delta_source": "同上"}
}
```

**Sn/Ge の Δ は文献調査中。** 暫定的に：
- Sn 系の Δ は **Kashikar 13軌道の λ_Sn を読んで Δ_Sn = 3 λ_Sn で計算**してください（`data/parameters/SOURCES.md` 参照）
- Ge 系も同様 Δ_Ge = 3 λ_Ge
- これは Kashikar の解析式 Eq.(9) で R 点 SOC 分裂が `3λ` になることに基づく **物理的に正当な選択**（Kashikar arXiv:2101.08562 Eq.(9) 出典）

不確かさ伝搬：**Δ には ±20% 程度の不確かさがある**ことを明記し、g 因子も範囲で報告してください。

### 2.3 タスクリスト

**Step A4-1.** `data/parameters/experimental_band_data.json` 作成
- 上記 JSON を出典付きで書き出し
- Sn/Ge の Δ は Kashikar から計算して埋める（出典: Kashikar 2021 Eq.(9)）

**Step A4-2.** `scripts/scan_g_factors.py`
- 9 材料に k·p 普遍式 (Kirstein Eq.5, Eq.6) を適用
- 2 通りの計算:
  - (i) 普遍パラメータ (p=6.8 eV·Å, Δg_e=−1) で全材料 → 「Kirstein 普遍曲線が Sn/Ge で成立するか」
  - (ii) 材料別の Δ を反映 → 「Sn/Ge は SOC が小さい分、関係がどう変わるか」
- 出力: `results/g_factors/g_factor_9material.csv`

**Step A4-3.** プロット
- `results/g_factors/kirstein_universal_plot.png`: x=Eg, y=g_e と g_h, Kirstein 曲線重畳
- `results/g_factors/material_grid.png`: 3×3 ヒートマップ
- 不確かさをエラーバーで表示

**Step A4-4.** 検証
- Pb 系 3 材料が Nestoklon Table S2 と meV 一致を assert
- Kirstein 2021 Fig.5 を視覚的に再現できるか確認

### 2.4 Phase 1.5（光学特性、並行可）

光学物性の文献根拠も明示しておきます：

| 出典 | 取り出す情報 | 該当箇所 |
|---|---|---|
| Cho 2019, arXiv:1908.09436 | 層状ペロブスカイトの TB-GW-BSE 計算（電子-ホール相互作用込み） | 全文 |
| Apergi 2023, arXiv:2309.14002 | TB から複素誘電関数 ε(ω) を出す手順、velocity operator 法 | Eq.(2)-(4) |
| Sipe & Shkrebtii 2000, PRB 61, 5337 | 線形・非線形光学応答の k 空間表式 | Eq.(2.7), Eq.(3.13) |

光学物性は g 因子と **同じ velocity operator** を使うので、A2 のインフラがそのまま使えます。

---

## 3. Phase 2 NEW: Theme F — Bulk Photovoltaic Effect / Shift Current

**狙い:** 9 材料 × 偏光方向で **shift current 応答**を系統スキャン。光起電力素子の設計指標として未踏領域（特に Sn/Ge）を予測。2025-2026 のホットトピック。

### 3.1 文献根拠（必読）

| 出典 | 役割 | 該当箇所 |
|---|---|---|
| **Young & Rappe 2012**, PRL 109, 116601, DOI:10.1103/PhysRevLett.109.116601 | **shift current の第一原理公式（核心）** | Eq.(1), Eq.(2) |
| **Sipe & Shkrebtii 2000**, PRB 61, 5337 | 非線形光学応答の一般理論 | Eq.(3.13) σ^(2) |
| **Tan & Rappe 2016**, npj Comput. Mater. 2, 16026, DOI:10.1038/npjcompumats.2016.26 | **ハライド・酸化物ペロブスカイトの shift current TB 計算** | 全文（特に Methods） |
| **Fregoso, Morimoto, Moore 2017**, PRB 96, 075421 | shift vector / Berry connection 形式 | Eq.(7) |
| **Cook, Fregoso et al. 2017**, Nat. Commun. 8, 14176 | shift current の対称性解析と TB 例 | Methods |
| **arXiv:2105.11310** (既収集) | bulk photovoltaic + 光誘起相転移、関連例 | 全文 |

**最重要:** Young & Rappe 2012 と Tan & Rappe 2016 を**先に読んでください**。Tan & Rappe は半ハライド系の shift current を TB で計算した先行例で、本研究の **直接の方法論ベース**になります。

### 3.2 計算式（Young & Rappe Eq.1, Sipe-Shkrebtii Eq.3.13 改変）

```
σ^(shift)_abc(ω) = -π e³/ℏ² · ∫ dk/(2π)³ · Σ_{n,m} f_{nm} · Im[r^a_{mn} r^b_{nm;c}] · δ(ω - ω_{nm})

ここで
  r^a_{mn} = i ⟨u_n | ∂/∂k^a | u_m⟩   (Berry connection)
  r^b_{nm;c} = ∂_{k^c} r^b_{nm} - i(r^c_{nn} - r^c_{mm}) r^b_{nm}   (covariant derivative)
  f_{nm} = f_n - f_m   (occupation difference)
  ω_{nm} = (E_m - E_n)/ℏ
```

**実装上の注意:**
- Berry connection `r^a_{mn}` は **velocity operator から計算**: `r^a_{mn} = i p^a_{mn} / (m₀ ω_{nm})` for `n ≠ m`
- これは A2 で実装済みの `velocity_operator(k)` をそのまま使える
- δ 関数は Lorentzian で smooth 化（η = 0.05 eV、Tan & Rappe と同じ）
- 立方ペロブスカイトでは bulk の shift current は通常 **ゼロ**（中心対称）。**歪み or 内部歪み を入れて symmetry を破る必要あり** — Theme B（廃止）の bond angle を Theme F の symmetry breaker として復活

### 3.3 タスクリスト

**Step F1.** Young & Rappe 2012 と Tan & Rappe 2016 を `references/pdfs/` から読む（既収集の確認、無ければ Cowork へ追加収集を依頼）

**Step F2.** `docs/shift-current-formulation.md` draft（A1 と同じ要領）
- Eq. の TB 表現
- 対称性条件（立方対称では vanishing → 何を symmetry breaker にするか）
- 検証アンカー: Tan & Rappe Fig.? の MAPbI₃ shift current ピーク値

**Step F3.** `src/perovskite_tb/shift_current.py`
- velocity operator + Berry connection 計算
- σ^(2)_abc(ω) を k グリッドで積分
- 立方対称な CsBX₃ には **uniaxial strain** or **bond-angle distortion** を加える（Theme B 統合）

**Step F4.** 検証テスト
- Sipe-Shkrebtii sum rule（出典: Sipe 2000 Eq.4.5）
- Tan & Rappe 2016 の MAPbI₃ ピーク位置を再現（±0.1 eV）
- 立方対称無歪みで σ^(2) ≈ 0（数値積分誤差以内）

**Step F5.** 9 材料 × 歪みスキャン
- 5% uniaxial strain で σ^(2)_xxx(ω) を計算
- 9 材料の最大値・スペクトル形状を比較
- 「Sn/Ge 系は shift current が大きいか」を検証

**Step F6.** 報告書 `reports/theme_F_shift_current.md`

---

## 4. Phase 3 Theme D: Chiral CD（Sn/Ge 拡張、優先度上昇）

### 4.1 文献根拠

| 出典 | 役割 |
|---|---|
| **Apergi 2023**, arXiv:2309.14002 | **直接の方法論ベース。** Pb 系 chiral perovskite の CD を TB で計算 |
| Sebastiani 2008, Mol. Phys. 106, 1117 | 凝縮系の CD 計算理論（参考） |

実装は Apergi 2023 を踏襲し、Sn/Ge B サイト変更で予測。**A4 完了後に着手。**

---

## 5. Phase 4 NEW: Theme G — Carrier Mobility（Sn/Ge 系の TB+Boltzmann）

**狙い:** Sn 系で実験的に高移動度が報告されているが、TB ベースの系統論（Ge 含む 9 材料）は存在しない。フォノン散乱の Fröhlich 模型で μ(T) を予測。

### 5.1 文献根拠

| 出典 | 役割 |
|---|---|
| **Frost 2017**, PRB 96, 195202, DOI:10.1103/PhysRevB.96.195202 | **ハライドペロブスカイトの Fröhlich polaron mobility（核心）** |
| **Hellman et al. 2009**, PRB 80, 014102 | 第一原理 Fröhlich モビリティの一般枠組み |
| **Filippetti et al. 2021** などレビュー類 | ハライドペロブスカイト輸送物性レビュー |
| **arXiv:2105.06525** (既収集) | MAPbI3 の動的不規則性と TB | 関連 |

### 5.2 計算式（Frost 2017 Eq.?）

Fröhlich 結合定数 α と effective mass m\* から：
```
μ_FH(T) = (e/(2 α ω_LO m*)) · [(exp(ℏω_LO/kT) - 1)] · ...
```
詳細は Frost 2017 を Step G1 で読み込み、`docs/mobility-formulation.md` を書く。

**effective mass は既存の Kashikar/Nestoklon TB から直接出る**（band curvature の数値微分）。これは A2 の velocity operator の発展系。

### 5.3 タスクリスト

A4 完了後に詳細化。Theme F 完了後の着手想定。

---

## 6. テーマごとの報告書（必須・1ネタ1報告書）

各テーマ（Phase）が完了したら、**結果が面白くなくても必ず**報告書を `reports/` 配下に書いてください。ネガティブ結果も科学的価値があります。フォーマットは v1 の指示通り（`reports/` の例参照）。

- `reports/theme_A_g_factor.md`
- `reports/theme_A5_optical.md`
- `reports/theme_F_shift_current.md` (Phase 2)
- `reports/theme_D_chiral_CD.md` (Phase 3)
- `reports/theme_G_mobility.md` (Phase 4)

---

## 7. 進捗確認と次の指示について（高頻度ループ）

**Claude Code 側のルール（必読）:**
- **サブタスク完了ごと**または **git commit するごと** に `next_directive.md` を読み直してください。内容が更新されていることがあります
- 同様に、コミット直前に **`progress/code_review_*.md`** の新着があれば確認してください
- 30 分以上行き詰まったら、`progress/.../「行き詰まったこと」` に詳細を書いて **そこで一旦止まる**

**Cowork（監督）側のルール:**
- 毎時 8 分にこのリポを巡回します（supervisor task）
- 月・木 9:00 に進行中テーマの新規性を厳密検証します（novelty-watch task）
- レビュー依頼や行き詰まり報告があれば、`progress/code_review_YYYYMMDD_HHMM.md` で返します
- 重要判断はユーザーに通知

---

## 8. コードレビュー協力（Cowork 側）

光学・輸送系を含めると新規コードが大幅に増えます。Cowork は以下を引き受けます：

### Cowork がやれること
- **コードレビュー:** `git diff` または `progress/` 経由でコミット差分を提示してくれれば、physics の正しさ・テストの十分性・既存規約との整合をチェックして `progress/code_review_YYYYMMDD_HHMM.md` で返します
- **数値整合性チェック:** 「論文 Eq.(X) と実装が一致するか」を別途独立に検証（紙ベースで式展開）
- **論文の追加調査:** 「アルゴリズムの細部の出典が不明」「最新の Fröhlich モデル variant」など、文献調査が必要なら Cowork が webfetch/Chrome で探します
- **進捗ファイルの定期巡回:** 1 時間に 1 回 `progress/` を読みます

### レビュー依頼の出し方
`progress/YYYY-MM-DD_HHMM_review_request.md` を作成：

```markdown
## レビュー依頼
- 対象: src/perovskite_tb/shift_current.py (commit hash: abc123)
- 観点: Young & Rappe 2012 Eq.(1) の TB 表現が docs/shift-current-formulation.md と合っているか
- 急ぎ度: 通常 / 急
- 添付: 必要なら計算結果プロットへのパスも
```

私が次回巡回時に `progress/code_review_YYYYMMDD_HHMM.md` で返答します。

---

## 9. まずやってほしいこと（A4 着手 first action）

```bash
# 1. 文献の確認（既収集 PDF にあることを確認）
ls references/pdfs/arxiv_2112.15384.pdf  # Kirstein 2021
ls references/pdfs/arxiv_2305.10586.pdf  # Nestoklon 2023
# Young & Rappe 2012 (PRL) は arXiv にあれば取得、無ければ Cowork に依頼

# 2. data/parameters/experimental_band_data.json を作成（§2.2 の表通り）
# Sn/Ge の Δ は Kashikar λ から計算: Δ = 3λ_B (Kashikar Eq.9 出典)

# 3. scripts/scan_g_factors.py 実装、A4-2 を実行

# 4. プロット + 検証

# 5. progress/2026-05-23_phase1_log.md に追記、A4 結果を報告
```

---

がんばってください。次の commit/サブタスク完了時に、本 directive と `progress/2026-05-23_0810_code_review.md` を読み直してから進めてください。
