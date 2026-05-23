# Next Directive — Claude Code 向け作業指示

**発行日:** 2026-05-23
**発行元:** Cowork（監督役）
**有効期限:** 次の `next_directive.md` 更新まで
**全体方針:** 既存の論文値再現済み TB エンジン（Kashikar 13/4軌道, Nestoklon sp³d⁵s\*）を活かし、**実験では未測定 / 系統的に計算されていない物性を Hamiltonian から予測**して学術コミュニティに貢献する。実験は不要。論文に出ている実験値はベンチマーク用にのみ使う。

研究テーマ全体像は `research_ideas.md` を参照。**新規性検証（2026-05-23）の結果は `novelty_assessment.md` を必ず確認**してください。

**改訂版優先順位（2026-05-23 update）:**

| Phase | テーマ | 新規性 |
|---|---|---|
| Phase 1 | **Theme A**: g 因子 9 材料マップ | ✅ 強い |
| Phase 2 | **Theme C**: ML 内挿で混合 B サイト予測 | ✅ 中 |
| Phase 3 | **Theme D**: Sn/Ge chiral CD（Apergi 拡張） | ✅ 強い |
| — | ~~Theme B（bond angle → Rashba 単独）~~ | ⚠️ Boyer-Richard 2016 と重複。Theme A の延長として統合 |

本 directive は **Phase 1 (Theme A)** の着手指示。

---

## Phase 1: g 因子計算モジュールの追加（目標 2 週間）

### A1. 文献読み込み（先行作業、半日）

以下を `references/pdfs/` から `pdftotext` 化して読む。**特に式番号と検証アンカーをメモ**：

1. **2112.15384** Kirstein 2021 "The Landé factors of electrons and holes in lead halide perovskites: universal dependence on the band gap"
   - **要抽出:** 普遍関係 g(Eg) の関数形（Eq. ?）、実験 g 値表（CsPbCl₃, CsPbBr₃, CsPbI₃, MAPbI₃ 等）
   - Pb 系のみ扱われている。Sn/Ge 系の予測こそが本研究の貢献

2. **2305.10586** Nestoklon 2023 "Tailoring electron and hole Landé factors in lead halide perovskite nanocrystals"
   - **要抽出:** TB Hamiltonian からの g因子計算式（Roth-Lax 公式の具体的な書き下し）
   - sp³d⁵s\* で実装されているはず。既存の Nestoklon パラメータと整合する

3. **2605.15807** Kopteva 2026 "Layer-dependent Landé g-factors of electrons, holes, and excitons in 2D RP lead halide perovskites"
   - **要抽出:** 最新の実験値（特に CsPbBr₃, CsPbI₃ のバルクと層構造）。比較のベンチマーク用

4. **2012.14705** Nestoklon 2020 "Tight-binding description of inorganic lead halide perovskites in cubic phase"
   - 既存実装の元論文。g因子計算は明示的に書かれていないが、Hamiltonian と速度演算子は揃っている

**出力物:** `docs/g-factor-formulation.md`（理論定式化メモ、3-5ページ）。Roth-Lax 公式の TB 表現、要求される行列要素、検証アンカー（Kirstein 表の Pb 系 g 値）を整理。

### A2. 実装（コア機能）

新規モジュール `src/perovskite_tb/g_factor.py` を作成：

```python
def compute_g_factor(
    hamiltonian: np.ndarray,      # H(k) at k=k0 (band edge)
    velocity_ops: tuple[np.ndarray, np.ndarray, np.ndarray],  # vx, vy, vz
    band_index: int,              # 着目バンドのインデックス
    spin_orbit_basis: bool = True,
) -> dict:
    """
    Roth-Lax 公式で g テンソルを計算する。

    Returns
    -------
    {"g_iso": float, "g_xx": float, "g_yy": float, "g_zz": float,
     "delta_g": float, "method": "Roth-Lax-2nd-order"}
    """
```

設計指針：
- **既存の Hamiltonian builder と velocity operator builder を再利用**（破壊変更しない）
- 速度演算子 v = (1/ℏ) ∂H/∂k は数値微分でなく **解析的に出す**（既存 SK 行列要素から導出）。誤差を桁で改善できる
- 立方対称なら g_iso = g_xx = g_yy = g_zz になることをテストで確認
- SOC を λ → 0 にする極限で g → 2.0023 (自由電子値) に収束することをテストで確認

### A3. 検証テスト（必須）

`tests/test_g_factor.py` を新規作成。以下を pytest で通す：

