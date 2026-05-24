# design — 追加検証タスク（09）

## 方針
- 物性予測（A比較）は**コアTB（Kashikar/Nestoklon）の固有値・波動関数**から導く。論文値は検算用。
- トイ模型（QWZ/Rashba/SSH/Wilson-Dirac）は**手法検証(B)専用**。材料の数値主張には使わない。
- 各タスク: ①DOI事前検証(web/crossref) → ②原典精読 → ③コアTBに検証関数追加 → ④テスト → ⑤benchmark JSON → ⑥図 → ⑦docs → ⑧自己批判レビュー。
- SK-TB/Blount 由来の絶対値は**honestにD維持**（無理にA化しない）。

## 新規インフラ（実装する関数）
- `bandstructure.effective_mass(builder, k0, band, ...)`: R点で E(k) を放物線フィットし m*/m0=(ħ²/m0)/(d²E/dk²)。T1-3 のポーラロン m* に使用。
- `bandengr.pressure_coefficient(params, a, B)`: a_g を体積弾性率Bで dE_g/dP[meV/GPa] に換算。T1-2。
- `topology.parity_delta_at_trim` / `z2_invariant_from_parities`: Fu-Kane parity Z₂。T2-2。
- `edelstein.longitudinal_conductivity` / `edelstein_ratio`: τ非依存効率 χ/σ。T2-4。
- `polarization.ferroelectric_polarization_difference`: 電子 ΔP_z=(e/2πA)(φ(d)−φ(0))。T2-3。

## タスク別設計
- **T1-1 (F5)**: slab.slab_gap で CsPbI₃ E_g(N) → 減衰べき指数 p を Blancon 自由粒子ギャップ(検証済)と比較。トレンド限定。
- **T1-2 (F12)**: bandengr の Harrison a_g → 圧力係数 → 符号(実験一致)＋大きさ(過大, tilting欠如)。
- **T1-3 (F6)**: effective_mass で全9材料 m* → CsPbBr₃ で TB駆動 α。誘電データは cited のみ。
- **T2-1 (F4)**: 極性 Kashikar の α_R → バルクDFT(CsPbF₃)と順序一致/絶対値過小。
- **T2-2 (F1/F2)**: Fu-Kane parity を Wilson-Dirac 模型で検証。実ペロブスカイトは反転演算子未確定で保留。
- **T2-3 (F14-B)**: 極性変位の電子 ΔP → 符号反転＋DFTと同オーダ（電子寄与のみ）。
- **T2-4 (F11)**: χ_yx/σ_xx → 2D Rashba 解析値 mα/(4μ) と一致＋極性ペロブスカイト効率。

## 影響範囲
- 既存 314 テストは不変（追加は新規 or append）。docs §10/§12/§13/§15/§16/§17 を更新。
- benchmark JSON: blancon2018_2drp_gaps / strain_benchmark / rashba_bulk_benchmark / polarization_fe_benchmark / frohlich_polaron_params（拡充）。
