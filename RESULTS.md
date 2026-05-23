# 進捗・再現結果サマリ (RESULTS)

> 作業状況と「論文値の再現結果」を一目で分かるようにまとめたファイルです。
> コミットごとに更新します（携帯からの確認用）。

**最終更新:** 2026-05-23
**作業ブランチ:** main

---

## 1. 現在のステータス

| フェーズ | 状態 |
|---|---|
| 論文サーベイ（TBアルゴリズム・パラメータ抽出） | ✅ 完了 |
| パラメータ JSON 化（出典付き） | ✅ 完了 |
| TB 計算エンジン実装（Kashikar 13/4軌道, Nestoklon sp³/sp³d⁵s\*） | ✅ 完了 |
| 論文値の再現テスト (V&V) | ✅ 完了（**228 テスト全通過**） |
| バンド構造プロット出力 | ✅ 完了（全21図 + 再現性メタデータ） |
| ドキュメント整備 (docs/) | ✅ 完了（13本、自己レビュー2回クリアで承認） |
| **Theme A: Landé g 因子 9 材料マップ** | ✅ 完了（Production bundle 化済み） |
| **Phase 1.5: 光学応答 ε(ω) Kubo-Greenwood** | ✅ 完了（Production bundle 化済み） |
| **Theme F: shift current / BPVE** | ✅ 完了（F1–F6, Production bundle 化済み） |

**`pytest`: 228 passed.** JSON 入力 → CLI でバンド図生成まで一通り動作。
全21図 + 物性（g 因子・光学・shift current）を再現性メタデータ付きで出力済み。
Cowork（監督役）と協調し、論文値の検証を最優先（**ハルシネーション禁止**）で進行中。

---

## 2. ★ 論文値の再現結果（最重要）

### Nestoklon (arXiv:2012.14705) 立方晶 CsPbI₃ — 実験/DFT値を厳密再現

| 検証項目 | 論文値 | 本実装 | 差 | 判定 |
|---|---|---|---|---|
| sp³ R点ギャップ (DFT) | 1.017 eV | 1.0182 eV | 1.2 meV | ✅ |
| sp³d⁵s\* R点ギャップ (DFT) | 1.017 eV | **1.0166 eV** | 0.4 meV | ✅ |
| sp³d⁵s\* 伝導帯 SO 分裂 (R点) | 1.48 eV | **1.469 eV** | 11 meV | ✅ |
| 実験補正 R点ギャップ | 1.65 eV | **1.6500 eV** | ~0 | ✅ |
| 実験補正 M点ギャップ | 2.75 eV | **2.7549 eV** | 5 meV | ✅ |
| 直接ギャップが R 点 | (そう) | R点で直接 | — | ✅ |

→ Jancu sp³d⁵s\* モデル（八面体ジオメトリ + d, s\* 軌道 + SOC）の実装が
**論文の数値を meV 精度で再現**。バンド図も Nestoklon Fig.2 と一致
（深い I-s 帯 ~-13.4 eV、Pb-s 結合帯 ~-7.7 eV、Pb-p 伝導帯、d/s\* 高エネルギー帯）。

### Kashikar (arXiv:2101.08562) 立方晶 CsBX₃ 全9種 — 解析式で厳密検証

| 検証項目 | 判定 |
|---|---|
| 13軌道 H(R) の固有値 = 解析式 Eq.(9)（全9材料） | ✅ 機械精度 ~1e-15 |
| 伝導帯 SO 分裂 (R点) = 3λ（全9材料） | ✅ |
| 4軌道 ギャップ閉形式 = 数値対角化 | ✅ |
| 立方ハライドペロブスカイトの直接ギャップ@R | ✅ |

CsBX₃ 9種の R点直接ギャップ（13軌道, SOC込み, eV）:

| | Cl | Br | I |
|---|---|---|---|
| **Ge** | 1.767 | 1.031 | 0.640 |
| **Sn** | 1.056 | 0.383 | 0.175 |
| **Pb** | 2.127 | 1.100 | 0.630 |

（Cl→Br→I でギャップ減少、Sn 系が最小、という論文の傾向を再現。
CsPbI₃ の伝導帯 SO 分裂 1.50 eV は Nestoklon の 1.48 eV とも整合。）

---

## 2.5 物性計算（Phase 2 / Theme A・1.5・F） — 監督役 Cowork と協調

