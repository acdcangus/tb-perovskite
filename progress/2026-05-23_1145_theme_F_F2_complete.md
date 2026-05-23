# Theme F F2 完了通知（formulation doc draft v1）— 2026-05-23 11:45

commit ddbdc1a。`docs/shift-current-formulation.md` draft v1。**F3（実装）は本 doc の
Cowork 承認待ち**（CLAUDE.md「1ファイルごと承認」）。205 テスト維持（エンジン変更なし）。

## F1 結果（PDF）
- ✅ **Passos 2018 (arXiv:1712.04924)** 取得・タイトル検証OK → F2 primary 方法論。
- ✅ **Sheikhabadi 2022 (arXiv:2207.00331)** 取得・検証OK（correction 1110 と一致）→ sub。
- ❌ **Cowork 提示の ID 1207.5462 / 1612.09194 は無関係論文**（統計 / billiards 数学）だった
  → 削除。**Young & Rappe 2012 / Fregoso 2017 の正しい PDF は Cowork 取得待ち**。
- ❌ Tan & Rappe 2016 未取得（検証アンカー用、OA のはず）。

## F2 で Cowork に確認したい点（レビューポイント）
1. **【重要・物理補正】symmetry breaker**: directive 推奨の **uniaxial strain は不適**。
   cubic Pm-3m に一軸歪み → 正方晶 P4/mmm（**依然 中心対称**）→ σ⁽²⁾ は依然ゼロ。
   shift current には**反転対称の破れ**が必須なので、**極性変位（Pb/Cs を [001] に off-center,
   → P4mm）を symmetry breaker に推奨**。この変更で良いか確認希望。
2. **SK 距離スケーリング指数 η_l**: 歪み下の hopping 修正 `t(d)=t(d₀)(d₀/d)^{η_l}` に必要だが
   Kashikar/Nestoklon は固定結合長で η を与えていない。Harrison 標準値採用か材料別フィットか、
   **出典確定まで F3 は保留**（推測しない）。
3. σ⁽²⁾ 式の符号規約を Young&Rappe/Sipe-Shkrebtii と照合（PDF 取得後）。Berry connection の
   n=m 除外・covariant derivative の k 有限差分 vs 解析の選択。

## 実装準備（F3, 承認後）
- Berry connection `r^a_{mn}=i⟨m|∂_aH|n⟩/(E_n-E_m)` は **velocity.py の ∂H/∂k 再利用**。
- covariant derivative は k 有限差分（Tan&Rappe 流）。
- 検証: **無歪み立方で σ⁽²⁾≈0**（ハルシネーションproof）、極性変位で発現、Tan&Rappe MAPbI₃ 照合。
- Blount 1962 統一ナラティブ継続（絶対振幅は過小の見込み）。

## 並行作業（F2 レビュー待ちの間）
- directive 2.2 の **Theme A 論文図 polish (b) ge_universality 2 段化**に着手予定
  （review #6 §4 で Cowork も提案）。完了後 commit + 報告。

## 次
- Cowork の F2 レビュー（symmetry breaker 補正の可否、η_l 出典）と Young&Rappe/Tan&Rappe PDF 待ち。
  承認 + 出典確定後に F3（`shift_current.py`）着手。
