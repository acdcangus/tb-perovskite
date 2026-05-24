# tb-perovskite — 拡張機能 実装報告書

**作成日**: 2026-05-24
**実装者**: Claude Code（実装エージェント）
**対象仕様**: `03_tb-perovskite_spec.md`（F1–F14）+ `07_agent_handoff.md`（実装手順・ハルシネーション防止指針）
**リポジトリ**: `tb-perovskite`（既存 Slater–Koster / Jancu TB ペロブスカイトコード）

---

## 0. エグゼクティブサマリ

仕様書 `03_tb-perovskite_spec.md` の F1–F14 のうち、**現実時間で「文献グラウンディング + 厳密 V&V + 無捏造」を満たせる 12 feature-slot を実装完了**した（10 新モジュール、新規テスト 82、全 **313 passed**、既存 231 テスト不変）。

| 状態 | 機能 |
|---|---|
| ✅ 実装済み | F1, F2(部分), F4, F5, F6, F7, F9, F11, F12, F13, F14-A, F14-B |
| ⏸ 未実装（理由付き, §4） | F3 (BSE), F8 (SHG), F2 残 (Z₂ parity) |

すべて handoff §0–§2 のワークフロー（引用 DOI を事前 web 検証 → 原典式を精読 → 解析解/既知模型/位相量子化で V&V → `.steering/` + `docs/` 整備）に準拠。**引用 24+ 件すべて実在確認済み**。実装過程で**引用ミス 1 件を是正**（§3.2）。記憶ベースの式・数値はゼロ。

---

## 1. 実装機能一覧（feature-slot 別）

各機能: モジュール / 主要文献（実在確認済み）/ V&V アンカー / テスト数 / commit / honest 限界。
内部単位は仕様 §3 統一系（eV, Å, V/Å, Tesla, K）。既存 `velocity.py`（dH/dk）を共有基盤として再利用。

### F1 ★★★ Berry 曲率コア → AHC / SHC / 離散 Chern
- **モジュール**: `src/perovskite_tb/berry.py` / **テスト**: `tests/test_berry.py`（22）/ **commit**: `24fa03a`
- **文献**: Xiao-Chang-Niu, RMP 82, 1959 (2010)（Berry 曲率 Kubo 式 **Eq.(1.13)**, ar5iv 原典で確認）; Fukui-Hatsugai-Suzuki, JPSJ 74, 1674 (2005)（離散 link 法）; Sinova et al., RMP 87, 1213 (2015)（SHC, スピン流 j=½{s,v}）; Qi-Wu-Zhang, PRB 74, 085308 (2006)（QWZ テスト模型）
- **V&V**: 質量 Dirac 下バンド Ω₋=+m/2(k²+m²)^{3/2}（解析, 符号を自前導出）; QWZ 整数 Chern + 相図; Kubo↔Fukui 一致; 立方 CsBX₃ で **AHC=0 を ~1e-15**（P·T）; su(2) 代数
- **限界**: SHC の絶対値は in-repo ベンチ材料なく未検証 + Blount 限界 → 対称性・構造・相対のみ信頼

### F2 ★★★（部分）Wilson ループ / Wannier 電荷中心 (WCC)
- **モジュール**: `src/perovskite_tb/topology.py` / **テスト**: `tests/test_topology.py`（12）/ **commit**: `981f1f8`
- **文献**: Yu-Qi-Bernevig-Fang-Dai, PRB 84, 075119 (2011); Soluyanov-Vanderbilt, PRB 83, 235401 (2011)
- **V&V**: **Wilson ループ Chern == Fukui plaquette Chern**（2 独立手法一致, QWZ）; 相図; Wilson 行列 unitary 性; 分極位相 gauge 不変
- **未実装（意図的, §4）**: Fu-Kane parity Z₂ / 時間反転 Z₂

