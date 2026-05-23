# 検証・妥当性確認 (V&V) 計画書

「**コードが意図通り方程式を解いているか (Verification)**」と
「**モデルが論文/現実を再現するか (Validation)**」を区別して管理する。
すべて `tests/` の自動テストに対応し、`pytest` で再現できる（現状 **163 テスト全通過**）。

---

## A. Verification（検証）— 実装の正しさ

### A-1. Slater-Koster 二中心積分 (`tests/test_slater_koster.py`)
- 軸方向 `(1,0,0)` の行列要素を Slater-Koster (1954) Table I から**手計算**した値と照合
  （s-s, s-p, s-d, p-p, p-d, d-d）。
- 基本関係 `E_{αβ}(\mathbf d) = E_{βα}(-\mathbf d)` を全軌道対（100通り）で確認。
- s\* が s と同じ角度形を持つことを確認。

### A-2. スピン軌道相互作用 (`tests/test_soc.py`)
- `λL·S` の固有値が `{+λ/2 (×4), -λ (×2)}`、トレース 0、Hermite。
- Δ/3 規約で p 分裂が `3λ` になること。

### A-3. Kashikar 13軌道 — 解析式との一致 (`tests/test_kashikar.py`)
- **R点で数値対角化した固有値が解析式 Eq.(9) と一致**（全9材料、許容 1e-10 eV、
  実測 ~1e-15）。縮退構造 `{1,8,3,1}` も確認。これは SK 構築・ジオメトリ・ゲージの
  独立検証であり、ハルシネーション排除の中核。
- 一般 k で Hermite。
- 伝導帯 SO 分裂（R点）= `3λ`。

### A-4. Kashikar 4軌道 (`tests/test_kashikar.py`)
- SOC なしギャップ閉形式 `E_g = ε_p-ε_s-2t_{ppσ}-4t_{ppπ}+6t_{ss}` と数値対角化の一致。

### A-5. Nestoklon Hermite 性 (`tests/test_nestoklon.py`)
- 一般 k で 80×80 Hamiltonian が Hermite。

> 数値手法は固有値問題であり、CFL 等の時間積分安定性条件は無い。保存則の検証は
> 本スコープでは対象外（電子バンドのみ）。誤差要因は丸めと k 離散化
> （[numerical-methods.md](numerical-methods.md) §7）。

---

## B. Validation（妥当性確認）— 論文値の再現

### B-1. Nestoklon CsPbI₃ (`tests/test_nestoklon.py`, arXiv:2012.14705)

| 検証項目 | 論文値 | 本実装 | 許容 | 判定 |
|---|---|---|---|---|
| sp³ R点ギャップ (DFT) | 1.017 eV | 1.0182 | ±0.01 | ✅ |
| sp³d⁵s\* R点ギャップ (DFT) | 1.017 eV | 1.0166 | ±0.01 | ✅ |
| sp³d⁵s\* 伝導帯 SO 分裂 (R) | 1.48 eV | 1.469 | ±0.03 | ✅ |
| 実験補正 R点ギャップ | 1.65 eV | 1.6500 | ±0.01 | ✅ |
| 実験補正 M点ギャップ | 2.75 eV | 2.7549 | ±0.02 | ✅ |
| 直接ギャップが R 点 | (そう) | R で直接 | — | ✅ |

バンド図 (`results/nestoklon/CsPbI3_sp3d5sstar.png`) は Nestoklon Fig.2 と一致
（I-s 深部帯 ~-13.4 eV、Pb-s 結合帯 ~-7.7 eV、Pb-p 伝導帯、d/s\* 高エネルギー帯）。

### B-2. Kashikar CsBX₃ (arXiv:2101.08562)
- A-3/A-4 の解析式一致が妥当性確認も兼ねる（論文が導出した式の再現）。
- 9材料の R点直接ギャップ傾向（Cl→Br→I で減少、Sn 最小）を再現（[RESULTS.md](../RESULTS.md)）。
- CsPbI₃ 伝導帯 SO 分裂 1.50 eV が Nestoklon の 1.48 eV と整合（論文間整合）。

---

## C. 受け入れ基準

- すべての V&V テストが許容誤差内で通過すること。
- 論文の解析式に対しては機械精度（≤ 1e-9 eV）。
- 明示されたギャップ・SO 分裂に対しては ≤ 10〜30 meV。
- `pytest` 全通過、CLI で JSON 入力からバンド図と再現性メタデータが生成できること。

## D. 定期回帰

- パラメータ JSON・実装の変更時は `pytest` を再実行し全通過を維持。
- 新規論文が `references/` に追加されたら、TB モデル/パラメータの有無を確認し、
  該当すればパラメータ JSON と検証テストを追加する。

## E. 既知の限界（Validation スコープ外）

- 低対称相（正方/斜方）、表面・ナノ構造、歪み、励起子・光学応答は未検証・未実装。
- Nestoklon は最近接モデルゆえ、`-3〜-2 eV` の一部平坦価電子帯は原論文同様に
  厳密再現できない（第二近接や SK 一般化が必要、原論文 §III.B 記載）。
- Kashikar の一部パラメータに符号の誤植が疑われる（`SOURCES.md` 注記）。値は改変せず、
  Eq.9 検証はパラメータ値に依存しないため実装の正しさには影響しない。
