# requirements — F7 CPGE / injection current

**発行元:** `extention/03_tb-perovskite_spec.md` F7
**日付:** 2026-05-24
**依存:** `berry`（Berry 曲率・velocity_matrix）。

## スコープ
- 円偏光 2 次注入電流テンソル β_ij（一般式 + 2 バンド Berry 曲率形）。絶対値は τ/規約依存でスコープ外。

## 引用（実在確認済み 2026-05-24, web。式は ar5iv 原典で精読）
| 文献 | 確認 |
|---|---|
| Sipe, Shkrebtii, PRB 61, 5337 (2000), DOI 10.1103/PhysRevB.61.5337 | ✅ |
| de Juan, Grushin, Morimoto, Moore, Nat. Commun. 8, 15995 (2017), DOI 10.1038/ncomms15995 (arXiv:1611.05887) | ✅ 式・量子化値を ar5iv で確認 |

原典式（de Juan, ar5iv 確認）:
β_ij = (πe³/ℏV) ε_jkl Σ f_nm Δ^i_nm r^k_nm r^l_mn δ(ℏω−E_mn), r^a_nm=−i v^a_nm/E_nm。
2 バンド: β_ij = (iπe³/ℏ²V) Σ ∂_i E_12 Ω^j_1 δ。Weyl 量子化: Tr[β]=iπ(e³/h²)C。

## 受け入れ条件
- 式の簡約: −Im(ε_jkl r^k_12 r^l_21)=Ω^j_1（一般式 ⇔ 2 バンド一致）。
- 中心反転（非縮退）→ β=0。
- Weyl: Tr[β] ω 非依存プラトー + chirality 符号反転 + |Tr|≈1/(4π)（~20%）。
- 既存テスト不変。

## 実装上の注意（記録）
- εrr は純虚数（=iΩ）→ Im を取り、Xiao（berry.py）規約に合わせ符号を −Im に固定（de Juan と Berry 曲率規約差を 2 バンド検証で整合）。当初 Re を取り 0 になるバグを発見・修正。
- 立方ペロブスカイト β=0 は Kramers gauge 問題回避のため非縮退中心反転模型で検証。

## 結果
- `src/perovskite_tb/cpge.py` + `tests/test_cpge.py`（4 ケース, green）。docs §14, repository-structure 更新。