### F9 ★ Boltzmann 熱電輸送（CRTA）
- **モジュール**: `src/perovskite_tb/thermo.py` / **テスト**: `tests/test_thermo.py`（6）/ **commit**: `6773898`
- **文献**: Madsen-Singh, Comp. Phys. Commun. 175, 67 (2006)（BoltzTraP）
- **V&V**: **Wiedemann-Franz** Lorenz数 → π²/3 (k_B/e)²（縮退極限, rtol 0.5%, バンド非依存厳密則）; Sommerfeld Seebeck; 正孔 S>0; Σ∝ε^{3/2}
- **限界**: 絶対 σ/κ_e は緩和時間 τ（材料・散乱依存）が必要でスコープ外 → 相対値・比のみ

### F4 ★★ Rashba スピン分裂
- **モジュール**: `src/perovskite_tb/rashba.py` / **テスト**: `tests/test_rashba.py`（8）/ **commit**: `188d28d`
- **文献**: Bychkov-Rashba, JETP Lett. 39, 78 (1984); Niesner et al., PRL 117, 126401 (2016)
- **V&V**: 解析 2 バンド Rashba で α_R を厳密回復 + spin⊥k; 立方 CsBX₃ → 分裂 0（Kramers）; 極性 (P4mm) → 分裂あり, Γ で消失, |k| 増大
- **限界**: α_R 絶対値はベンチ不整合（文献=表面 Rashba, 本=バルク極性）+ Blount → 対称性・spin-momentum locking のみ信頼

### F11 ★★ Edelstein 効果（電流誘起スピン分極）
- **モジュール**: `src/perovskite_tb/edelstein.py` / **テスト**: `tests/test_edelstein.py`（4）/ **commit**: `b3e2b99`
- **文献**: Edelstein, Solid State Commun. 73, 233 (1990)
- **V&V**: 中心反転（非縮退）模型 → χ=0; Rashba 模型 → 直交応答 χ_yx≠0, χ_xx≪χ_yx; χ_yx(−α)=−χ_yx(α)
- **限界**: per-band 公式は非縮退バンド前提（立方 Kramers は極性相で評価）; 絶対値は τ 依存

### F7 ★★ 円偏光光起電力効果 (CPGE) / injection current
- **モジュール**: `src/perovskite_tb/cpge.py` / **テスト**: `tests/test_cpge.py`（4）/ **commit**: `92b2ac5`
- **文献**: Sipe-Shkrebtii, PRB 61, 5337 (2000); de Juan-Grushin-Morimoto-Moore, Nat. Commun. 8, 15995 (2017)（式・量子化値を ar5iv 原典で確認）
- **V&V**: de Juan 式簡約 −Im(ε_jkl r^k r^l)=Ω^j（一般式 == 2 バンド形）; 中心反転→0; **Weyl 量子化**（Tr[β] が ω 非依存プラトー + chirality 符号反転 + |Tr|≈πe³/h²=1/4π を 20% で数値再現）
- **限界**: 符号は Berry 曲率規約を 2 バンド検証で整合; 絶対値は規約 + Blount 依存

### F6 ★★ Fröhlich ポーラロン結合
- **モジュール**: `src/perovskite_tb/polaron.py` / **テスト**: `tests/test_polaron.py`（7）/ **commit**: `d0ca915` / **データ**: `data/parameters/frohlich_polaron_params.json`（出典明記）
- **文献**: Fröhlich, Adv. Phys. 3, 325 (1954); Feynman 1955/1962; Frost, PRB 96, 195202 (2017)（α 式を ar5iv で確認）; Sendner et al., Nat. Commun. 12, 4945 (2021)
- **V&V**: **2 独立 published ベンチで前因子固定** — MAPbI₃ α=2.39(e)/2.68(h)（Frost）を <1% 再現; CsPbBr₃ α≈2（Sendner, ε∞=4.8/ε_S=20.5/LO=19.2 meV/m*=0.22）を再現
- **限界**: α + 先頭次弱結合質量 1+α/6 のみ（完全 Feynman variational 移動度は未実装）; 9 材料 α マップは各材料の cited な ε_S/ω_LO が必要（CsPbBr₃ 収集済）

