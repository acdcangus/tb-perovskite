# 拡張機能 F1（Berry 曲率 → AHC/SHC）実装完了 — Claude Code — 2026-05-24 16:10

PI 依頼「`extention/` の拡張機能仕様を熟読・検討し、拡張可能なら実装（標準ルール準拠・ハルシネーション厳禁・
承認不要で完了まで独自に）」に対応。

## 方針（最初に確定）
`extention/03_tb-perovskite_spec.md` は F1–F14 の多月規模ロードマップ。**paper-quality + フル V&V + ハルシネーションゼロ**で
完遂できる単位として、handoff (`07_agent_handoff.md`) の最優先 **Phase A = F1（Berry 曲率コア → AHC + SHC）** を実装。
理由: (1) 最優先, (2) 既存 velocity.py の上に構築, (3) 全引用が実在確認済み, (4) 解析解 V&V が明快。F2–F14 は roadmap 化（`.steering/20260524-berry-curvature-shc/tasklist.md`）。

## ハルシネーション防止（実施）
全引用を着手前に web 検証（handoff サイクル A）:
- Xiao, Chang, Niu, RMP 82, 1959 (2010) — **ar5iv で Eq.(1.13) 本文確認**、Kubo 規約で下バンド Dirac Ω₋=+m/(2|d|³) を当方で解析導出。
- Fukui, Hatsugai, Suzuki, JPSJ 74, 1674 (2005) — 離散 link 法。
- Sinova et al., RMP 87, 1213 (2015) — スピン流演算子 j=½{s,v}。
- Qi, Wu, Zhang, PRB 74, 085308 (2006) — QWZ テスト模型。
4 件すべて実在・OA 確認済み（DOI/arXiv 一致）。記憶ベースの式・数値は不使用。

## 成果物
- `src/perovskite_tb/berry.py`（SPDX, 出典付き docstring）: Berry 曲率(Kubo)・スピン Berry 曲率・離散 Chern(Fukui)・AHC/SHC 和・スピン演算子・Kashikar-13 ヘルパ。
- `tests/test_berry.py`（**22 ケース**）。
- `docs/numerical-methods.md` §9、`docs/repository-structure.md` 更新（CLAUDE.md 準拠）。
- `.steering/20260524-berry-curvature-shc/`（requirements/design/tasklist）。

## V&V 結果（paper-quality 基準）
- **解析解一致**: 質量 Dirac 下バンド Ω₋ = +m/(2(k²+m²)^{3/2}) に rtol 1e-6 で一致（符号・係数を実証）。
- **整数 Chern**: QWZ で Fukui 法が整数、|C|=1 (|u|<2)・u=0 符号反転・|u|>2 で 0（相図）。
- **2 手法相互一致**: Kubo BZ 和 ≈ Fukui Chern。
- **対称性**: 立方 CsBX₃（CsPbI₃/CsSnI₃/CsGeCl₃, SOC on）で **AHC=0 を ~1e-15** で確認（P·T）。
- **代数**: スピン演算子 [Sx,Sy]=iSz, Sz²=¼I; スピン流エルミート性。
- **回帰**: `pytest` 全体 **253 passed**（既存 231 不変 + 新規 22）。

## 実装中に発見・解決した非自明点（記録）
1. Fukui Chern の符号: 連続極限導出（A=i⟨u|∂u⟩ ⇒ Im ln(plaquette)→−Ω dk²）より C=−(1/2π)Σ に補正し Kubo と整合。
2. 立方ペロブスカイトの 0.96 eV halide-p **flat band**（多重縮退）が固定バンド数の占有を割る → AHC 検証は**実ギャップ内 Fermi 準位**で占有選択（縮退多重項を割らない）に変更。

## honest な限界（明記）
- SHC の**絶対値**は in-repo にベンチ材料（Pt 等）が無く未検証 → 相対・対称性・構造のみ信頼（g 因子/shift current と同じ立場）。Blount 限界も併記。
- 9 材料 SHC production スキャン（spec F1 novelty）は任意 follow-up。本コミットは検証済みコア基盤 + V&V。

## 次
- 同セッションで継続検討: F2（topology, Wilson loop/Z₂）= berry.py の Fukui 基盤を再利用、handoff Phase B。着手前に Fu-Kane 2007 / Yu 2011 / Soluyanov-Vanderbilt 2011 の DOI を web 検証する。