1. **解析極限:** SOC λ → 0 で電子 g → 2.0023（許容誤差 1e-3）
2. **対称性:** 立方ペロブスカイトで g_xx = g_yy = g_zz（許容誤差 1e-6）
3. **Kirstein 実験値再現:** Pb 系 3 材料（Cl/Br/I）で既存 Hamiltonian から計算した g_e, g_h が Kirstein 2021 の実験値と **符号と大きさのオーダーで一致**（許容誤差 ±0.5、これは TB 近似の限界）
4. **Nestoklon 2023 との交差検証:** ナノ結晶極限（量子閉じ込めなし）で Nestoklon の Pb 系 g 値と一致

検証が通らない場合は **値を改竄しない**。`docs/g-factor-formulation.md` に「TB 近似で再現困難な物理」として記録し、考察を残す。

### A4. 9 材料スキャン（メイン計算）

`scripts/scan_g_factors.py` を作成し、以下を実行：

```python
# 全 9 材料（既存 JSON パラメータ）に対し g テンソルを計算
materials = ["CsGeCl3", "CsGeBr3", "CsGeI3",
             "CsSnCl3", "CsSnBr3", "CsSnI3",
             "CsPbCl3", "CsPbBr3", "CsPbI3"]
models = ["kashikar2021_cubic_13orb", "nestoklon2021_CsPbI3"]  # 後者は CsPbI3 のみ

# 結果を CSV と PDF プロット両方で出す
# 列: material, model, Eg(eV), g_e, g_h, g_exciton
```

**出力:**
- `results/g_factors/g_factor_table.csv` — 全数値
- `results/g_factors/kirstein_plot.png` — x軸: Eg, y軸: g_e と g_h（Kirstein の普遍関係に乗るか確認）
- `results/g_factors/material_grid.png` — 3×3 ヒートマップ（B, X 各3）

### A5. 解析・考察ノート

`docs/g-factor-analysis.md` に以下を書く：

1. Pb 系 3 材料が Kirstein 普遍関係を再現するか（成功なら定量的に、失敗なら原因考察）
2. Sn 系・Ge 系の **予測値**（実験未測定）と、Pb 系の普遍関係から外挿される値との比較
3. **どの材料で g 因子が異常になるか**（普遍関係から外れる）。これが論文のキーポイント
4. 鉛フリー光学スピン素子の候補ランキング表（|g|, バンドギャップ, 直接性で総合スコア）

### A6. 進捗報告（必須・毎日 or 区切りごと）

以下のフォーマットで `progress/YYYY-MM-DD_phase1_log.md` を作成・追記する：

```markdown
# Phase 1 進捗ログ: YYYY-MM-DD

## 完了したサブタスク
- [ ] A1 (文献読み込み)
- [ ] A2 (実装)
- [ ] A3 (テスト)
- [ ] A4 (9材料スキャン)
- [ ] A5 (解析)

## 今日やったこと
- ...

## 数値結果（あれば）
- CsPbI3 g_e (Kashikar 13orb) = X.XX (Kirstein exp: Y.YY, diff: Z%)
- ...

## 行き詰まったこと / 判断に迷うこと
- ...

## 次に何をするか
- ...
```

---

---

## Phase 1.5: 光学特性モジュール（A2 と並行可、目標 2-3 週間）

g 因子と並行して **光学特性計算モジュール**を入れます。これも Theme A の延長で、光デバイス応用に直結し、Sn/Ge 系で実験未測定の予測ができる重要な切り口です。

### B1. 文献から定式化を抽出

- **1908.09436** Cho 2019 "TB-GW-BSE for layered hybrid perovskites" — TB から複素誘電関数 ε(ω) を出す手順。励起子効果は Wannier 模型で
- **2309.14002** Apergi 2023 "CD of chiral halide perovskites: TB" — 円二色性（CD）の Berry phase 表現、kxk 行列要素の出し方（chirality 拡張は Phase 2 で扱う）
- **2104.07771** Benam 2021 — 光学吸収端と SOC の関係

`docs/optical-formulation.md` に整理してください（Roth-Lax と同じ要領で）。

### B2. 実装

`src/perovskite_tb/optical.py` に以下を追加：

```python
def compute_dielectric(
    hamiltonian_fn: Callable[[np.ndarray], np.ndarray],  # H(k)
    velocity_ops_fn: Callable[[np.ndarray], tuple],       # vx(k), vy(k), vz(k)
    k_grid: np.ndarray,                                   # Monkhorst-Pack
    omega_grid: np.ndarray,                               # eV
    smearing_eta: float = 0.05,                           # eV (Lorentzian)
    include_local_field: bool = False,
) -> dict:
    """
    線形応答理論（Kubo-Greenwood）で複素誘電関数を計算。
    励起子効果は含めない（次フェーズで Wannier-Mott or BSE 簡易版を検討）。

    Returns: {"omega": np.ndarray, "eps_real": np.ndarray, "eps_imag": np.ndarray,
              "alpha": np.ndarray (absorption coefficient), "n_refractive": np.ndarray}
    """
```