### F12 ★★ 歪みバンド工学（変形ポテンシャル）
- **モジュール**: `src/perovskite_tb/bandengr.py` / **テスト**: `tests/test_bandengr.py`（8）/ **commit**: `e80e7e7`
- **文献**: Harrison, *Electronic Structure and the Properties of Solids*, Freeman (1980)（d⁻² スケーリング）; Bir-Pikus (1974); Buin 2014 / Grumet 2018
- **V&V**: Harrison 則 t_*(1+ε)⁻²（オンサイト/SOC 不変）; ε=0 で無歪みギャップ（CsPbI₃ 0.6298 eV）回復; 線形性; 引張/圧縮逆符号
- **限界**: SK-TB + Harrison **推定**。構造的挙動は模型内で厳密だが、a_g 絶対値は近似（DFT/実験との定量一致は非主張）

### F5+F13+F14-A ★★★ 有限 z スラブ / 超格子 / Stark スラブ
- **モジュール**: `src/perovskite_tb/slab.py` / **テスト**: `tests/test_slab.py`（7）/ **commit**: `0f123ae`
- **文献**: Smith-Mailhiot, RMP 62, 173 (1990)（超格子 TB）; Even-Pedesseau-Katan, **ChemPhysChem 15, 3733 (2014)**（2D RP 量子閉じ込め, §3.2 の引用訂正参照）; Blancon et al., Science 355, 1288 (2017); Neugebauer-Scheffler, PRB 46, 16067 (1992)
- **手法**: 3D Bloch H をゲージ変換 U(k_z)=diag(e^{−ik_z z_α})（X_z ハライド軌道は z=a/2; in-repo コードから確定, 推測なし）で 2π/a 周期化 → 厳密 Fourier 分解で intra-cell H∥ と inter-cell T。ブロック三重対角スラブ
- **V&V**: 層ブロック**厳密再構成**（H∥+T e^{ik_z a}+h.c. == 3D H, 機械精度）; **周期スタック == 3D バンド**（k_z=2πm/(Na), F13）; ミニバンド崩壊（inter-layer→0）; open スラブのギャップ厚み収束（F5）; **Stark**: E=0 回復 + 幅 ~eE(N−1)a（F14-A）
- **限界**: spacer/passivation は hard-barrier (open BC) 理想化（Even 2014）; E_g(n) 絶対値は SK-TB/Blount caveat

### F14-B ★★★ Berry 位相分極（KSV）
- **モジュール**: `src/perovskite_tb/polarization.py` / **テスト**: `tests/test_polarization.py`（4）/ **commit**: `5f06ec2`
- **文献**: King-Smith-Vanderbilt, PRB 47, 1651 (1993); Su-Schrieffer-Heeger, PRL 42, 1698 (1979)（SSH テスト模型）
- **V&V**: **SSH Zak 位相 0/π 量子化 + 位相転移で π ジャンプ**（厳密アンカー）; Rice-Mele（反転破れ）→ 連続シフト; ペロブスカイト電子 Zak finite/実/決定論的
- **限界（重要）**: ペロブスカイトの返り値は**電子 Berry 位相のみ**。物理的量子化分極は KSV のイオン寄与 + 分極量子が必要（total のみ gauge 不変・量子化）→ 量子化は SSH で検証、用途は ΔP（gauge 不変観測量）

---

## 2. 統計と再現性

- **新モジュール**: 10（`berry, topology, thermo, rashba, edelstein, cpge, polaron, bandengr, slab, polarization`.py）
- **新規テスト**: 82（22+12+6+8+4+4+7+8+7+4）/ **総テスト**: **313 passed**（既存 231 不変）
- **再現コマンド**:
  ```bash
  pip install -e .
  python -m pytest -q                       # 全 313
  python -m pytest tests/test_berry.py -q   # 機能別
  ```
- **ドキュメント**: `docs/numerical-methods.md` §9–§18（各機能の式・出典・V&V・限界）; `docs/repository-structure.md`（モジュール一覧）; `.steering/20260524-*/`（各機能の requirements）

---

## 3. ハルシネーション防止（handoff §0 準拠）の実施記録

