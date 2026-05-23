# F3 escalation: shift-vector fails for Kramers-degenerate (SOC) bands — 2026-05-23 12:30

**対象:** `src/perovskite_tb/shift_current.py` (F3 v1, WIP), `tests/test_shift_current.py`
**急ぎ度:** 通常（F3 完遂のため Cowork の式検証を依頼）
**判定依頼:** 縮退バンドの shift vector（非アーベル化）の正しい離散表式

## 状況：何が validated で何が問題か
**Validated（テスト通過）:**
- Young & Rappe 2012 Eq.(1)-(3) の factorized 形（intensity × shift vector）の構造。
- **polar-displaced Nestoklon builder**: δ=0 で base Nestoklon builder と**ビット一致**
  （max|ΔH|=0, max|ΔdHdk|=2e-15）→ symmetry breaker 実装は正しい。δ>0 で反転対称破れ、TRS E(k)=E(-k) 維持。
- Harrison scaling `t(d)=t(d0)(d0/d)^2`（出典明記）。
- transition intensity `|⟨v|∂_zH|c⟩|²`（光学 ε₂ と同じ、I(+k)=I(-k) 確認済み）。

**問題（δ=0 で σ_zzz が消えない, |σ|~O(10) ≠ 0）:**
- 原因を切り分け済み: **バンドが Kramers 2 重縮退**（SOC）。
  固有値が完全に対で縮退（例: -2.0002×2, 3.5875×2, ...）。
- 縮退対の中で対角化器（numpy eigh）が**各 k で固有ベクトルを任意に混合**するため、
  私の **Abelian（バンド対角）shift vector** の link `⟨u_c(k+dk)|u_c(k)⟩` が無意味になり、
  R_z が破綻（R_z(+k)=123, R_z(-k)=3141 と巨大・非反対称; 本来 ~O(1 Å)・k→-k で奇関数のはず）。
- intensity は正しい（I(+k)=I(-k)）。**問題は shift vector のみ**。

## Cowork へのレビュー依頼（核心）
**縮退（Kramers）バンドに対する shift vector の正しい離散表式**を確認したい:
1. **非アーベル化（degenerate-subspace trace）**: 価電子縮退群 V・伝導縮退群 C について、
   `Σ_{v∈V,c∈C}` の和とし、link を 2×2（縮退ブロック）行列の det/trace で取る形。
   gauge-invariant な離散ループ表式（U(2) 縮退ブロック対応）の具体形を、Young&Rappe /
   Fregoso 2017 (arXiv:1701.00172, 取得済) / Passos 2018 (arXiv:1712.04924, 取得済) から
   照合して確定したい（紙ベース式展開の協力希望）。
2. または **velocity-gauge sum-over-states 形（Passos 2018）**に切替え、縮退を energy 分母で
   自然に扱う方が頑健か（その場合 generalized derivative の sum-over-states 公式の確認が要る）。

## 私の方針（no-hallucination 順守）
- δ=0 vanishing を満たさない現状を**改竄せず**、テストは `xfail(strict)` で明示記録（通れば即検知）。
- 正しい縮退表式が確定するまで σ_zzz の**数値結果は出さない**（推測実装しない）。
- builder/Harrison/intensity は validated なので、shift vector の縮退対応が決まれば即完遂可能。

## 参考（取得済 PDF）
- Young & Rappe 2012: arXiv:1202.3168（Eq.1-3, R_q=-∂_qφ-(χ_c-χ_v)）
- Fregoso 2017: arXiv:1701.00172（shift vector gauge-invariance）
- Passos 2018: arXiv:1712.04924（velocity gauge, covariant derivative, Blount 分解）
- Tan & Rappe 2016: doi_10.1038_npjcompumats.2016.26（縮退・SOC 系の扱いが Methods にある可能性 → 要精読）

## 状態
208 passed + 1 xfailed（既存 205 維持 + builder/Harrison 3 通過 + δ=0 xfail）。
