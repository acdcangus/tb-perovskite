# requirements — F4 Rashba / 中心反転破れスピン分裂

**発行元:** `extention/03_tb-perovskite_spec.md` F4
**日付:** 2026-05-24
**依存:** `berry.spin_operators`（スピン演算子）、`shift_current.make_polar_kashikar13_builders`（spinful P4mm, SOC 込み, delta=0 で立方と bit 一致）。

## スコープ
- スピンテクスチャ ⟨S⟩(k)、線形 k スピン分裂係数 α_R の抽出。
- 立方→α_R=0（Kramers）、極性→α_R≠0 の対称性検証 + 解析 Rashba 模型での抽出検証。

## 引用（実在確認済み 2026-05-24, web）
| 文献 | 確認 |
|---|---|
| Bychkov, Rashba, JETP Lett. 39, 78 (1984) — Rashba H_R=α(σ×k)·ẑ | ✅（正準 Rashba 論文） |
| Niesner et al., PRL 117, 126401 (2016), DOI 10.1103/PhysRevLett.117.126401 (arXiv:1606.05867) — ペロブスカイト Rashba | ✅ |

## 受け入れ条件
- 解析 2 バンド Rashba で α_R を厳密回復、spin ⊥ k。
- 立方 CsBX₃ → 分裂 0（<1e-6, Kramers）。
- 極性 CsBX₃（δ=0.4 Å）→ 分裂 >1e-4、Γ で 0、|k| 増大で増大。
- 既存テスト不変。

## honest 限界
α_R 絶対値はベンチ不整合（文献=表面 Rashba, 本=バルク極性）+ Blount → 対称性・spin-momentum locking・相対のみ信頼。

## 結果
- `src/perovskite_tb/rashba.py` + `tests/test_rashba.py`（8 ケース, green）。docs §12, repository-structure 更新。
