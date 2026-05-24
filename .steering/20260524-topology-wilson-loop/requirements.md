# requirements — F2 topology（Wilson ループ / WCC, 部分）

**発行元:** `extention/03_tb-perovskite_spec.md` F2（★★★, Phase B）
**日付:** 2026-05-24
**依存:** F1 `berry.py`（link 変数を再利用）

## スコープ（本作業 = paper-quality で検証可能な部分のみ）
- **実施:** 非アーベル Wilson ループ、Wannier 電荷中心 (WCC)、WCC/分極の巻き付き数＝Chern。
- **スキップ（ハルシネーション防止）:**
  - Fu-Kane parity Z₂ → Kashikar 基底の**空間反転演算子**が in-repo 情報から未確定（推測=捏造）→ 一次文献確定まで保留。
  - Soluyanov-Vanderbilt 時間反転 Z₂（partner switching）→ 検証用の既知 3D-Z₂ 模型が無い → 保留。
  PI 指示「文献が無ければスキップ可」に従う。

## 引用（実在確認済み 2026-05-24, web 検証）
| 文献 | 確認 |
|---|---|
| Yu, Qi, Bernevig, Fang, Dai, PRB 84, 075119 (2011), DOI 10.1103/PhysRevB.84.075119 (arXiv:1101.2011) | ✅ |
| Soluyanov, Vanderbilt, PRB 83, 235401 (2011), DOI 10.1103/PhysRevB.83.235401 (arXiv:1102.5600) | ✅ |
| Qi, Wu, Zhang, PRB 74, 085308 (2006)（QWZ 検証模型, F1 で確認済） | ✅ |

## 受け入れ条件
- **Wilson ループ Chern == Fukui plaquette Chern**（berry.py）= 2 独立手法の相互一致（整数）。
- QWZ 相図再現（|C|=1 内側 / 0 外側 / u=0 符号反転）。
- Wilson ループ unitary・分極位相 gauge 不変・WCC ∈ (−½,½]。
- 既存テスト不変（265 passed = 231 + 22 berry + 12 topology）。

## 結果
- `src/perovskite_tb/topology.py` + `tests/test_topology.py`（12 ケース, 全 green）。
- docs/numerical-methods.md §10, docs/repository-structure.md 更新。
