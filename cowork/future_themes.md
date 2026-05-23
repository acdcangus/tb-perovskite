# Future Themes — 全部終わった場合の次のネタ

**発行:** Cowork, 2026-05-23 14:50
**契機:** PI 不在中（10 時間）に既存タスクキューが全て完了した場合の次の作業
**前提:** Theme F F4-F6、Theme A 報告書磨き、Production 化、古典 16 本コピーが全て完了済み

以下のテーマは **既存のインフラ（velocity operator, Roth-Lax, k·p 公式, sum-over-states）を再利用** できる軽量拡張です。Claude Code の判断で着手 OK。各テーマは独立に進められます。

---

## 🎯 Theme H — Anomalous Hall / Spin Hall conductivity（Berry curvature 系）

### 動機
shift current (Theme F) と同じ **Berry connection の枠組み** で、もう一段大事な観測量が出せる：

- **Anomalous Hall conductivity (AHC)** σ_xy^AH（時間反転対称性破れで発生）
- **Spin Hall conductivity (SHC)** σ_xy^SH（時間反転対称性下でも発生、TI / Rashba 系で大きい）

CsBX₃ 立方相は中心対称・非磁性なので AHC = 0、SHC ≠ 0 になり得る。**鉛フリーで強い SHC は新しい物理**。

### 文献根拠
- **Xiao, Chang, Niu 2010** Rev. Mod. Phys. 82, 1959 — Berry phase レビュー（Berry curvature の解析的表現）
- **Sinova et al. 2015** Rev. Mod. Phys. 87, 1213 — Spin Hall effect レビュー
- 既存 `references/pdfs/` の topology papers (1704.04211, 1811.11081, 2302.13773) — 関連

### 実装
- 既存 `velocity.py` の `velocity_operator` を再利用
- Berry curvature Ω_n(k) を Kubo 公式（Fukui-Hatsugai-Suzuki 法 or 解析的）で計算
- BZ 積分 → σ_xy

新規コード: 300-400 行（`src/perovskite_tb/hall_conductivity.py`）

### 期待される新規性
- 9 材料 SHC マップ（Pb 中心の文献を Sn/Ge へ拡張）
- SOC の B サイト依存性が SHC にどう効くか

### 報告書
`reports/theme_H_hall_conductivity.md`

---

## 🎯 Theme I — Exciton binding energy via Wannier-Mott + TB

### 動機
ハライドペロブスカイトの光学物性で **励起子結合エネルギー** は重要な観測量（実験で数 meV〜数百 meV）。

既存 TB から effective mass を出し、**Wannier-Mott 公式** で励起子結合エネルギーを推定：
```
E_b = (μ/m₀)(1/ε_r²) × Ry∞     (Ry∞ = 13.6 eV)
1/μ = 1/m_e + 1/m_h
```

Phase 1.5 で既に ε(ω) → ε_r が出ているので、合わせて E_b が出る。

### 文献根拠
- **Yang et al. 2017** PRB 96, 035301 — halide perovskite の Wannier-Mott
- **Tanaka et al. 2003** Solid State Comm. 127, 619 — 励起子結合エネルギーの実験
- 既存 1908.09436 (Cho 2019 GW-BSE), 2210.01324 (nanocrystals)

### 実装
- 既存 band 計算から effective mass を抽出（Theme A の P 計算と同じ枠組み）
- ε_∞（Phase 1.5 の output）を入力
- E_b = (μ/m₀)(1/ε_∞²) × 13.6 eV

新規コード: 100-150 行（軽量）

### 期待される新規性
- 9 材料の E_b 系統マップ
- 実験との比較（Pb 系は知られている、Sn/Ge は実験値少ない）
- 鉛フリー LED 設計指針（E_b 大きい材料が明るく光る）

### 報告書
`reports/theme_I_exciton_binding.md`

---

## 🎯 Theme J — Circular Photogalvanic Effect (CPGE)

### 動機
Shift current (Theme F) は線偏光に応答。**CPGE は円偏光に応答**して直流電流を生成する別の現象。

- shift current: TRS 下でも生成可能、空間反転破れが条件
- CPGE: TRS 破れ または カイラル構造で生成
- 関連：chiral perovskite spin-LED（2026 Adv. Mater.）

