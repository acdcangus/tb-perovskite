# 進捗・再現結果サマリ (RESULTS)

> このファイルは作業状況と「論文値の再現結果」を一目で分かるようにまとめたものです。
> 携帯からでも確認できるよう、コミットごとに更新します。

**最終更新:** 2026-05-23（作業開始時点）
**作業ブランチ:** main（こまめに commit & push）

---

## 1. 現在のステータス

| フェーズ | 状態 |
|---|---|
| 論文サーベイ（TBアルゴリズム・パラメータ抽出） | 進行中 |
| パラメータ JSON 化（出典付き） | 着手予定 |
| TB 計算エンジン実装 | 着手予定 |
| 論文値の再現テスト (V&V) | 着手予定 |
| ドキュメント整備 (docs/) | 着手予定 |
| バンド構造プロット出力 | 着手予定 |

---

## 2. 採用する論文とモデル（出典の明示）

ハルシネーション防止のため、すべてのモデル式・パラメータは以下の論文に出典を持ちます。

1. **Kashikar, Gupta, Nanda (2021)** "A Generic Slater-Koster Description of the
   Electronic Structure of Centrosymmetric Halide Perovskites", arXiv:2101.08562.
   → 立方晶 CsBX₃ 全9種の 13軌道・4軌道 SK-TB モデルとパラメータ表。
   **R点の固有値の解析式 (Eq. 9)** があり、実装の厳密検証に使える。

2. **Nestoklon (2021)** "Tight-binding description of inorganic lead halide
   perovskites in cubic phase", arXiv:2012.14705.
   → 立方晶 CsPbI₃ の sp³ / sp³d⁵s\* ETB パラメータ (Table I)。
   DFT バンドギャップ 1.017 eV、実験補正 1.65 eV (R点) / 2.75 eV (M点)、
   伝導帯 SO 分裂 1.48 eV など **明示された数値**で検証可能。

（補助）3. Ashhab et al. (2017) arXiv:1703.03574 — 鉛ハライドペロブスカイトの TB モデル。

---

## 3. 論文値の再現結果

> ここに、テストで確認できた「論文の数値 vs 本実装の計算値」を表で随時追記します。

（まだ計算結果はありません。実装・検証が進み次第ここに記載します。）

---

## 4. 参照論文の取り込み状況

- `references/pdfs/` に 49 本の arXiv 論文（自動収集）。`references/references.md` に一覧。
- うち 3 本（arxiv_2209.13267 / 2302.13773 / 2501.06503）は**ダウンロードが途中で切れた破損ファイル**で
  現時点では読めません（"Stream has ended unexpectedly"）。自動収集で再取得され次第、再確認します。
  - 特に **2501.06503**（"DFT-Leveraged Tight-binding Insights into Inorganic Halide Perovskites"）は
    関連性が高いため、再取得後に優先確認します。

---

## 5. 次にやること

1. パラメータ表を出典付き JSON 化（`data/parameters/`）。
2. Slater-Koster 二中心積分エンジン + Kashikar 13/4 軌道モデルを実装。
3. Eq. 9 を再現する単体テストを通す。
4. Nestoklon モデルを実装し、1.017 / 1.65 / 2.75 / 1.48 eV を再現確認。
5. docs/ の永続ドキュメントを整備（自己レビュー2回で承認）。
