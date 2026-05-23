# 初回実装 タスクリスト (tasklist)

**作業ID:** 20260523-initial-implementation
凡例: [x] 完了 / [~] 進行中 / [ ] 未着手

## 論文調査・パラメータ抽出
- [x] 49本を機械スクリーニングし TB/パラメータ明示の論文を特定
- [x] Kashikar Table II/IV、Nestoklon Table I を出典付き JSON 化（誤植は注記）
- [x] `data/parameters/SOURCES.md` に出典・検証アンカーを記録

## 実装（コア）
- [x] `_soc.py`: p軌道 L·S（Δ/3規約 = 3λ分裂）
- [x] `models_kashikar.py`: 13/4軌道ハミルトニアン + Eq.9解析式
- [x] `kpath.py` / `io_params.py` / `models.py` / `bandstructure.py`
- [x] `plotting.py` / `cli.py` / `_meta.py`
- [x] `slater_koster.py`: 一般SK二中心積分（s,p,d,s\*）
- [x] `models_nestoklon.py`: sp³ / sp³d⁵s\* ペロブスカイトハミルトニアン

## 検証 (V&V) — 163 テスト全通過
- [x] Eq.9 R点固有値の機械精度一致（全9材料）
- [x] SOC L·S 固有値・分裂=3λ
- [x] 4軌道ギャップ閉形式
- [x] SK二中心積分の軸方向手計算照合・パリティ対称性（106テスト）
- [x] Nestoklon: R点 1.0166（DFT, 目標1.017）/ 実験補正 1.6500・2.7549 / SO分裂 1.469 eV

## 出力・ドキュメント
- [x] Kashikar 全9材料のバンド図 + 再現性メタデータ JSON
- [x] Nestoklon CsPbI₃ バンド図（sp³ / sp³d⁵s\* / 実験補正）
- [x] `docs/` 永続ドキュメント9本（自己レビュー2回クリアで承認）
- [x] `RESULTS.md` に再現結果を反映
- [x] `scripts/screen_papers.py`（論文の定期チェック）, `scripts/generate_all_bands.py`

## 完了条件 — すべて達成
- [x] 全 V&V テストが通る（論文値を許容誤差内で再現）
- [x] `pytest` 全通過、CLI で JSON 入力からバンド図が生成できる
- [x] ドキュメントが揃い、出典が明示されている