設計指針:
- k 点数収束は **論文値を再現するまでテストで担保**
- 既存 g_factor.py と **velocity operator を共有**（重複実装禁止）
- 立方対称材料では ε_xx = ε_yy = ε_zz を確認

### B3. 検証テスト

`tests/test_optical.py`:
1. **f-sum rule:** ∫ ω·Im[ε(ω)] dω = π·ω_p²/2（許容 1%）
2. **Kramers-Kronig 整合:** 計算した Im[ε] から KK 変換した Re[ε] と直接計算した Re[ε] が一致
3. **Pb 系で論文値再現:** Cho 2019 Fig.? の CsPbI₃ ε(ω) ピーク位置（許容 ±0.1 eV）

### B4. 9材料 + g因子 × 光学物性 統合スキャン

`scripts/scan_optoelectronic.py`:

```python
# 9材料 × {g_factor, dielectric, absorption} を一気に出す
# 出力: results/optoelectronic/{material}_{model}/
#   - bands.png  (既存)
#   - g_tensor.json
#   - eps_omega.png
#   - absorption.png
#   - summary.json  (Eg, g_e, g_h, eps_inf, peak1_eV, peak1_intensity, ...)
```

`results/optoelectronic/full_summary.csv` に全 9 材料 × 2 モデルの全数値を集約。

### B5. 解析

`docs/optoelectronic-analysis.md`:
1. 鉛フリー（Sn/Ge）でバンドギャップが小さく g 因子が大きい組成 → **赤外スピン-LED 候補**
2. 吸収係数の大きい鉛フリー組成 → **太陽電池候補**
3. (g, α(ω peak), Eg) の 3D 散布図で「未開拓だが有望」な領域をマーク

---

## コードレビュー協力（Cowork 側）

光学を含めると新規コードが 1500-2000 行 + テスト多数になります。Cowork は以下を引き受けます：

### Cowork がやれること
- **コードレビュー:** `git diff` または `progress/` 経由でコミット差分を提示してくれれば、physics の正しさ・テストの十分性・既存規約との整合をチェックして `progress/code_review_YYYYMMDD.md` で返します
- **数値整合性チェック:** 「論文 Eq.(X) と実装が一致するか」を別途独立に検証（紙ベースで式展開して確認）
- **論文の追加調査:** 「Roth-Lax の最新変種が見つからない」「励起子効果の TB 軽量実装を探したい」など、文献調査が必要なら Cowork が webfetch/Chrome で探します
- **進捗ファイルの定期巡回:** 日次で `progress/` を読み、判断が必要なら user に通知

### レビュー依頼の出し方
`progress/` に以下のように書いてください：

```markdown
## レビュー依頼
- 対象: src/perovskite_tb/g_factor.py (commit hash: abc123)
- 観点: Roth-Lax 公式の TB 行列要素への落とし方が docs/g-factor-formulation.md と合っているか
- 急ぎ度: 通常 / 急
- 添付: 必要なら計算結果プロットへのパスも
```

私が次回巡回時に `progress/code_review_YYYYMMDD.md` で返答します。

---

---

## テーマごとの報告書（必須・1ネタ1報告書）

各テーマ（Phase）が完了したら、**結果が面白くなくても必ず**報告書を `reports/` 配下に書いてください。ネガティブ結果も科学的価値があります。

### 報告書のフォーマット

`reports/theme_<X>_<short_name>.md`（例: `reports/theme_A_g_factor.md`, `reports/theme_A5_optical.md`）

```markdown
# Theme X: <タイトル>

**ステータス:** 完了 / 部分完了 / 失敗（理由）
**実施期間:** YYYY-MM-DD 〜 YYYY-MM-DD
**コミット範囲:** abc123..def456

## 1. 動機と仮説
- 何を予測したかったか
- どんな新規性を狙ったか

## 2. 方法
- 使った Hamiltonian と論文出典
- 実装の要点（コア式）
- 検証アンカー

## 3. 主要結果
- 数値（表 + プロット）
- **未測定物性の予測値**（実験で確認待ちの新しい数値はここに明示）

## 4. 論文値との比較・整合性
- 既知の物性値（Pb 系の Kirstein g 因子等）の再現精度
- 整合する範囲と外れる範囲

## 5. 物理的考察
- なぜそうなったか
- 既存理論との関係
- 例外があればその原因

## 6. 学会・論文化の見通し
- このネタ単独で論文1本になるか、組み合わせるか
- どのジャーナル/学会が向くか（PRB, PRL, JPC, MRS Meeting, APS March 等）
- 「面白い結果」と「面白くない結果」の区別を率直に書く

## 7. 限界・残課題
- TB 近似の限界由来の不確かさ
- 次フェーズで解決すべき点

## 8. 再現コマンド
```bash
# 完全に再現できる手順を貼る
PYTHONPATH=src python -m perovskite_tb gfactor --params ... --material all
```

## 9. 関連ファイル
- 実装: src/perovskite_tb/g_factor.py
- テスト: tests/test_g_factor.py
- データ: results/g_factors/g_factor_table.csv
- 図: results/g_factors/*.png
```