### 3.1 グラウンディング
- 全引用文献（24+ 件）の DOI/arXiv を**着手前に web 検証**（実在・著者・年・巻号）。
- 主要な式は**原典を精読してグラウンディング**: Berry 曲率（Xiao Eq.1.13, ar5iv）、CPGE injection 式と量子化値（de Juan, ar5iv）、Fröhlich α 式と MAPbI₃ ベンチ（Frost, ar5iv）。
- 物性データは PI 認可で**自分で OA 収集**し、各値に一次出典を明記（`frohlich_polaron_params.json`）。

### 3.2 発見・是正した引用ミス（spec 記載の誤り）
- **Even-Pedesseau-Katan の 2D RP 量子閉じ込め論文**: 仕様書は「J. Phys. Chem. C 118, 11566 (2014)」と引用するが、その表題（"Understanding Quantum Confinement of Charge Carriers in Layered 2D Hybrid Perovskites"）の論文は実際は **ChemPhysChem 15, 3733 (2014)**（JPCC 118,11566 は別テーマ＝相転移の Even 論文）。→ 検証済みの ChemPhysChem を採用（`slab.py` docstring + docs §17 に明記）。

### 3.3 検証戦略
すべての絶対値主張は、解析解（Dirac, Rashba, 水素様）・既知模型（QWZ, SSH, Rice-Mele）・厳密則（Wiedemann-Franz）・位相量子化（Weyl, Chern, Zak）・published ベンチ（Frost/Sendner ポーラロン）のいずれかでアンカー。検証アンカーが立たない量（SHC/Rashba/Edelstein/CPGE/分極の絶対値）は**未検証であることを honest に明記**し、対称性・構造・相対トレンド・量子化のみを信頼する立場（既存 g_factor/shift_current と統一）。

---

## 4. 未実装機能と着手前提（no-hallucination の境界）

| 機能 | 未実装の理由 | 着手に必要な前提 |
|---|---|---|
| **F3 BSE 励起子** | 現実時間版（2 バンド有効質量 model BSE）は既存 `exciton.py`（Wannier-Mott）と重複し新規検証価値が薄い。真に新規な band-resolved TB-BSE（バンド混成・非放物線性）は spec どおり 4–6 週規模 | 腰を据えた数週の実装期間。検証: Cho 2019（in-repo, CsPbI₃ GW-BSE）/ Wannier-Mott 極限 |
| **F8 SHG (χ⁽²⁾)** | Aversa-Sipe χ² は interband+intraband+modulation の多項で、clean な定量アンカーが cubic→0 のみ → 未検証の式を出すリスク | Aversa-Sipe PRB 52, 14636 (1995) 精読 + 2 バンド解析 χ² の自前導出（定量検証用） |
| **F2 残（Z₂ parity / TRS-Z₂）** | Fu-Kane parity の反転演算子（基底は読めたが反転中心・inter-cell 対応の確証が要る）+ 検証用の既知 3D-Z₂ 模型が未整備。Wilson ループ基盤(`topology.py`)は流用可 | 反転演算子表現の確定（Kashikar 基底）+ 既知 3D-Z₂ 模型（Fu-Kane-Mele PRL 98,106803 / Bi₂Se₃ k·p）での parity 検証 |

これらは handoff §0 の「実在しない・確認できない/未検証のものは保留」「3 プロジェクト独立・ゼロから検証」の原則に従い、**着手前提が揃うまで意図的に未実装**とした。

---

## 5. 既存資産との整合（handoff §1.3）

- 既存テーマ（Theme A g 因子・Theme F shift current・Phase 1.5 光学・Theme I 励起子）と既存 Production bundle / 231 テストは**一切変更せず**、すべて不変。
- 新機能は既存 `velocity.py` / `models_kashikar.py` の共有基盤上に**非侵襲**に追加（相互再利用: F7/F4/F11 ← F1, F14-B ← topology, F11 ← thermo+berry）。
- 3 プロジェクト統合はしない方針（handoff §0.3）に従い、本実装は tb-perovskite 内で完結。

---

**(EOF)** — Reviewed for hallucination per `07_agent_handoff.md` §0.1; all cited DOIs/arXiv IDs verified 2026-05-24.