### 文献根拠
- **de Juan et al. 2017** Nat. Commun. 8, 15995 — Weyl semimetal CPGE
- **Sipe-Shkrebtii 2000** PRB 61, 5337（既収集間接、Lan 2016 経由）
- 既存 `references/pdfs/arxiv_2309.14002.pdf` (Apergi 2023 chiral CD)

### 実装
- Theme F の `shift_current.py` の枠組みを拡張
- 円偏光の電場（左/右回り）に対する j^c = β·E×E* の計算
- 立方無歪み → 0、空間反転破り（歪み）で非ゼロ

新規コード: 200-300 行

### 期待される新規性
- 9 材料の CPGE 系統スキャン
- Theme F (shift) と Theme J (CPGE) の対称性比較
- カイラル拡張（Theme D 統合）への準備

### 報告書
`reports/theme_J_cpge.md`

---

## 🎯 Theme K — Layer-dependent g-factor for 2D Ruddlesden-Popper

### 動機
**Kopteva 2026 (arXiv:2605.15807) が実験で測定済み**：2D RP ハライドペロブスカイトの n=1,2,3,4 層構造の g 因子。

理論との照合を求められているが、まだ系統的計算は出ていない。**本研究の TB エンジンを 2D RP に拡張**する自然な次ステップ。

### 文献根拠
- **既収集 2605.15807** (Kopteva 2026) — 実験データ
- **既収集 2305.10586** (Nestoklon 2023) — Pb ナノ結晶の枠組み
- **既収集 1908.09436** (Cho 2019) — TB-GW-BSE の 2D 層状

### 実装
- 既存の立方 CsPbI3 sp³d⁵s\* を **n 層スラブ**に拡張（z 方向有限、x/y 周期）
- 層数 n=1,2,3,4 で k·p 公式の Eg, Δ を抽出
- g 因子計算（既存モジュール）

実装規模：800-1000 行（やや重い、PI 起床後に着手判断推奨）

### 期待される新規性
- Kopteva 2026 実験との直接照合（理論パート）
- 鉛フリー（Sn/Ge）2D RP 予測

### 報告書
`reports/theme_K_2D_RP_g_factor.md`

---

## 🎯 Theme L — Carrier mobility (Fröhlich polaron, Theme G の本格化)

既に v2 directive で Theme G として保留中だが、上記が全て終わったら着手。

### 文献根拠
- **Frost 2017** PRB 96, 195202 — Halide perovskite Fröhlich
- 既存 2105.06525 (Abramovitch 2021)

### 実装
- effective mass（Theme I の output と共有）
- LO フォノンエネルギー ω_LO（文献値）
- Fröhlich 結合定数 α
- μ_FH(T)

### 報告書
`reports/theme_L_mobility.md`

---

## 📋 推奨順序（軽い → 重い）

1. **Theme I (Exciton binding)** — 100-150 行、即実装可能、軽い
2. **Theme H (Berry curvature, Hall)** — 300-400 行、velocity op 再利用
3. **Theme J (CPGE)** — 200-300 行、Theme F の自然な拡張
4. **Theme L (Mobility)** — 中規模、文献調査必要
5. **Theme K (2D RP g-factor)** — 重い、PI 判断後

各テーマ完了で報告書 1 本 + reports/ 追加。

---

## 💡 共通する物理的視点

これらは全て **同じ物理エンジン（TB Hamiltonian + velocity operator + Berry connection）の異なる射影** です。論文化したら：

- Theme A (g 因子) + Theme F (shift current) + Theme H (Hall) + Theme J (CPGE) + Theme I (exciton)

を **「Lead-free halide perovskites: a tight-binding suite」** という統一的レビュー論文（Phys. Rep. or RMP）に纏める道も拓けます。

---

## ⚠️ Production モード強制

これらすべて **`PRODUCTION_RULES.md` 準拠**で実施してください：
- 収束確認 3 段階
- MANIFEST.json
- 入力ファイル一式
- `results/production/<theme>/<date>_<hash>/`

---

## 🚨 行き詰まったら

`cowork/progress/.../BLOCKED_<theme>.md` に書いて次のテーマへ。PI 起床後にレビュー・判断します。