**面白くない結果の例:**
- 「予想したような Sn 系の g 因子異常は見られなかった」→ それでも報告書には Kirstein 普遍関係に乗ることを示し「鉛フリーでも普遍関係が成立する」というポジティブな解釈を書く
- 「テストが論文値を再現できなかった」→ 原因（TB 近似の限界 / 論文の誤植可能性 / 実装ミス）を切り分けて報告

報告書ができたら `progress/YYYY-MM-DD_HHMM_report_ready.md` で Cowork に通知してください。Cowork がレビューして公開可能なクオリティに磨きます。

---

## 進捗確認と次の指示について（高頻度ループ）

**Claude Code 側のルール（必読）:**
- **サブタスク完了ごと**（A1→A2→A3 と進むごと）、または **git commit するごと** に `next_directive.md` を読み直してください。内容が更新されていることがあります
- 同様に、コミット直前に **`progress/code_review_*.md`** の新着があれば確認してください（Cowork からの review コメント）
- 30 分以上行き詰まったら、`progress/.../「行き詰まったこと」` に詳細を書いて **そこで一旦止まる**。次の巡回で Cowork が拾います（待ち時間を最小化）

**Cowork（監督）側のルール:**
- 1 時間に 1 回、`progress/` と最新コミットを巡回します
- レビュー依頼や行き詰まり報告があれば、`progress/code_review_YYYYMMDD_HHMM.md` で返します
- 重要判断はユーザーに通知

Phase 1+1.5 が概ね完了したら、**次の `next_directive.md` を書き換え**て Phase 2（Theme B: Rashba ボンド角スキャン、または Theme D: chiral CD 計算）に移ります

---

## 守ってほしいルール（既存 CLAUDE.md と整合）

1. **ハルシネーション禁止。** 全パラメータ・式は論文出典つき。テストで論文値を再現できないものは「再現困難」と記録して進める（値を改竄しない）
2. **既存テスト 163 個を絶対に壊さない。** 拡張のみ。破壊変更が必要なら別ブランチで提案
3. **新規論文が必要になったら** `references/pdfs/` を確認 → 無ければユーザーに依頼（Cowork が arxiv 等から取得）
4. **コミット頻度高め。** サブタスクごとに `git commit`、コミットメッセージに何の検証アンカーをクリアしたか書く
5. **不明点はユーザーに聞かず、まず `progress/.../「行き詰まったこと」` に書く。** 私が日次で拾います

---

## まずやってほしいこと（指示待ち解消用 first action）

このセクションを読んだら、まず以下を実行してください：

```bash
# 1. 文献テキスト化（重複は skip）
mkdir -p references/texts
for f in references/pdfs/arxiv_*.pdf; do
  base=$(basename "$f" .pdf)
  [ -f "references/texts/${base}.txt" ] && continue
  pdftotext -layout "$f" "references/texts/${base}.txt"
done

# 2. 進捗ディレクトリの初期化
mkdir -p progress
echo "# Phase 1 進捗ログ: $(date +%Y-%m-%d)\n\n## サブタスク\n- [ ] A1 文献読み込み\n- [ ] A2 実装\n- [ ] A3 テスト\n- [ ] A4 スキャン\n- [ ] A5 解析\n" > progress/$(date +%Y-%m-%d)_phase1_log.md
```

その上で、**A1（文献読み込み）から開始**してください。`docs/g-factor-formulation.md` のドラフト第一版（Roth-Lax 公式の TB 形式、検証アンカー一覧）を書いて `progress/` を更新したら、一度そこで止まって構いません（Cowork が次回巡回時に確認します）。

なお、Cowork は実験できませんが、論文の引用関係・最新動向の検索・PDF の追加収集はできます。必要なら `progress/.../「行き詰まったこと」` に「○○の論文が欲しい」「○○について最新の状況を調べてほしい」と書いてください。

がんばってください！
