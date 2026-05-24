# tb-perovskite — 拡張機能 実装報告書

**作成日**: 2026-05-24 ／ **最終更新**: 2026-05-24（実装後のリファクタリング・効率化を反映, §6 追加）
**実装者**: Claude Code（実装エージェント）
**対象仕様**: `03_tb-perovskite_spec.md`（F1–F14）+ `07_agent_handoff.md`（実装手順・ハルシネーション防止指針）
**リポジトリ**: `tb-perovskite`（既存 Slater–Koster / Jancu TB ペロブスカイトコード）

---

## 0. エグゼクティブサマリ

仕様書 `03_tb-perovskite_spec.md` の F1–F14 のうち、**現実時間で「文献グラウンディング + 厳密 V&V + 無捏造」を満たせる 12 feature-slot を実装完了**した（10 新モジュール、新規モジュールテスト 82、全 **314 passed**、既存 231 テスト不変）。
実装後に**可読性リファクタリング + 効率化パス**（挙動・数値は完全等価を検証, §6）を実施済み。

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
- **新規テスト**: 82（22+12+6+8+4+4+7+8+7+4, 新モジュール）+ 1（§6 の nestoklon batch 等価ガード）/ **総テスト**: **314 passed**（既存 231 不変）
- **再現コマンド**:
  ```bash
  pip install -e .
  python -m pytest -q                       # 全 314
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

## 6. 実装後のリファクタリング・効率化（2026-05-24）

初回実装（§1）の後、**挙動・数値を完全に保ったまま**可読性と速度を改善した。各変更は、(a) リファクタは既存
314 テストを回帰チェックとして、(b) 効率化は「旧実装の出力を先に保存 → 新実装が機械精度で一致」を確認する
等価性ガードで担保した（物理は不変）。

### 6.1 可読性（DRY, 挙動不変）
- **`berry.py`**: ほぼ同一だった `berry_curvature_kubo` / `spin_berry_curvature_kubo` を共通ヘルパ `_kubo_sum(evals, Ax, Vy, tol)` に統合（差は x 側頂点のみ）。
- **`_constants.py`**: `RYDBERG_EV / G0 / KB_EV / COULOMB_EV_ANG` を集約（exciton/g_factor/thermo/optical が import）。`optical.py` の `14.39964` 二重リテラルを解消。
- **`tests/_helpers.py`**: 共通 Pauli 行列・QWZ ビルダ・材料ローダを集約し、property 系テストの重複を解消。

### 6.2 効率化（物理的に等価, 数値検証済み）
| 対象 | 手法 | 効果 | 等価性検証 |
|---|---|---|---|
| **`shift_current.py`** nestoklon 極性ビルダ | k 方向にベクトル化し `(K,3)→(K,2N,2N)`（SOC は k 非依存で一度だけ構築・broadcast）, `_batched=True` で既存 batched パスを使用 | フルスイート **~217s → ~105s（約 2×）**, 最重テスト `test_polar_displacement` **71s → 18s** | 旧 per-k 出力と最大誤差 **1.4e-14**（H は完全一致）, 永続ガード `test_nestoklon_polar_builder_batched_matches_single` |
| **`cpge.py`** `cpge_tensor` | per-k + occ/unocc ループを batched eigh + einsum(k,n,m) に書換 | `test_weyl_quantization` **8.7s → 0.83s（約 10×）** | 旧ループ出力と最大誤差 **8.3e-16** |
| **`thermo.py`** `transport_distribution` | per-sample Gaussian ループをチャンク化ベクトル演算に | 該当テスト **1.85s → 1.46s** | 同一の Gaussian 和（formula 不変） |
| **`cpge.py`** ε 縮約 | `Σ ε_jkl r^k r^l` を `np.cross` に | 微小 + 可読性↑ | 同一縮約 |

すべて **Production の数値・既存 231 テストは不変**、新規含め **314 passed**。

### 6.3 ドキュメント追従
- `docs/numerical-methods.md`: 冒頭に目次（コア §1–8 + 物性モジュール §9–18）を追加。
- `README.md`: 「計算できる物性」表（10+ モジュール ↔ 物理量）を追加し、本報告書と numerical-methods §9–18 へリンク。

### 6.4 フォルダ構成・ドキュメント構成の評価
- `src/perovskite_tb/` のフラット構成（~30 モジュール）は既存規約と整合 → **サブパッケージ化は不要**（import パス・規約を壊す割に利得が薄い）。
- `.steering/` の蓄積は CLAUDE.md 規約どおりの作業履歴。`data/parameters/` は整然、API キーは gitignore（漏洩なし）、PDF は非追跡（肥大化なし）。
- 関連 commit: `6fd36e5`（可読①②③ + thermo/cpge 初期効率化）, `3c8b58d`（nestoklon batch）, `b12e04e`（cpge ベクトル化 + docs）。

---

## 7. 追加検証タスク（09）— 2026-05-24

`09_additional_validation_tasks.md` の Tier-1/Tier-2 を **全 7 件実施**（テスト 314→**330**, 全 pass）。**コア TB のエネルギー・波動関数で物性を計算**（論文値は検算）。詳細・達成カテゴリ・引用訂正 4 件は **`08_validation_status_quantitative.md` §7** を参照。要約:

| タスク | 達成カテゴリ（honest） | 新規インフラ |
|---|---|---|
| T1-1 F5 Blancon トレンド | C→B（減衰指数 15%以内）| — |
| T1-2 F12 歪み dE_g/dε | C（符号一致）/ D（絶対 過大）| `bandengr.pressure_coefficient` |
| T1-3 F6 TB-駆動 polaron α | A（公式）/ B | `bandstructure.effective_mass`（全9材料 m\*）|
| T2-1 F4 Rashba バルク DFT | C（CBM>VBM 順序）/ D（絶対 ~40×小）| — |
| T2-2 F1/F2 Z₂ parity | B（Wilson-Dirac 相図再現, 「未実装」解消）| `topology.z2_invariant_from_parities` / `parity_delta_at_trim` |
| T2-3 F14-B 強誘電 ΔP | C→B（符号反転 + DFT と同オーダ）| `polarization.ferroelectric_polarization_difference` |
| T2-4 F11 χ/σ 比 | B（2D Rashba 解析値 mα/(4μ) 一致）| `edelstein.longitudinal_conductivity` / `edelstein_ratio` |

### 7.1 タスク別詳細

#### T1-1 — F5 2D-RP 閉じ込め E_g(n)（`slab.py`, `test_blancon_layer_dependence`）
- **コア TB**: Kashikar-13 CsPbI₃ スラブ（hard-barrier）の閉じ込めギャップ E_g(N) を R 点面内射影 (π/a,π/a) で算出。
- **出典（検証済）**: J.-C. Blancon et al., "Scaling law for excitons in 2D perovskite quantum wells", **Nat. Commun. 9, 2254 (2018), DOI 10.1038/s41467-018-04659-x**（自由粒子ギャップ n=1: 2.540, n=4: 2.078, n=5: 1.846 eV; Fig.3a/4 から検証）。
- **V&V / カテゴリ**: 減衰べき指数 p_TB≈0.93 vs p_exp≈0.85（自由粒子基準 E∞≈1.65–1.70 eV）→ **15%以内**。**C→B（トレンド限定）**。図 `results/figures/blancon_E_g_n.png`、benchmark `data/parameters/blancon2018_2drp_gaps.json`。
- **限界**: 無機 CsPbI₃ アナログ vs MAPbI₃ 系 RP（材料差）+ SK-TB → 絶対 E_g(n) は非主張。p_exp は E∞ に敏感（1.60→0.71, 1.70→0.91）。**commit `7eef9b5`**。

#### T1-2 — F12 歪み変形ポテンシャル dE_g/dε（`bandengr.py`, `test_strain_gap_sensitivity_lit`）
- **コア TB**: Harrison d⁻² でスケールした Kashikar-13 の R 点ギャップ応答 → `pressure_coefficient(params,a,B)` で dE_g/dP に換算。
- **出典（検証済）**: 実験 A. Pieniazek et al., **J. Phys. Chem. Lett. 14, 6470 (2023), DOI 10.1021/acs.jpclett.3c01258**（MAPbI₃ dE_g/dP = −13〜−41 meV/GPa）; 体積弾性率 Y. Liu et al., **Molecules 28, 7643 (2023), DOI 10.3390/molecules28227643**（CsPbI₃ 9.87, CsPbBr₃ 13.36, CsPbCl₃ 16.01 GPa）。
- **V&V / カテゴリ**: 符号一致（加圧で gap 減 = dE_g/dε>0）**C**。大きさは TB dE_g/dP≈−210 meV/GPa vs 実験 −13〜−41 → **~5–16× 過大（D）**。benchmark `data/parameters/strain_benchmark.json`。
- **限界**: cubic-frozen TB は **octahedral tilting 自由度なし**でボンド長寄与のみ捉える → 過大評価。**引用訂正**: Buin 2014（trap-free 合成）・Grumet PRB 98,155143（GW 手法論文, crossref 確認）は歪みと無関係 → 削除。**commit `a4f1fc1`**。

#### T1-3 — F6 TB-駆動 Fröhlich polaron α（`polaron.py`/`bandstructure.py`, `test_cspbbr3_alpha_from_core_tb_mass` 他）
- **コア TB**: `bandstructure.effective_mass`（R 点放物線フィット, 合成放物線で厳密検証）で **全 9 CsBX₃ の m\*** を算出（`results/tb_effective_masses.json`; 例 CsPbBr₃ 0.151, CsPbI₃ 0.106, CsSnI₃ 0.035, 全て等方）。
- **出典（検証済）**: Frost, **PRB 96, 195202 (2017)**（α 公式）; Sendner, **Nat. Commun. 12, 4945 (2021)**（CsPbBr₃ ε∞=4.8, ε_S=20.5, LO=19.2 meV）。
- **V&V / カテゴリ**: CsPbBr₃ TB-駆動 α_TB=1.66 vs 文献 2.0 → 差 −17% は **完全にバンド質量比** √(0.151/0.22)=0.83 で説明（公式は m\*=0.22 で文献を <1% 再現）。**A（公式）/ B**。
- **限界**: 9 材料 α マップは **Cs 系無機の cited 誘電/LO データが一次出典に存在しない**ため完成不可（Sendner 2016/Wright 2016/arXiv:2201.06360 はいずれも MA 系のみ）→ 捏造回避で部分。**commit `b8baaca`**。

#### T2-1 — F4 Rashba α_R バルク DFT 比較（`rashba.py`, `test_bulk_dft_comparison`）
- **コア TB**: [001] 極性（P4mm）Kashikar-13 の doublet 分裂から α_R=ΔE/(2|k|)。
- **出典（検証済）**: P. Bhumla et al., **arXiv:2108.03683 (2021)**（無機強誘電バルク CsPbF₃: α_R CBM=1.05, VBM=0.41 eVÅ）。**表面** Rashba（Niesner PRL 117,126401, ~11 eVÅ）は別系で除外。
- **V&V / カテゴリ**: **CBM>VBM 順序**は DFT 一致 **C**。絶対値 TB CBM≈0.027 eVÅ は DFT 1.05 の **~1/40（D）**。benchmark `data/parameters/rashba_bulk_benchmark.json`。
- **限界**: 剛体副格子変位モデル（実強誘電歪みに未校正）+ Blount → 過小評価。**commit `be6dcc0`**。

#### T2-2 — F1/F2 Fu-Kane parity Z₂（`topology.py`, `test_wilson_dirac_parity_z2` 他）
- **手法検証（トイ模型）**: `parity_delta_at_trim` / `z2_invariant_from_parities` を実装。反転対称 3D Wilson-Dirac (BHZ 型) 模型で固有ベクトル抽出パリティ=解析値 −sign(M)、強指数 ν₀ が解析相図（1<|m₀|<3 で STI）を再現。Berry 曲率の質量符号反転も確認。
- **出典（検証済）**: Fu, Kane, **PRB 76, 045302 (2007)**（parity 規準）; Fu, Kane, Mele, **PRL 98, 106803 (2007)**（3D Z₂）。
- **カテゴリ B**。docs §10 の「未実装」解消。**限界**: 実ペロブスカイト（Kashikar 基底）への適用は反転演算子の表現が未確定のため保留（捏造せず）。**commit `591b3a9`**。

#### T2-3 — F14-B 強誘電 ΔP（`polarization.py`, `test_ferroelectric_delta_p_*`）
- **コア TB**: 極性 Kashikar-13 の電子 Zak 位相差 ΔP_z=(e/2πA)(φ(d)−φ(0)) を μC/cm² で算出。
- **出典（検証済）**: Bhumla et al., **arXiv:2108.03683 (2021)**（CsPbF₃ P=34 μC/cm²）; 典型 FE ハライドは数 μC/cm²。
- **V&V / カテゴリ**: 変位 0 で ΔP=0、**ΔP(−d)=−ΔP(+d)**（FE 符号反転, gauge 不変, 小 d で反対称）、大きさ ~1–8 μC/cm²（DFT と同オーダ）。**C→B**。benchmark `data/parameters/polarization_fe_benchmark.json`。
- **限界**: **電子寄与のみ**（DFT 値は ionic+electronic の total）→ 定量一致は非主張。**commit `251140f`**。

#### T2-4 — F11 Edelstein 効率 χ_yx/σ_xx（`edelstein.py`, `test_rashba_edelstein_ratio_analytic` 他）
- **コア TB / 手法**: `longitudinal_conductivity` を同じ CRTA Fermi 窓で実装し、`edelstein_ratio`=χ_yx/σ_xx（τ・k 格子正規化がキャンセル）。
- **出典（検証済）**: Edelstein, **Solid State Commun. 73, 233 (1990)**。
- **V&V / カテゴリ**: 2D Rashba で χ_yx/σ_xx = **mα_R/(4μ)**（自前導出）を 15%以内（α=0.05 で 3.6%）再現、χ_xx/σ_xx≈0、α に線形。極性 CsPbI₃（P4mm）効率は TB 予測値（実験照合は文献待ち）。**B**。**commit `163d8d1`**。

**V&V カテゴリ更新**: A は F6 polaron（公式 <1% + TB-駆動 α）・F9 WF（0.5%）が中心。多くは SK-TB/Blount の構造限界で符号/順序/トレンド/量子化/τ非依存比（B/C）に留まり、絶対値は honest に D 維持（09 の「全 A 化」想定に対する誠実な現実; 捏造回避）。

---

**(EOF)** — Reviewed for hallucination per `07_agent_handoff.md` §0.1; all cited DOIs/arXiv IDs verified 2026-05-24 (incl. §7 additional references via web/crossref). §6 efficiency changes verified numerically equivalent to the pre-refactor implementation (machine precision).