### Theme A: Landé g 因子（9 材料）
- 電子 g_e は 9 材料が **単一普遍曲線**（Kirstein 2021 の k·p 普遍関係）にほぼ載る。
- 正孔 g_h は **鉛フリー（Sn/Ge）で Pb 普遍曲線から上方乖離**（Δ→0 で g_h→+2）← Theme A 主結果。
- Roth-Lax 原子論的 g 因子は Blount 1962 由来で過小（k·p を主、Roth-Lax を比較として併記）。
- bundle: `results/production/theme_A_g_factor/`、報告書: `cowork/reports/theme_A_g_factor.md`。

### Phase 1.5: 光学応答 ε(ω)（9 材料）
- Kubo-Greenwood で誘電関数虚部 ε_i(ω)（Apergi 2023 式）。f-sum rule ~0.21（Blount 限界で過小、既知）。
- bundle: `results/production/phase_1.5_optical/`、報告書: `cowork/reports/theme_A5_optical.md`。

### Theme F: shift current / バルク光起電力効果（BPVE）— ★ 新規完了
- **手法**: velocity-gauge sum-over-states。TB では Fregoso 2017 Eq.(C2) の **第2微分 w 項が必須**
  （連続形では 2-band で σ≡0）。**Rice-Mele 閉形式 Eq.(D15)/(D16) と機械精度一致で符号・prefactor 確定**（F4-3）、
  Tan & Rappe 2016 の対称則とも一致（F4-2）。
- **主結果（F5, 9 材料 × 極性変位 δ, P4mm）**: **鉛フリー Sn/Ge ハライド（特にヨウ化物）が Pb 系より大きい
  shift current**（ピーク |σ_zzz|: CsSnI₃ 3.43 > CsGeI₃ 2.67 > CsSnBr₃ 1.31 ≈ CsGeBr₃ 1.30 > CsPbI₃ 0.97、
  相対単位）。σ はバンドギャップと逆相関。→ 毒性 Pb 代替として Sn/Ge が BPVE 的に有望。
- 絶対 μA/V² は Blount 限界 + 規約敏感のため相対比較を一次成果として deferred。
- bundle: `results/production/theme_F_shift_current/2026-05-23_ef575e3/`、報告書: `cowork/reports/theme_F_shift_current.md`、
  定式化: `docs/shift-current-formulation.md`。

---

## 3. 成果物の場所

- **パラメータ（出典付き JSON）**: `data/parameters/`（`SOURCES.md` に出典・検証アンカー）
- **バンド図**: `results/kashikar13/`（9材料）, `results/kashikar4/`（9材料）,
  `results/nestoklon/`（CsPbI₃ × 3セット）。各図に再現性メタデータ JSON が付属。
- **コード**: `src/perovskite_tb/`
- **テスト**: `tests/`（`pytest` で実行）
- **使い方**: `README.md`、設計は `.steering/20260523-initial-implementation/`

### 再現コマンド例
```bash
pip install -r requirements.txt
PYTHONPATH=src python -m perovskite_tb gap --params data/parameters/kashikar2021_cubic_13orb.json --material all
PYTHONPATH=src python -m perovskite_tb band --params data/parameters/nestoklon2021_CsPbI3.json --parameter-set experiment_corrected --out results/nestoklon/CsPbI3.png
PYTHONPATH=src python -m pytest -q
```

---

## 4. 参照論文の取り込み状況

- `references/pdfs/` に 49 本（自動収集）。一覧は `references/references.md`。
- うち 3 本（arxiv_2209.13267 / 2302.13773 / 2501.06503）は**ダウンロード破損**で未読。
  自動収集で再取得され次第、再確認します（特に 2501.06503 = DFT-leveraged TB は要確認）。

---

## 5. 残タスク / 今後

1. 破損 PDF（2209.13267 / 2302.13773 / 2501.06503）の再取得後の確認。
   `python scripts/screen_papers.py` で破損検出と新規 TB 論文の候補抽出ができる。
2. 新規にたまった論文の定期チェック（同スクリプト）。高関連の未取り込み候補は
   `scripts/screen_papers.py` の出力末尾に列挙される。
3. （任意）2D/層状ペロブスカイト、低対称相（正方/斜方）、他モデル（DFTB 等）への拡張。

## 6. 主要な所感（レビュアー向け）

- **ハルシネーション対策**: すべての式・数値は論文に出典を持ち（`data/parameters/SOURCES.md`）、
  実装は論文の**解析式 (Kashikar Eq.9)** と**明示数値 (Nestoklon の各ギャップ)** に対する
  自動テストで裏付け済み。誤植が疑われる値も改変せず注記のみ。
- 最も強い検証は Kashikar 13軌道の R点固有値が解析式と**機械精度**で一致すること、および
  Nestoklon 実験補正セットが R=1.65 / M=2.75 eV を**ほぼ完全一致**で再現すること。
