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
- [~] `models_nestoklon.py`: sp³ / sp³d⁵s\* ペロブスカイトハミルトニアン

## 検証 (V&V)
- [x] Eq.9 R点固有値の機械精度一致（全9材料）
- [x] SOC L·S 固有値・分裂=3λ
- [x] 4軌道ギャップ閉形式
- [ ] SK二中心積分の軸方向手計算照合・パリティ対称性
- [ ] Nestoklon: R点ギャップ 1.017 eV（DFTセット）/ 実験補正 1.65・2.75 eV / SO分裂 1.48 eV

## 出力・ドキュメント
- [x] Kashikar 全9材料のバンド図 + 再現性メタデータ JSON
- [ ] Nestoklon CsPbI₃ バンド図（DFT/実験補正セット）
- [ ] `docs/` 永続ドキュメント9本（自己レビュー2回で承認）
- [~] `RESULTS.md` に再現結果を随時反映

## 完了条件
- 全 V&V テストが通る（論文値を許容誤差内で再現）
- `pytest` 全通過、CLI で JSON 入力からバンド図が生成できる
- ドキュメントが揃い、出典が明示されている
