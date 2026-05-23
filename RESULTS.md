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
| 論文値の再現テスト (V&V) | ✅ 完了（**163 テスト全通過**） |
| バンド構造プロット出力 | ✅ 完了（全12図） |
| ドキュメント整備 (docs/) | 🔄 進行中 |

**`pytest`: 163 passed.** JSON 入力 → CLI でバンド図生成まで一通り動作。

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

## 5. 残タスク

1. `docs/` 永続ドキュメント9本の整備（自己レビュー2回で承認）。
2. 破損 PDF の再取得・確認、新規論文の定期チェック。
3. （任意）2D/層状ペロブスカイトや他モデルへの拡張。
