# Theme A5 (Phase 1.5): 立方晶 CsBX₃ の光学応答（複素誘電関数）

**ステータス:** 部分完了（B1-B5 実装・検証・9材料スキャン済み、draft v1。Cowork レビュー待ち）
**実施期間:** 2026-05-23
**コミット範囲:** 11ba555 .. (本コミット)

## 1. 動機
g因子（Theme A）と同じ TB Hamiltonian + velocity operator から、立方晶 CsBX₃ の
複素誘電関数 ε(ω)・吸収 α(ω)・屈折率を独立粒子近似で計算し、9材料を系統比較する。
光デバイス（吸収端・屈折率）の設計指標。励起子効果は含めない（将来 BSE 拡張）。

## 2. 方法
- ε_i: Apergi 2023 (arXiv:2309.14002) Eq.(3),(4)。**ED 項の速度行列要素 = `velocity.py` の ∂H/∂k**
  を再利用（Theme A と同一インフラ）。ε_r は Kramers-Kronig。`src/perovskite_tb/optical.py`。
- k 積分: Monkhorst-Pack。Lorentzian smearing η。前因子 πe²/ε₀=568.4 eV·Å（次元解析・f-sum で検証）。
- 出典: Apergi 2023; Cho 2019 (arXiv:1908.09436); Blount 1962 (Phys. Rev. 126, 1636)。

## 3. 主要結果
### 3.1 検証（`tests/test_optical.py`, 4 通過）
- **吸収端 = バンドギャップ**: CsPbI₃ で ε_2,α が Eg=1.65 eV 直上に立ち上がる。
  収束研究（`results/optical/convergence.md`）で **k 細分化により吸収端→Eg に収束**
  （6³→2.3, 8³→2.0, 12³→1.8 eV）。
- **立方等方** ε_xx=ε_yy=ε_zz（~1e-9）。**KK 整合**。
- **f-sum rule ~0.21**（k,η に対し安定）→ **Blount 1962 の TB 不完全性**（intra-atomic 電流欠落、
  g因子 Roth-Lax 過小評価と同根）。絶対強度・ε_∞ は系統的に過小。改竄せず記録。

### 3.2 9材料スキャン（`results/optical/9material_optical_summary.csv`, `9material_eps_imag.png`）
| 量 | 傾向 |
|---|---|
| 吸収端 | 各材料の TB ギャップを追従（mBJ ギャップは小さめ） |
| ε_∞ | **ギャップと逆相関**（小ギャップほど大）。CsGeI₃ 4.67, CsSnI₃ 4.70 が最大 |
| **ε_∞ 順序** | **CsPbI₃(3.46) > CsPbBr₃(2.35) > CsPbCl₃(1.46)** ← 実験/DFT の傾向と一致 ✅ |

→ **相対傾向（ε_∞ の B,X 依存・ハロゲン順序）は実験と整合**。絶対値は TB-IPA + Blount 不完全性で過小。

## 4. 論文値との比較
- ε_∞ の**ハロゲン順序 I>Br>Cl** は実験/DFT と一致（Cowork 推奨ベンチマーク合格）。
- 絶対 ε_∞（~1.5-4.7）は実験 ~5-6 より過小 → f-sum ~20% と整合（Blount 1962）。
- 吸収係数 α は可視〜近 UV で ~10⁵ cm⁻¹ オーダー（高エネルギー側）→ 文献オーダーと整合。

## 5. 物理的考察
- ε_∞ ∝ 1/Eg（小ギャップ・重ハロゲンほど分極率大）は標準的な傾向で、本 TB-IPA が
  **相対傾向を正しく再現**することを示す。
- 絶対強度の過小は Blount 1962 の TB position operator 不完全性（Theme A の g因子と統一的）。
  → **TB-IPA は「端・形状・相対傾向は信頼可、絶対量は過小」**という一貫した適用範囲。

## 6. 学会・論文化の見通し
- Theme A（g因子）と統合し、「**TB 法による CsBX₃ の磁気光学・光学物性の系統予測と、
  その適用限界（Blount 1962）の定量化**」として 1 本にまとめられる。
- 光学単独でも「鉛フリー Sn/Ge の吸収端・誘電率マップ」は光デバイス設計に有用。

## 7. 限界・残課題
- 励起子効果なし（独立粒子）。Wannier-Mott / 簡易 BSE 拡張は将来。
- 絶対強度・ε_∞ は Blount 不完全性で過小（Wannier ベース position operator が要）。
- Kashikar の mBJ ギャップは小さめ。realistic gap での再評価は Theme A の Eg データで可能。
- 3D 無機立方の直接論文アンカーが弱い（Cowork が実験 ε(ω) 文献を調査中）。

## 8. 再現コマンド
```bash
PYTHONPATH=src python scripts/scan_optical.py            # CsPbI3 (Nestoklon)
PYTHONPATH=src python scripts/optical_convergence.py     # B4 収束
PYTHONPATH=src python scripts/scan_optical_9materials.py # B5 9材料
PYTHONPATH=src python -m pytest tests/test_optical.py -q
```

## 9. 関連ファイル
- **Production バンドル（数値の典拠）:** `results/production/phase_1.5_optical/2026-05-23_31374dc/MANIFEST.json`
  （ε_∞ 順序・f-sum・吸収端等は `key_numbers`、収束は `convergence` フィールド/`raw/convergence.md`）
- 定式化: `docs/optical-formulation.md`、実装: `src/perovskite_tb/optical.py`
- データ/図: `results/optical/`（`9material_optical_summary.csv`, `convergence.md`, `*_dielectric.png`, `9material_eps_imag.png`）
- テスト: `tests/test_optical.py`
