# 論文骨子初稿: Theme I — Exciton binding energies of cubic CsBX₃ from TB effective masses + Materials Project DFPT dielectrics

**ステータス:** 骨子初稿（清書は後日）。PI directive `2026-05-24_1145_directive_PI_decisions.md` Part 1 T1-c。
**投稿候補:** npj Computational Materials / Physical Review Materials / J. Phys. Chem. C（いずれも計算物性 + ペロブスカイト光物性に適合）。

---

## Abstract（~200 字）
立方ハライドペロブスカイト CsBX₃（B=Ge/Sn/Pb, X=Cl/Br/I）の励起子結合エネルギー E_b を、tight-binding（Kashikar-13）
TB（Kashikar 2021 の 13 軌道 active basis）有効質量と Materials Project の DFPT 高周波誘電率 ε∞ を組み合わせた Wannier-Mott 模型で系統評価。誤差源を μ（TB）と
ε∞（外部 DFPT, 単一手法）に分離。E_b は Cl 系で最大（CsPbCl₃ 119 meV）、Sn-I で最小（CsSnI₃ 4 meV）。bare ε∞ 由来で
絶対値は上限だが相対トレンドは頑健。CsPbI₃ は実効 ε≈6.1 で E_b=22 meV と実験整合し校正点を与える。LED（大 E_b）/
太陽電池（小 E_b）の材料選択指針を提示。

## 1. Introduction（~250 字）
- 励起子結合エネルギーのデバイス的意義（LED 発光 vs 太陽電池キャリア分離）。
- 既存研究: Pb 系の実験/GW-BSE（Cho 2019 等）はあるが、鉛フリー Sn/Ge 含む 9 材料の consistent な系統比較は不足。
- 課題: Wannier-Mott の遮蔽 ε の取り方（bare ε∞ vs 実効 ε_eff）が絶対値を大きく左右し、文献値は手法・相がばらつく。
- 本研究の狙い: μ=TB / ε=単一手法 DFPT に分離した hybrid で defensible な相対トレンドを与え、bare ε∞ の限界を定量化。

## 2. Methods（~300 字）
- **TB 有効質量**: Kashikar-13 sp 基底, R 点（直接ギャップ端）バンド曲率 m*/m₀=(ℏ²/m₀)/(d²E/dk²)、3 軸平均（立方等方）。
- **誘電率**: Materials Project DFPT bare ε∞（mp-api, 8/9 材料）。一部材料は基底状態相由来（相を明記、~相非依存 proxy）。
- **Wannier-Mott**: E_b=(μ/m₀)/ε_r²·Ry。校正に Cho 2019 の CsPbI₃ 実効 ε≈6.1。
- 再現性: 全 Production bundle（MANIFEST, git_dirty:false）、収束（dk, 方向異方性）、乱数なし。

## 3. Results（~250 字）
- 有効質量マップ（表 + Eg 依存）: Cl→Br→I 軽量化、Sn 系最軽（μ: 0.015–0.116）。
- E_b マップ（C', 8 材料, 表 + 図）: CsPbCl₃ 119 > … > CsSnI₃ 4 meV。相対トレンドは μ と ε∞ の競合で理解。
- 校正点（D'）: CsPbI₃ 実効 ε で 22 meV、実験 7.4–50 meV (Cho 2019) の範囲内（C' bare 41 meV の ~1.9× 補正）。

## 4. Discussion（~300 字）
- **bare ε∞ vs 実効 ε_eff**: Wannier-Mott は ε_eff（フォノン込み）を要するが文献は bare ε∞ を報告 → E_b 過大。定量化。
- **Blount 統一限界**: TB 位置演算子の原子内成分欠落が g 因子・光学 f-sum・本 ε∞ 過小に共通（同研究群の横断的知見）。
- 相依存・MP データ可用性（CsSnCl₃ 欠落）の限界と、Wannier 化 / GW-BSE / 実験 ε_eff による改善の道筋。
- デバイス含意: E_b 大（Cl, Pb/Ge）→ 発光、小（Sn-I）→ 光起電。

## 5. Conclusion（~150 字）
9 材料の defensible な E_b 相対トレンドと有効質量マップを提示。bare ε∞ の系統的上限性を honest に定量化し、
実効 ε による校正点で実験整合を示した。鉛フリー光デバイス材料選択の計算指針。

## 6. References（主要）
- Tanaka 2003 SSC 127, 619（巻号確認済; MAPbBr₃/MAPbI₃ 励起子, CsPbCl₃ ではない）。Wannier-Mott 適用例（Yang 2017 PRB 96 035301 は要原典確認・web 未確認）
- Cho 2019 arXiv:1908.09436（GW-BSE, 実効 ε）
- Jain 2013 APL Mater. 1 011002（Materials Project）
- Kashikar 2021 arXiv:2101.08562（TB, 13 軌道 active basis）; Blount 1962 PR 126 1636（TB 限界; in-repo 外）
- Kirstein et al. arXiv:2112.15384, in-repo（g 因子 Eg 普遍関係, 同材料群の関連）

## 既存ドキュメントとの差分（学術論文ならでは）
- 技術報告書 `theme_I_exciton.md`: 実装・bundle 中心。PI 解説 `PI_explained_theme_I.md`: 非専門向け。
- 本骨子: **先行研究レビュー + novelty 明示 + 図表の論文体裁 + 限界の学術的議論**を加える。novelty 判定は `cowork/novelty_assessment.md` 参照。
